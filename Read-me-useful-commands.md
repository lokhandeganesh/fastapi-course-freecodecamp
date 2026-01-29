## This document will help you to introduce useful commands to run project

### Working with `uv`

<div id="badges">
  <a href="https://docs.astral.sh/uv/">
    <img src="https://docs.astral.sh/uv/assets/logo-letter.svg" alt="uv Badge"/>
  </a>

  An extremely fast Python package and project manager
</div>

### To install uv or check version
`pip install uv`

* then lets check whether its installed properly by printing its version

`uv --version`

* if you want to add new dependancy library into project, eg. pandas

`uv add pandas`

### Running project

after installing `uv` we will spin our project directory to run as local server,
here we will bind our `main.py` which is kept inside of `app` folder to `:app`, with port of `8000` and we will reload server if any changes happen to file with flag `--reload`

`uv run uvicorn app.main:app --port 8000 --reload`

this will run our project with `http://localhost:8000`

### Working with `almebic`

Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine
https://alembic.sqlalchemy.org/en/latest/index.html

you can find docs of almebic by running
`uv run alembic --help`

* this command will create new .py file in name of version_number and comment of it which we will use to change db

`uv run alembic revision -m "add user table"`

* to check your current version number
`uv run alembic current`

* to check history of your versions
`uv run alembic history`

* to check your current head
`uv run alembic heads`

* to run the latest revesion
`uv run alembic upgrade head`

* to run previous version, can simply run commands using numrical value, like `+1, +2 or -1, -2`, where each number represents steps from current version
`uv run alembic upgrade +1`

* almebic is intelegent enough to detect your models defination and your current tabel structure in db
`uv run alembic revision --autogenerate -m "auto-vote"`