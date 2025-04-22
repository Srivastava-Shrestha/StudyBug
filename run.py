# StudyBug/run.py

from app import app_creator
from app.config import Configuration

if __name__ == "__main__":
    app_creator(Configuration)
