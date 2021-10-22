import pickle
import re
from pathlib import Path

admin_list = []
DATABASE_FILE = "admins.pickle"


def init_admin_database():
    global admin_list
    database_path = Path(DATABASE_FILE)
    if database_path.exists():
        f = open(DATABASE_FILE, "rb")
        admin_list = pickle.load(f)
        f.close()
    else:
        admin_list = []


def get_admins():
    return admin_list


def add_admins(*args):
    admin_list.append(args)
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(admin_list, f)


def update_admins():
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(admin_list, f)
