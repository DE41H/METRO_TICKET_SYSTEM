from __future__ import annotations
from typing import Callable

import os
import sys
import csv
import uuid
from collections import deque


class Node:

    def __init__(self, value: Station) -> None:
        self.value: Station = value
        self.parent: Node

    def __repr__(self) -> str:
        return str(self.value)
    
    def __hash__(self) -> int:
        return hash(self.value.uid)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and self.value.uid == other.value.uid
    
    @property
    def gen(self) -> list[Node]:
        alpha: list[Node] = []
        root: Node = self
        while True:
            alpha.append(root)
            try:
                root = root.parent
            except AttributeError:
                break
        return alpha
    
    def add_child(self, value: Station) -> Node:
        child = Node(value)
        child.parent = self
        return child


class Config:

    STATIONS_FILE: str = "data/stations.csv"
    LINES_FILE: str = "data/lines.csv"
    TICKETS_FILE: str = "data/tickets.csv"
    DELIMITER: str = ","
    LIST_DELIMITER: str = "$"
    NEWLINE: str = ""


class Menu:

    def __init__(self) -> None:
        self.functions: dict[int, Callable[[], None]]  = {}
        self.options: dict[int, str] = {
            1: "Purchase Tickets",
            2: "View Tickets",
            3: "Delete Tickets",
            0: "Exit"
        }
        self.functions[1] = self.buy_tickets
        self.functions[2] = self.view_tickets
        self.functions[3] = self.remove_tickets
        self.functions[0] = self.exit

    def menu(self) -> None:
        while True:
            self.clear()
            print("\n=============[ MAIN MENU ]=============\n")
            for number, option in self.options.items():
                print(f'[{number}] >>> {option}')
            try:
                choice: int = int(input("\nEnter Option ID: "))
                if choice not in self.functions:
                    raise ValueError
            except ValueError:
                print("Not a valid option!\nTry Again...")
                continue
            func = self.functions.get(choice)
            if func:
                func()
    
    def view_tickets(self) -> None:
        self.clear()
        print("\n=============[ TICKET VIEWING ]=============\n")
        Ticket.display()
        input("\nPress ENTER to finish viewing...")
        
    def buy_tickets(self) -> None:
        self.clear()
        print("\n=============[ TICKET PURCHASE ]=============\n")
        Station.display()
        print()
        start_uid: int = self.input_station_id("starting")
        stop_uid: int = self.input_station_id("destination")
        while start_uid == stop_uid:
            print("\nStarting and Destination cannot be the same!\nTry Again...\n")
            stop_uid: int = self.input_station_id("destination")
            continue
        self.confirm_purchase(start_uid, stop_uid)
    
    def confirm_purchase(self, start_uid: int, stop_uid: int) -> None:
        print("\n=============[ CONFIRMATION ]=============\n")
        path: tuple[Station, ...] = Station.__sub__(Station.from_uid(start_uid), Station.from_uid(stop_uid))
        price: int = (len(path) - 1) * 100
        route: str = ""
        for i in range(len(path)):
            if i == 0:
                route += path[i].name
            else:
                route += " => " + path[i].name
        while True:
            try:
                print(f'Starting: {Station.from_uid(start_uid)}\nDestination: {Station.from_uid(stop_uid)}\nRoute: {route}\nPrice: ${price}')
                choice = input("Purchase this ticket? (y/n)\n").strip().lower()
                match choice:
                    case "y":
                        Ticket.buy(start_uid, stop_uid, path)
                        return
                    case "n":
                        return
                    case _:
                        raise ValueError
            except ValueError:
                print("\nError!\nTry again...")
                continue

    def remove_tickets(self) -> None:
        self.clear()
        print("\n=============[ TICKET REMOVAL ]=============\n")
        Ticket.display()
        choice: str = input("\nEnter Ticket ID: ")
        if Ticket.remove(choice):
            print(f'\nTicket with ID: {choice} has been deleted!')
        else:
            print("\nInvalid Ticket ID!")

    @staticmethod
    def exit() -> None:
        Ticket.save()
        sys.exit(0)

    @staticmethod
    def input_station_id(prompt: str) -> int:
        while True:
            try:
                uid = int(input(f'Enter {prompt} Station ID: '))
                if uid not in Station.stations:
                    raise ValueError
                return uid
            except ValueError:
                print("\nNot a valid Station ID!\nTry Again...\n")
                continue
    
    @staticmethod
    def clear():
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception:
            print("\033[H\033[J", end="")


class Station:
    
    stations: dict[int, Station] = {}

    def __init__(self, uid: int, name: str, neighbours: tuple[Station, ...]) -> None:
        self.uid: int = uid
        self.name: str = name
        self.neighbours: tuple[Station, ...] = neighbours

    def __repr__(self) -> str:
        return self.name
    
    def __sub__(self, other: Station) -> tuple[Station, ...]:
        visited: set[int] = {self.uid}
        queue: deque[Node] = deque([Node(self)])
        while queue:
            node: Node = queue.popleft()
            if node.value.uid == other.uid:
                path: list[Node] = node.gen
                path.reverse()
                return tuple(item.value for item in path)
            visited.add(node.value.uid)
            for neighbour in node.value.neighbours:
                if neighbour.uid not in visited:
                    visited.add(neighbour.uid)
                    queue.append(node.add_child(neighbour))
        return tuple()

    @classmethod
    def load(cls) -> None:
        try:
            temp: list[tuple[int, str]] = []
            with open(Config.STATIONS_FILE, "r", newline=Config.NEWLINE) as file:
                reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                for row in reader:
                    cls.stations[int(row["uid"])] = Station(int(row["uid"]), row["name"], tuple())
                    temp.append((int(row["uid"]), row["neighbours"]))
                for temp_uid, temp_neighbours in temp:
                    cls.stations[temp_uid].neighbours = cls.from_str(temp_neighbours)
        except (FileNotFoundError, IOError, csv.Error, KeyError) as err:
            Ticket.save()
            raise RuntimeError(f'Error loading {Config.STATIONS_FILE}: {err}')

    @classmethod
    def display(cls) -> None:
        for line in Line.lines:
            print(f'\n------------ <{line.name}> ------------\n')
            for station in line.stations:
                print(f'  [{station.uid}] >>> {station.name}')

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
            Ticket.save()
            raise RuntimeError(f'Error loading {Config.LINES_FILE}: {err}')


class Ticket:

    tickets: dict[str, Ticket] = {}

    def __init__(self, uid: str, start_uid: int, stop_uid: int, path: tuple[Station, ...]) -> None:
        self.uid: str = uid
        self.start_uid: int = start_uid
        self.stop_uid: int = stop_uid
        self.path: tuple[Station, ...] = path
        self.price: int = (len(self.path) - 1) * 3

    def __repr__(self) -> str:
        return self.uid
    
    @classmethod
    def load(cls) -> None:
        try:
            with open(Config.TICKETS_FILE, "r") as file:
                reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                for row in reader:
                    cls.tickets[row["uid"]] = Ticket(row["uid"], int(row["start_uid"]), int(row["stop_uid"]), Station.from_str(row["path"]))
        except (FileNotFoundError, IOError, csv.Error, KeyError) as err:
            raise RuntimeError(f'Error loading {Config.TICKETS_FILE}: {err}')

    @classmethod
    def buy(cls, start_uid: int, stop_uid: int, path: tuple[Station, ...]) -> None:
        uid: str = cls.create_uid()
        cls.tickets[uid] = Ticket(uid, start_uid, stop_uid, path)
            
    @classmethod
    def display(cls) -> None:
        for uid, ticket in cls.tickets.items():
            print(f'[{uid}] >>> {Station.from_uid(ticket.start_uid)} => {Station.from_uid(ticket.stop_uid)}')
    
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
            raise RuntimeError(f'Error writing to {Config.TICKETS_FILE}: {err}')

    @staticmethod
    def create_uid() -> str:
        uid: str = uuid.uuid4().hex
        while uid in Ticket.tickets:
            uid = uuid.uuid4().hex
        return uid


def main():
    try:
        Station.load()
        Line.load()
        Ticket.load()
    except RuntimeError as err:
        print(f'Error: {err}')
        return

    menu: Menu = Menu()
    menu.menu()

if __name__ == "__main__":
    main()
