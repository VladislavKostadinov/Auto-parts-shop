import pickle
import re
from pathlib import Path

approved_users = []
DATABASE_FILE = "approved.pickle"


def init_approved_users_database():
    global approved_users
    database_path = Path(DATABASE_FILE)
    if database_path.exists():
        f = open(DATABASE_FILE, "rb")
        approved_users = pickle.load(f)
        f.close()
    else:
        approved_users = []


def get_approved_users():
    return approved_users


def add_approved_users(*args):
    approved_users.append(args)
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(approved_users, f)


def update_approved_users():
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(approved_users, f)
