import pickle
import re
from pathlib import Path

parts = []
DATABASE_FILE = "parts.pickle"


def init_database_parts():
    global parts
    database_path = Path(DATABASE_FILE)
    if database_path.exists():
        f = open(DATABASE_FILE, "rb")
        parts = pickle.load(f)
        f.close()
    else:
        parts = []


def get_parts():
    return parts


def add_parts(*args):
    parts.append(args)
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(parts, f)


def update_parts():
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(parts, f)
