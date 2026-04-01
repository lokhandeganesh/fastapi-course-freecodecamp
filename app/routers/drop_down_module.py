from fastapi import APIRouter, Depends, HTTPException, status
# import json
# from fastapi.responses import JSONResponse

import orjson
from fastapi.responses import ORJSONResponse

# from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_files.database import get_db
from app.db_files.redis import get_redis, get_seconds_until_next_7am
from app.logging.logger import logger
from app.schema import params_schemas

from sqlalchemy import select
from app.model.admin_models import Village

router = APIRouter(tags=['Administrative-Information'])


# fetching village api
@router.post("/get_villages")
async def get_villages(
    village_info: params_schemas.VillageInfo,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis)
  ):
    """
    """
    # Cache Key Generation (Join tuple into a string)
    cache_parts = (
        "villages",
        f":dist-{village_info.district_code or 'all'}",
        f":tal-{village_info.taluka_code or 'all'}",
        f":vil-{village_info.village_code or 'all'}",
        f":poc-{village_info.is_pocra or 'all'}",
        f":phs-{village_info.phase or 'all'}"
    )
    cache_key = "".join(cache_parts)

    # Optional Redis Cache Check
    if redis:
        try:
            cached_data = await redis.get(cache_key)
            if cached_data:
                logger.info(f"Cache HIT: {cache_key}")
                return {
                    "status": status.HTTP_200_OK,
                    "response": "Villages list (cached)",
                    "data": orjson.loads(cached_data)
                }
        except Exception as e:
            logger.warning(f"Redis lookup failed (skipping): {e}")

    # Pure SQLAlchemy Dynamic Filtering (Clean Map & Loop)
    stmt = select(
        Village.dtncode, Village.dtname, Village.dtmname,
        Village.thncode, Village.thname, Village.thmname,
        Village.vincode, Village.vlname, Village.vilmname,
        Village.extent['xmax'].as_float().label("xmax"),
        Village.extent['xmin'].as_float().label("xmin"),
        Village.extent['ymax'].as_float().label("ymax"),
        Village.extent['ymin'].as_float().label("ymin")
    )

    # Map the model columns to user inputs
    filters = {
        Village.dtncode: village_info.district_code,
        Village.thncode: village_info.taluka_code,
        Village.vincode: village_info.village_code,
        Village.is_pocra: village_info.is_pocra,
        Village.phase: village_info.phase
    }

    # Only apply where value is not None
    for column, value in filters.items():
        if value is not None:
            stmt = stmt.where(column == value)

    stmt = stmt.order_by(Village.dtname, Village.thname)

    try:
        # Database Execution
        result = await db.execute(stmt)
        # .mappings().all() gives you the list of dictionaries (like dict_row)
        villages = [dict(row) for row in result.mappings().all()]

        if not villages:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Data Found for the given filters"
            )

        # Get next 7 AM timestamp
        expire_at_seconds = get_seconds_until_next_7am()
        # Cache the data in Redis
        await redis.set(cache_key, orjson.dumps(villages), ex=expire_at_seconds)

        logger.info(f"Cached new data for key: {cache_key}")

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": status.HTTP_200_OK,
                "response": "Villages list",
                "data": villages
            }
        )

    except HTTPException:
        # Let FastAPI handle HTTPException (like 404)
        raise
    except Exception as e:
        # Log the exception for debugging
        logger.exception(f"Unhandled error in get_talukas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in fetching data")
