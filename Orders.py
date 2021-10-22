import pickle
import re
from pathlib import Path

orders = []
DATABASE_FILE = "orders.pickle"


def init_database_orders():
    global orders
    database_path = Path(DATABASE_FILE)
    if database_path.exists():
        f = open(DATABASE_FILE, "rb")
        orders = pickle.load(f)
        f.close()
    else:
        orders = []


def get_orders():
    return orders


def add_orders(*args):
    orders.append(args)
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(orders, f)


def update_orders():
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(orders, f)
