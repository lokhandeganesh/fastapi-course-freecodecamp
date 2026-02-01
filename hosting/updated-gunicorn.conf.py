# gunicorn.conf.py
import multiprocessing
# import os

# log_path = "/home/lokhandeganesh/fastapi-course-freecodecamp/logs"
# os.makedirs(log_path, exist_ok=True)

workers = ((min(multiprocessing.cpu_count(), 4)) * 2) + 1
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"

# accesslog = f"{log_path}/access.log"
# errorlog = f"{log_path}/error.log"

accesslog = "-"
errorlog = "-"
loglevel = "info"