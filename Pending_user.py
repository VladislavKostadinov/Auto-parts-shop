import pickle
import re
from pathlib import Path

pending = []
DATABASE_FILE = "pending.pickle"


def init_database():
    global pending
    database_path = Path(DATABASE_FILE)
    if database_path.exists():
        f = open(DATABASE_FILE, "rb")
        pending = pickle.load(f)
        f.close()
    else:
        pending = []


def get_clients():
    return pending


def add_clients(*args):
    pending.append(args)
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(pending, f)


def update_clients():
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(pending, f)
