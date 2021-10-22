import pickle
import re
from pathlib import Path

cars = []
DATABASE_FILE = "cars.pickle"


def init_database_cars():
    global cars
    database_path = Path(DATABASE_FILE)
    if database_path.exists():
        f = open(DATABASE_FILE, "rb")
        cars = pickle.load(f)
        f.close()
    else:
        cars = []


def get_cars():
    return cars


def add_cars(*args):
    cars.append(args)
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(cars, f)


def update_cars():
    with open(DATABASE_FILE, "wb") as f:
        pickle.dump(cars, f)
