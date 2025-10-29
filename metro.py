from __future__ import annotations
from typing import Callable, ClassVar

import os
import sys
import csv
import time
import string
import random
from collections import deque


class Config:

    DELAY: ClassVar[float] = 1.2
    STATIONS_FILE: ClassVar[str] = "data/stations.csv"
    LINES_FILE: ClassVar[str] = "data/lines.csv"
    TICKETS_FILE: ClassVar[str] = "data/tickets.csv"
    DELIMITER: ClassVar[str] = ","
    LIST_DELIMITER: ClassVar[str] = "|"
    NEWLINE: ClassVar[str] = ""
    PRICE_FACTOR: ClassVar[int] = 3
    PASS_CHARS: ClassVar[str] = string.ascii_uppercase + string.digits
    ANSI: ClassVar[dict[str, str]] = {
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
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "orange": "\033[93m",
        "bright_blue": "\033[94m",
        "pink": "\033[95m",
        "bright_cyan": "\033[96m",
        "clear": "\033[H",
        "clear_scrollback": "\033[3J",
        "home": "\033[J"
    }
    LINE_COLORS: ClassVar[dict[str, str]] = {
        "Red Line": ANSI["bright_red"],
        "Yellow Line": ANSI["orange"],
        "Blue Line": ANSI["bright_blue"],
        "Green Line": ANSI["bright_green"],
        "Violet Line": ANSI["magenta"],
        "Pink Line": ANSI["pink"],
        "Magenta Line": ANSI["red"],
        "Grey Line": ANSI["grey"],
        "Airport Express": ANSI["bright_cyan"]
    }


class Menu:

    def __init__(self) -> None:
        self.functions: dict[int, Callable[[], None]]  = {}
        self.options: dict[int, str] = {
            1: "View Metro Stations",
            2: "Purchase Tickets",
            3: "View Tickets",
            4: "Delete Tickets",
            0: "Exit"
        }
        self.functions[1] = self.view_stations
        self.functions[2] = self.buy_tickets
        self.functions[3] = self.view_tickets
        self.functions[4] = self.remove_tickets
        self.functions[0] = self.exit

    @property
    def clear(self) -> str:
        if os.name == "nt":
            os.system("cls")
            return ""
        else:
            return Config.ANSI["clear"] + Config.ANSI["home"] + Config.ANSI["clear_scrollback"]

    def menu(self) -> None:
        while True:
            print(self.clear)
            print(f'{Config.ANSI["bold"]}=============[ MAIN MENU ]============={Config.ANSI["reset"]}\n')
            for number, option in self.options.items():
                print(f'[{number}] {option}')
            choice: str = input("\nEnter Option ID: ")
            if choice.isdigit() and int(choice) in self.functions:
                func = self.functions.get(int(choice))
                if func:
                    func()
            else:
                print("Not a valid Option ID!\nTry Again...")
                time.sleep(Config.DELAY)

    def view_stations(self) -> None:
        print(self.clear)
        print(f'{Config.ANSI["bold"]}=============[ METRO STATIONS ]============={Config.ANSI["reset"]}\n')
        print(Station.display())
        input("Press ENTER to continue...")
    
    def view_tickets(self) -> None:
        while True:
            print(self.clear)
            print(f'{Config.ANSI["bold"]}=============[ TICKETS ]============={Config.ANSI["reset"]}\n')
            print(Ticket.display())
            choice: str = input("Enter Ticket ID (ENTER -> abort): ")
            if choice == "":
                return
            elif choice in Ticket.tickets:
                print(self.clear)
                print(Ticket.tickets[choice].detail)
                print(Line.guide(Ticket.tickets[choice].path))
                input("Press ENTER to continue...")
                return
            else:
                print("Invalid Ticket ID\nTry Again...")
                time.sleep(Config.DELAY)
        
    def buy_tickets(self) -> None:
        print(self.clear)
        print(f'{Config.ANSI["bold"]}=============[ TICKET PURCHASE ]============={Config.ANSI["reset"]}\n')
        print(Station.display(), end="\n\n")
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
        while True:
            print(self.clear)
            print(f'{Config.ANSI["bold"]}=============[ CONFIRMATION ]============={Config.ANSI["reset"]}\n')
            ticket: Ticket = Ticket(Ticket.create_uid(), start_uid, stop_uid, ())
            ticket.path = Station.from_uid(stop_uid) - Station.from_uid(start_uid)
            print(f'Starting: {Station.from_uid(ticket.start_uid)}\nDestination: {Station.from_uid(ticket.stop_uid)}\nPrice: ${ticket.price}')
            choice = input("\nPurchase this ticket? (y/n)\n").strip().lower()
            match choice:
                case "y":
                    Ticket.buy(ticket)
                    return
                case "n":
                    return
                case _:
                    print("\nNot a valid option!\nTry again...")
                    time.sleep(Config.DELAY)

    def remove_tickets(self) -> None:
        while True:
            print(self.clear)
            print(f'{Config.ANSI["bold"]}=============[ TICKET REMOVAL ]============={Config.ANSI["reset"]}\n')
            print(Ticket.display())
            choice: str = input("Enter Ticket ID (ENTER -> abort): ")
            if choice == "":
                return
            elif Ticket.remove(choice):
                print(f'\nTicket with ID: {choice} has been deleted!')
                time.sleep(Config.DELAY)
            else:
                print("\nInvalid Ticket ID!")
                time.sleep(Config.DELAY)

    @staticmethod
    def exit() -> None:
        Ticket.save()
        sys.exit(0)

    @staticmethod
    def input_station_id(prompt: str) -> int:
        while True:
            choice: str = input(f'Enter {prompt} Station ID (ENTER -> abort): ')
            if choice == "":
                return 0
            elif choice.isdigit() and int(choice) in Station.stations:
                return int(choice)
            else:
                uid: int = Station.exists(choice)
                if uid:
                    return uid
                else:
                    print("\nNot a valid Station!\nTry Again...\n")
                    continue
                    


class Station:
    
    stations: ClassVar[dict[int, Station]] = {}
    name_to_uid: ClassVar[dict[str, int]] = {}
    display_text: ClassVar[str] = ""

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
                    cls.name_to_uid[row["name"]] = int(row["uid"])
                    temp.add((int(row["uid"]), row["neighbours"]))
                for temp_uid, temp_neighbours in temp:
                    cls.stations[temp_uid].neighbours = frozenset(cls.split(temp_neighbours))
        except FileNotFoundError:
            raise RuntimeError(f'Error: {Config.STATIONS_FILE} not found')
        except PermissionError:
            raise RuntimeError(f'Error: Lacking permission to write to {Config.STATIONS_FILE}')
        except (ValueError, csv.Error, KeyError):
            raise RuntimeError(f'Error: Data format error in {Config.STATIONS_FILE}')
        except (IOError, Exception):
            raise RuntimeError(f'Error: Problem loading {Config.STATIONS_FILE}')

    @classmethod
    def display(cls) -> str:
        if cls.display_text == "":
            out: str = ""
            for line, stations in Line.lines.items():
                out += f'\n {Config.LINE_COLORS[line]}{Config.ANSI["underline"]}{line}\n{Config.ANSI["reset"]}'
                for station in stations:
                    out += f' [{station.uid}] {Config.LINE_COLORS[line]}{station.name}{Config.ANSI["reset"]}\n'
            cls.display_text = out
        return cls.display_text

    @classmethod
    def from_uid(cls, uid: int) -> Station:
        return cls.stations[uid]
    
    @classmethod
    def exists(cls, name: str) -> int:
        if name in cls.name_to_uid:
            return cls.name_to_uid[name]
        return 0
    
    @classmethod
    def split(cls, prompt: str) -> tuple[Station, ...]:
        arr: list[int] = [int(item) for item in prompt.split(Config.LIST_DELIMITER)]
        return tuple([cls.from_uid(item) for item in arr])


class Line:

    lines: ClassVar[dict[str, tuple[Station, ...]]] = {}

    @classmethod
    def load(cls) -> None:
        try:
            with open(Config.LINES_FILE, "r", newline=Config.NEWLINE) as file:
                reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                for row in reader:
                    stations: tuple[Station, ...] = Station.split(row["stations"])
                    cls.lines[row["name"]] = stations
                    for station in stations:
                        Station.stations[station.uid].lines.add(row["name"])
        except FileNotFoundError:
            raise RuntimeError(f'Error: {Config.LINES_FILE} not found')
        except PermissionError:
            raise RuntimeError(f'Error: Lacking permission to write to {Config.LINES_FILE}')
        except (ValueError, csv.Error, KeyError):
            raise RuntimeError(f'Error: Data format error in {Config.LINES_FILE}')
        except (IOError, Exception):
            raise RuntimeError(f'Error: Problem loading {Config.LINES_FILE}')
    
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
                next_line: str = cls.get_line(path[i], path[i + 1])
                instructions += Config.LINE_COLORS[next_line] + path[i].name + Config.ANSI["reset"]
            else:
                curr_line: str = cls.get_line(path[i], path[i - 1])
                instructions += " => " + Config.LINE_COLORS[curr_line] + path[i].name  + Config.ANSI["reset"]
                if i < len(path) - 1:
                    next_line: str = cls.get_line(path[i], path[i + 1])
                    if not (curr_line == next_line):
                        instructions += f'\nChange lines from {Config.LINE_COLORS[curr_line]}{curr_line}{Config.ANSI["reset"]} to {Config.LINE_COLORS[next_line]}{next_line}{Config.ANSI["reset"]}...\n'
                        instructions += Config.LINE_COLORS[next_line] + path[i].name  + Config.ANSI["reset"]
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
            with open(Config.TICKETS_FILE, "r", newline=Config.NEWLINE) as file:
                reader = csv.DictReader(file, delimiter=Config.DELIMITER)
                for row in reader:
                    cls.tickets[row["uid"]] = Ticket(row["uid"], int(row["start_uid"]), int(row["stop_uid"]), Station.split(row["path"]))
        except FileNotFoundError:
            raise RuntimeError(f'Error: {Config.TICKETS_FILE} not found')
        except (ValueError, csv.Error, KeyError):
            raise RuntimeError(f'Error: Data format error in {Config.TICKETS_FILE}')
        except (IOError, Exception):
            raise RuntimeError(f'Error: Problem loading {Config.TICKETS_FILE}')

    @classmethod
    def buy(cls, ticket: Ticket) -> None:
        cls.tickets[ticket.uid] = ticket
            
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
                    path: str = Config.LIST_DELIMITER.join([str(item.uid) for item in ticket.path])
                    writer.writerow([uid, ticket.start_uid, ticket.stop_uid, path])
        except FileNotFoundError:
            raise RuntimeError(f'Error: {Config.TICKETS_FILE} not found')
        except PermissionError:
            raise RuntimeError(f'Error: Lacking permission to write to {Config.TICKETS_FILE}')
        except (ValueError, csv.Error, KeyError):
            raise RuntimeError(f'Error: Data format error in {Config.TICKETS_FILE}')
        except (IOError, Exception):
            raise RuntimeError(f'Error: Problem loading {Config.TICKETS_FILE}')

    @classmethod
    def create_uid(cls) -> str:
        uid: str = "".join(random.choices(Config.PASS_CHARS, k=3)) + "-" + "".join(random.choices(Config.PASS_CHARS, k=3))
        while uid in cls.tickets:
            uid: str = "".join(random.choices(Config.PASS_CHARS, k=3)) + "-" + "".join(random.choices(Config.PASS_CHARS, k=3))
        return uid
    
def cache() -> None:
    Station.load()
    Line.load()
    Ticket.load()

def main() -> None:
    while True:
        try:
            cache()
            break
        except RuntimeError as err:
            print(Config.ANSI["red"] + str(err) + Config.ANSI["reset"])
            choice: str = input("Press ENTER to abort...\nEnter text to retry: ")
            if choice == "":
                return
            else:
                continue
    menu: Menu = Menu()
    menu.menu()

if __name__ == "__main__":
    main()
