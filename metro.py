from __future__ import annotations
from typing import Callable

import sys
import csv
import string
import random
from collections import deque


class Config:

    STATIONS_FILE: str = "data/stations.csv"
    LINES_FILE: str = "data/lines.csv"
    TICKETS_FILE: str = "data/tickets.csv"
    DELIMITER: str = ","
    LIST_DELIMITER: str = "|"
    NEWLINE: str = ""
    PRICE_FACTOR: int = 3
    PASS_CHARS: tuple[str, ...] = tuple(string.ascii_uppercase + string.digits)
    ANSI: dict[str, str] = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "grey": "\033[90m",
        "orange": "\033[93m",
        "pink": "\033[95m",
        "clear": "\033[H",
        "home": "\033[J"
    }


class Menu:

    clear: str = Config.ANSI["clear"] + Config.ANSI["home"]

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
            print(f'{self.clear}{Config.ANSI["bold"]}=============[ MAIN MENU ]============={Config.ANSI["reset"]}\n')
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
        print(f'{self.clear}{Config.ANSI["bold"]}=============[ TICKET VIEWING ]============={Config.ANSI["reset"]}')
        print(Ticket.display())
        try:
            choice: str = input("\nEnter Ticket ID: ")
            if choice not in Ticket.tickets:
                raise Exception
            print(Ticket.tickets[choice].detail)
            print("\n" + Line.guide(Ticket.tickets[choice].path))
            input("Press ENTER to continue...")
        except Exception:
            pass
        
    def buy_tickets(self) -> None:
        print(f'{self.clear}{Config.ANSI["bold"]}=============[ TICKET PURCHASE ]============={Config.ANSI["reset"]}')
        print(Station.display())
        print()
        start_uid: int = self.input_station_id("starting")
        if not start_uid:
            return
        stop_uid: int = self.input_station_id("destination")
        if not stop_uid:
            return
        while start_uid == stop_uid:
            print("\nStarting and Destination cannot be the same!\nTry Again...\n")
            stop_uid: int = self.input_station_id("destination")
            if not stop_uid:
                return
            continue
        self.confirm_purchase(start_uid, stop_uid)
    
    def confirm_purchase(self, start_uid: int, stop_uid: int) -> None:
        print(f'{self.clear}{Config.ANSI["bold"]}=============[ CONFIRMATION ]============={Config.ANSI["reset"]}')
        path: tuple[Station, ...] = Station.__sub__(Station.from_uid(start_uid), Station.from_uid(stop_uid))
        price: int = (len(path) - 1) * Config.PRICE_FACTOR
        route: str = ""
        for i in range(len(path)):
            if i == 0:
                route += path[i].name
            else:
                route += " => " + path[i].name
        while True:
            try:
                print(f'Starting: {Station.from_uid(start_uid)}\nDestination: {Station.from_uid(stop_uid)}\nRoute: {route}\nPrice: ${price}')
                choice = input("\nPurchase this ticket? (y/n)\n").strip().lower()
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
        print(f'{self.clear}{Config.ANSI["bold"]}=============[ TICKET REMOVAL ]============={Config.ANSI["reset"]}')
        print(Ticket.display())
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
            choice: str = input(f'Enter {prompt} Station ID: ')
            if choice == "":
                return 0
            else:
                try:
                    uid: int = int(choice)
                    if uid not in Station.stations:
                        print("\nNot a valid Station!\nTry Again...\n")
                        continue
                    return uid
                except ValueError:
                    uid: int = Station.exists(choice)
                    if not uid:
                        print("\nNot a valid Station!\nTry Again...\n")
                        continue
                    return uid


class Station:
    
    stations: dict[int, Station] = {}
    display_text: str = ""

    def __init__(self, uid: int, name: str) -> None:
        self.uid: int = uid
        self.name: str = name
        self.neighbours: frozenset[Station] = frozenset()
        self.lines: set[str] = set()

    def __repr__(self) -> str:
        return self.name
    
    def __hash__(self) -> int:
        return hash(self.uid)
    
    def __eq__(self, value: object) -> bool:
        return isinstance(value, self.__class__) and self.uid == value.uid
    
    def __sub__(self, other: Station) -> tuple[Station, ...]:
        visited: set[int] = {self.uid}
        queue: deque[int] = deque([self.uid])
        parents: dict[int, int] = {}
        while queue:
            station: Station = self.from_uid(queue.popleft())
            if station.uid == other.uid:
                path: list[int] = []
                temp: int = station.uid
                while temp in parents:
                    path.append(temp)
                    temp = parents[temp]
                path.append(self.uid)
                return tuple([self.from_uid(item) for item in path])
            for neighbour in station.neighbours:
                if neighbour.uid not in visited:
                    visited.add(neighbour.uid)
                    parents[neighbour.uid] = station.uid
                    queue.append(neighbour.uid)
        return tuple()

    @classmethod
    def load(cls) -> None:
        try:
            temp: set[tuple[int, str]] = set()
            with open(Config.STATIONS_FILE, "r", newline=Config.NEWLINE) as file:
                reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                for row in reader:
                    cls.stations[int(row["uid"])] = Station(int(row["uid"]), row["name"])
                    temp.add((int(row["uid"]), row["neighbours"]))
                for temp_uid, temp_neighbours in temp:
                    cls.stations[temp_uid].neighbours = frozenset(cls.split(temp_neighbours))
        except (FileNotFoundError, IOError, csv.Error, KeyError) as err:
            raise RuntimeError(f'Error loading {Config.STATIONS_FILE}: {err}')

    @classmethod
    def display(cls) -> str:
        if cls.display_text == "":
            out: str = ""
            for line, stations in Line.lines.items():
                out += f'\n{Config.ANSI["underline"]}{line}\n{Config.ANSI["reset"]}\n'
                for station in stations:
                    out += f' [{station.uid}] {station.name}\n'
            return out
        else:
            return cls.display_text

    @classmethod
    def from_uid(cls, uid: int) -> Station:
        return cls.stations[uid]
    
    @classmethod
    def exists(cls, name: str) -> int:
        for uid, station in cls.stations.items():
            if station.name.lower() == name.lower():
                return uid
        else:
            return 0
    
    @classmethod
    def split(cls, prompt: str) -> tuple[Station, ...]:
        arr: list[int] = [int(item) for item in prompt.split(Config.LIST_DELIMITER)]
        return tuple([cls.from_uid(item) for item in arr])


class Line:

    lines: dict[str, tuple[Station, ...]] = {}

    @classmethod
    def load(cls) -> None:
        try:
            with open(Config.LINES_FILE, "r", newline=Config.NEWLINE) as file:
                reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                for row in reader:
                    stations: tuple[Station, ...] = Station.split(row["stations"])
                    cls.lines[row["name"]] = stations
                    [Station.stations[station.uid].lines.add(row["name"]) for station in stations]
        except (FileNotFoundError, IOError, csv.Error, KeyError) as err:
            raise RuntimeError(f'Error loading {Config.LINES_FILE}: {err}')
    
    @classmethod
    def get_line(cls, x: Station, y: Station) -> str:
        x_lines: set[str] = x.lines
        y_lines: set[str] = y.lines
        intersection: set[str] = x_lines & y_lines
        return intersection.pop()
        
    @classmethod
    def guide(cls, path: tuple[Station, ...]) -> str:
        instructions: str = ""
        for i in range(len(path)):
            if i == 0:
                instructions += path[i].name
            else:
                if i < len(path) - 1:
                    curr_line: str = cls.get_line(path[i], path[i - 1])
                    next_line: str = cls.get_line(path[i], path[i + 1])
                    instructions += " => " + path[i].name
                    if not (curr_line == next_line):
                        instructions += f'\nChange lines from {curr_line} to {next_line}...\n'
                        instructions += path[i].name
                else:
                    instructions += " => " + path[i].name
        instructions += "\n"
        return instructions


class Ticket:

    tickets: dict[str, Ticket] = {}

    def __init__(self, uid: str, start_uid: int, stop_uid: int, path: tuple[Station, ...]) -> None:
        self.uid: str = uid
        self.start_uid: int = start_uid
        self.stop_uid: int = stop_uid
        self.path: tuple[Station, ...] = path

    def __repr__(self) -> str:
        return self.uid
    
    @property
    def detail(self) -> str:
        details: str = ""
        details += f'Ticket ID: {self.uid}\n'
        details += f'Starting: {Station.from_uid(self.start_uid).name}\n'
        details += f'Destination: {Station.from_uid(self.stop_uid).name}\n'
        return details
    
    @property
    def price(self) -> int:
        return (len(self.path) - 1) * Config.PRICE_FACTOR
    
    @classmethod
    def load(cls) -> None:
        try:
            with open(Config.TICKETS_FILE, "r") as file:
                reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                for row in reader:
                    cls.tickets[row["uid"]] = Ticket(row["uid"], int(row["start_uid"]), int(row["stop_uid"]), Station.split(row["path"]))
        except (FileNotFoundError, IOError, csv.Error, KeyError) as err:
            raise RuntimeError(f'Error loading {Config.TICKETS_FILE}: {err}')

    @classmethod
    def buy(cls, start_uid: int, stop_uid: int, path: tuple[Station, ...]) -> None:
        uid: str = cls.create_uid()
        cls.tickets[uid] = Ticket(uid, start_uid, stop_uid, path)
            
    @classmethod
    def display(cls) -> str:
        out: str = ""
        for uid, ticket in cls.tickets.items():
            out += f'[{uid}] {Station.from_uid(ticket.start_uid)} => {Station.from_uid(ticket.stop_uid)}\n'
        return out
    
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
                writer.writerow(["uid", "start_uid", "stop_uid", "path"])
                for uid, ticket in cls.tickets.items():
                    path: str = Config.LIST_DELIMITER.join(map(str, ticket.path))
                    writer.writerow([uid, ticket.start_uid, ticket.stop_uid, path])
        except (FileNotFoundError, IOError, csv.Error, KeyError) as err:
            raise RuntimeError(f'Error writing to {Config.TICKETS_FILE}: {err}')

    @classmethod
    def create_uid(cls) -> str:
        uid: str = "".join(random.choices(Config.PASS_CHARS, k=3)) + "-" + "".join(random.choices(Config.PASS_CHARS, k=3))
        while uid in cls.tickets:
            uid = cls.create_uid()
        return uid
    
def cache() -> None:
    Station.load()
    Line.load()
    Station.display_text = Station.display()
    Ticket.load()

def main() -> None:
    try:
        cache()
    except RuntimeError as err:
        print(f'Error: {err}')
        return
    menu: Menu = Menu()
    menu.menu()

if __name__ == "__main__":
    main()
