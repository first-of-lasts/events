from dotenv import load_dotenv
import os
import multiprocessing


load_dotenv()

DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
PORT = os.getenv("APP_PORT", "8000")
WORKERS = int(os.getenv("APP_WORKERS", multiprocessing.cpu_count() * 2 + 1))
#
bind = f"0.0.0.0:{PORT}"
workers = WORKERS
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "debug" if DEBUG else "info"

if DEBUG:
    reload = True
