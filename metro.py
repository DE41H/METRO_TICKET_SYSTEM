from __future__ import annotations
from typing import Callable

import csv
import sys
import uuid


# class Node:

#     depth: int = 0
#     layer: list[Node] = []

#     def __init__(self, value: int) -> None:
#         self.value: int = value
#         self.children = []
#         self.parent: Node

#     def __repr__(self) -> str:
#         return str(self.value)
    
#     def add_child(self, child: Node) -> None:
#         pass


class Config:

    STATIONS_FILE: str = "stations.csv"
    LINES_FILE: str = "lines.csv"
    TICKETS_FILE: str = "tickets.csv"
    DELIMITER: str = ","
    LIST_DELIMITER: str = "$"
    NEWLINE: str = ""
    DELAY: int = 2


class Menu:

    functions: dict[int, Callable[[], None]]  = {}
    options: dict[int, str] = {
        1: "Purchase Tickets",
        2: "View Tickets",
        3: "Delete Tickets",
        0: "Exit"
    }

    def __init__(self) -> None:
        self.functions[1] = self.buy_tickets
        self.functions[2] = self.view_tickets
        self.functions[3] = self.remove_tickets
        self.functions[0] = self.exit

    def menu(self) -> None:
        while True:
            print("\n=============[ MAIN MENU ]=============\n")
            for number, option in self.options.items():
                print(f'[{number}] >>> {option}')
            try:
                choice = int(input("\nEnter Option ID: "))
                if choice not in self.functions:
                    raise ValueError
            except ValueError:
                print("Not a valid option!\nTry Again...")
                continue
            func = self.functions.get(choice)
            if func:
                func()
    
    def view_tickets(self) -> None:
        Ticket.display()
        input("\nPress ENTER to finish viewing...")
        
    def buy_tickets(self) -> None:
        start_uid: int = self.input_station_id("starting")
        stop_uid: int = self.input_station_id("destination")
        while start_uid == stop_uid:
            print("Starting and Destination cannot be the same!\nTry Again...")
            stop_uid: int = self.input_station_id("destination")
            continue
        self.confirm_purchase(start_uid, stop_uid)
    
    @staticmethod
    def confirm_purchase(start_uid: int, stop_uid: int) -> None:
        price: int = 10
        while True:
            try:
                print(f'Starting: {Station.from_uid(start_uid)}\nDestination: {Station.from_uid(stop_uid)}\nPrice: ${price}')
                choice = input("Do you wish to purchase this ticket? (y/n)\n").strip().lower()
                match choice:
                    case "y":
                        Ticket.buy(start_uid, stop_uid)
                        return
                    case "n":
                        return
                    case _:
                        raise ValueError
            except ValueError:
                print("Error!\nTry again...")
                continue

    @staticmethod
    def remove_tickets() -> None:
        Ticket.display()
        choice: str = input("Enter Ticket ID: ")
        if Ticket.remove(choice):
            print(f'Ticket with ID: {choice} has been deleted!')
        else:
            print("Invalid Ticket ID!")

    @staticmethod
    def exit() -> None:
        Ticket.save()
        sys.exit(0)

    @staticmethod
    def input_station_id(prompt: str) -> int:
        while True:
            Station.display()
            try:
                uid = int(input(f'Enter {prompt} Station ID: '))
                if uid not in Station.stations:
                    raise ValueError
                return uid
            except ValueError:
                print("Not a valid Station ID!\nTry Again...")
                continue


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
            with open(Config.STATIONS_FILE, "r", newline=Config.NEWLINE) as file:
                reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                for row in reader:
                    cls.stations[int(row["uid"])] = Station(int(row["uid"]), row["name"], tuple())
                for row in reader:
                    cls.stations[int(row["uid"])].neighbours = cls.from_str(row["neighbours"])
        except (FileNotFoundError, IOError, csv.Error, KeyError) as err:
            print(f'Error loading {Config.STATIONS_FILE}: {err}')
            Menu.exit()

    @classmethod
    def display(cls) -> None:
        for uid, station in cls.stations.items():
            print(f'[{uid}]: {station.name}')

    @classmethod
    def from_uid(cls, uid: int) -> Station:
        return cls.stations[int(uid)]
    
    @classmethod
    def from_str(cls, prompt: str) -> tuple[Station, ...]:
        arr: list[int] = [int(item) for item in prompt.split("$")]
        return tuple([cls.from_uid(item) for item in arr])


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
            with open(Config.LINES_FILE, "r", newline=Config.NEWLINE) as file:
                reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                temp: list[Line] = []
                for row in reader:
                    temp.append(Line(row["name"], Station.from_str(row["stations"])))
                cls.lines = tuple(temp)
        except (FileNotFoundError, IOError, csv.Error, KeyError) as err:
            print(f'Error loading {Config.LINES_FILE}: {err}')
            Menu.exit()


class Ticket:

    tickets: dict[str, Ticket] = {}

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
            with open(Config.TICKETS_FILE, "r") as file:
                reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                for row in reader:
                    cls.tickets[row["uid"]] = Ticket(row["uid"], int(row["start_uid"]), int(row["stop_uid"]))
        except (FileNotFoundError, IOError, csv.Error, KeyError) as err:
            print(f'Error loading {Config.TICKETS_FILE}: {err}')
            Menu.exit()

    @classmethod
    def buy(cls, start_uid: int, stop_uid: int) -> None:
        cls.tickets[cls.create_uid()] = Ticket(cls.create_uid(), start_uid, stop_uid)
            
    @classmethod
    def display(cls) -> None:
        for uid, ticket in cls.tickets.items():
            print(f'[{uid}]: {Station.from_uid(ticket.start_uid)} => {Station.from_uid(ticket.stop_uid)}')
    
    @classmethod
    def remove(cls, uid: str) -> bool:
        if uid in cls.tickets:
            cls.tickets.pop(uid)
            return True
        else:
            return False

    @classmethod
    def save(cls) -> None:
        try:
            with open(Config.TICKETS_FILE, "w", newline=Config.NEWLINE) as file:
                writer = csv.writer(file, delimiter=Config.DELIMITER)
                writer.writerow(["uid", "start_uid", "stop_uid"])
                for uid, ticket in cls.tickets.items():
                    writer.writerow([uid, ticket.start_uid, ticket.stop_uid])
        except (FileNotFoundError, IOError, csv.Error, KeyError) as err:
            print(f'Error writing to {Config.TICKETS_FILE}: {err}')
            Menu.exit()

    @staticmethod
    def create_uid() -> str:
        uid: uuid.UUID = uuid.uuid4()
        return uid.hex


def main():
    Station.load()
    Line.load()
    Ticket.load()
    menu: Menu = Menu()
    menu.menu()

if __name__ == "__main__":
    main()
