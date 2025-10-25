from __future__ import annotations
from typing import Callable
import os
import csv
import sys
import time
import uuid

STATIONS_FILE = "stations.csv"
LINES_FILE = "lines.csv"
TICKETS_FILE = "tickets.csv"
DELIMITER = ","
LIST_DELIMITER = "$"
NEWLINE = ""
DELAY = 2


class Node:

    depth: int = 0
    layer: list[Node] = []

    def __init__(self, value: int) -> None:
        self.value: int = value
        self.children = []
        self.parent: Node

    def __repr__(self) -> str:
        return str(self.value)
    
    def add_child(self, child: Node) -> None:
        pass


class Station:
    
    stations: dict[int, Station] = {}

    def __init__(self, uid: int, name: str, neighbours: tuple[Station, ...]) -> None:
        self.uid: int = uid
        self.name: str = name
        self.neighbours: tuple[Station, ...] = neighbours

    def __repr__(self) -> str:
        return self.name

    @classmethod
    def load(cls) -> None:
        try:
            with open(STATIONS_FILE, "r", newline=NEWLINE) as file:
                reader = csv.DictReader(file, delimiter=DELIMITER)
                for row in reader:
                    cls.stations[int(row["uid"])] = Station(int(row["uid"]), row["name"], tuple(map(cls.from_uid, map(int, row["neighbours"].split(LIST_DELIMITER)))))
        except (FileNotFoundError, IOError, csv.Error, KeyError):
            print(f'Error loading {STATIONS_FILE}!')
            time.sleep(DELAY)
            sys.exit(0)

    @classmethod
    def display(cls) -> None:
        for station in cls.stations:
            print(f'[{station}]: {cls.stations[station].name}')

    @classmethod
    def from_uid(cls, uid: int) -> Station:
        return cls.stations[int(uid)]

    @classmethod
    def display_map(cls) -> None:
        pass


class Line:

    lines: tuple[Line, ...] = tuple()

    def __init__(self, name: str, stations: tuple[Station, ...]) -> None:
        self.name = name
        self.stations: tuple[Station, ...] = stations

    def __repr__(self) -> str:
        return self.name

    @classmethod
    def load(cls) -> None:
        try:
            with open(LINES_FILE, "r", newline=NEWLINE) as file:
                reader = csv.DictReader(file, delimiter=DELIMITER)
                temp: list[Line] = []
                for row in reader:
                    temp.append(Line(row["name"], tuple(map(Station.from_uid, map(int, row["stations"].split(LIST_DELIMITER))))))
                cls.lines = tuple(temp)
        except (FileNotFoundError, IOError, csv.Error, KeyError):
            print(f'Error loading {LINES_FILE}!')
            time.sleep(DELAY)
            sys.exit(0)


class Ticket:

    tickets: set[Ticket] = set()

    def __init__(self, uid: str, start_uid: int, stop_uid: int) -> None:
        self.uid: str = uid
        self.start_uid: int = start_uid
        self.stop_uid: int = stop_uid
        self.path = []

    def __repr__(self) -> str:
        return self.uid
    
    @classmethod
    def load(cls) -> None:
        try:
            with open(TICKETS_FILE, "r") as file:
                reader = csv.DictReader(file, delimiter=DELIMITER)
                temp: list[Ticket] = []
                for row in reader:
                    temp.append(Ticket(row["uid"], int(row["start_uid"]), int(row["stop_uid"])))
                cls.tickets = set(temp)
        except (FileNotFoundError, IOError, csv.Error, KeyError):
            print(f'Error loading {TICKETS_FILE}!')
            time.sleep(DELAY)
            sys.exit(0)

    @classmethod
    def buy(cls, start_uid: int, stop_uid: int) -> None:
        cls.tickets.add(Ticket(cls.create_uid(), start_uid, stop_uid))
            
    @classmethod
    def display(cls) -> None:
        for ticket in cls.tickets:
            print(f'[{ticket.uid}]: {Station.from_uid(ticket.start_uid)} => {Station.from_uid(ticket.stop_uid)}')
    
    @classmethod
    def remove(cls, uid: str) -> None:
        for ticket in cls.tickets:
            if ticket.uid == uid:
                cls.tickets.remove(ticket)

    @classmethod
    def save(cls) -> None:
        try:
            with open(TICKETS_FILE, "w", newline=NEWLINE) as file:
                writer = csv.writer(file, delimiter=DELIMITER)
                writer.writerow(["uid", "start_uid", "stop_uid"])
                for ticket in cls.tickets:
                    writer.writerow([ticket.uid, ticket.start_uid, ticket.stop_uid])
        except (FileNotFoundError, IOError, csv.Error, KeyError):
            print(f'Error writing to {TICKETS_FILE}!')
            time.sleep(DELAY)
            sys.exit(0)

    @staticmethod
    def create_uid() -> str:
        uid: uuid.UUID = uuid.uuid4()
        return uid.hex

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def close():
    Ticket.save()
    clear()
    sys.exit(0)

def remove():
    clear()
    Ticket.display()
    choice: str = input("Enter the ID of the ticket to remove: ")
    Ticket.remove(choice)
    print(f'Ticket with ID: {choice} has been deleted!')

def buy():
    start_uid: int
    stop_uid: int
    while True:
        clear()
        Station.display()
        try:
            start_uid = int(input("Enter starting Station ID: "))
            if start_uid not in Station.stations.keys():
                raise ValueError
            break
        except ValueError:
            print("Not a valid Station ID!\nTry Again...")
            time.sleep(DELAY)
            continue
    while True:
        clear()
        Station.display()
        try:
            stop_uid = int(input("Enter destination Station ID: "))
            if stop_uid not in Station.stations.keys():
                raise ValueError
            break
        except ValueError:
            print("Not a valid Station ID!\nTry Again...")
            time.sleep(DELAY)
            continue
    if start_uid == stop_uid:
            print("Start and Destination cannot be the same!\nTry Again...")
            time.sleep(DELAY)
            return
    price = 10
    while True:
        clear()
        try:
            print(f'Start: {Station.from_uid(start_uid)}\nDestination: {Station.from_uid(stop_uid)}\nThe price will be ${price}')
            choice = input("Do you wish to purchase this ticket? (y/n)\n").lower()
            if choice == "y":
                Ticket.buy(start_uid, stop_uid)
                return
            elif choice == "n":
                return
            else:
                raise ValueError
        except ValueError:
            print("Error!\nTry again...")
            time.sleep(DELAY)
            continue

def view():
    clear()
    Ticket.display()
    input("Press enter to finish viewing...")

def view_map():
    clear()
    Station.display_map()
    input("Press enter to finish viewing...")

menu: dict[int, Callable[[], None]] = {
    1: view,
    2: buy,
    3: remove,
    4: view_map,
    0: close
}

def main():
    Station.load()
    Line.load()
    Ticket.load()
    while True:
        clear()
        print("MAIN MENU\n--------------\n[1] => View tickets\n[2] => Buy tickets\n[3] => Remove tickets\n[4] => Station Map\n[0] => Exit")
        try:
            choice = int(input("Enter Option ID: "))
            if choice not in menu:
                raise ValueError
        except ValueError:
            print("Not a valid option!\nTry Again...")
            time.sleep(DELAY)
            continue
        func = menu.get(choice)
        if func:
            func()

if __name__ == "__main__":
    main()
