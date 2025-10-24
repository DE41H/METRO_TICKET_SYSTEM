import os
import csv
import time
import uuid
import base64

STATIONS_FILE = "stations.csv"
LINES_FILE = "lines.csv"
TICKETS_FILE = "tickets.csv"
DELIMITER = ","
LIST_DELIMITER = "$"
NEWLINE = ""


class Station:
    
    stations: dict = {}

    def __init__(self, uid: int, name: str, neighbours: list):
        self.uid: int = uid
        self.name: str = name
        self.neighbours: list = neighbours

    def __repr__(self) -> str:
        return str(self.name)

    @classmethod
    def load(cls):
        with open(STATIONS_FILE, "r", newline=NEWLINE) as file:
            reader = csv.DictReader(file, delimiter=DELIMITER)
            for row in reader:
                cls.stations[int(row["uid"])] = Station(int(row["uid"]), row["name"], row["neighbours"].split(LIST_DELIMITER))

    @classmethod
    def display(cls):
        for station in cls.stations:
            print(f'[{station}]: {cls.stations[station].name}')

    @classmethod
    def from_uid(cls, uid: int) -> str:
        return cls.stations[int(uid)]


class Line:

    lines: list = []

    def __init__(self, name: str, stations: list):
        self.name = name
        self.stations: list = stations

    def __repr__(self):
        return self.name

    @classmethod
    def load(cls):
        with open(LINES_FILE, "r", newline=NEWLINE) as file:
            reader = csv.DictReader(file, delimiter=DELIMITER)
            for row in reader:
                cls.lines.append(Line(row["name"], row["stations"].split(LIST_DELIMITER)))


class Ticket:

    tickets: list = []

    def __init__(self, uid, start_uid, stop_uid):
        self.uid = uid
        self.start_uid: int = start_uid
        self.stop_uid: int = stop_uid

    def __repr__(self):
        return self.uid
                
    @classmethod
    def load(cls):
        with open(TICKETS_FILE, "r") as file:
            reader = csv.DictReader(file, delimiter=DELIMITER)
            for row in reader:
                cls.tickets.append(Ticket(row["uid"], int(row["start_uid"]), int(row["stop_uid"])))

    @classmethod
    def calc_price(cls, start_uid: int, stop_uid: int):
        pass

    @classmethod
    def buy(cls, start_uid: int, stop_uid: int):
        cls.tickets.append(Ticket(cls.create_uid(), start_uid, stop_uid))
            
    @classmethod
    def display(cls):
        for ticket in cls.tickets:
            print(f'[{ticket.uid}]: {Station.from_uid(ticket.start_uid)} => {Station.from_uid(ticket.stop_uid)}')
    
    @classmethod
    def remove(cls, uid):
        for ticket in cls.tickets:
            if ticket.uid == uid:
                cls.tickets.remove(ticket)

    @classmethod
    def save(cls):
        with open(TICKETS_FILE, "w", newline=NEWLINE) as file:
            writer = csv.writer(file, delimiter=DELIMITER)
            writer.writerow(["uid", "start_uid", "stop_uid"])
            for ticket in cls.tickets:
                writer.writerow([ticket, ticket.start_uid, ticket.stop_uid])

    @staticmethod
    def create_uid() -> str:
        uid = uuid.uuid4()
        uid = uid.bytes
        uid = base64.urlsafe_b64encode(uid).rstrip(b'=').decode('utf-8')
        return uid


def close():
    Ticket.save()
    os.system('cls' if os.name == 'nt' else 'clear')
    os._exit(0)

def remove():
    os.system('cls' if os.name == 'nt' else 'clear')
    Ticket.display()
    choice = input("Enter the ID of the ticket to remove: ")
    Ticket.remove(choice)
    print(f'Ticket with ID: {choice} has been deleted!')

def buy():
    start_uid: int
    stop_uid: int
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        Station.display()
        try:
            start_uid = int(input("Enter starting Station ID: "))
            if start_uid not in Station.stations.keys():
                raise ValueError
            break
        except ValueError:
            print("Not a valid Station ID!\nTry Again...")
            time.sleep(2)
            continue
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        Station.display()
        try:
            stop_uid = int(input("Enter destination Station ID: "))
            if stop_uid not in Station.stations.keys():
                raise ValueError
            break
        except ValueError:
            print("Not a valid Station ID!\nTry Again...")
            time.sleep(2)
            continue
    if start_uid == stop_uid:
            print("Start and Destination cannot be the same!\nTry Again...")
            time.sleep(2)
            return
    price = Ticket.calc_price(start_uid, stop_uid)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            print(f'Start: {Station.from_uid(start_uid)}\nDestination: {Station.from_uid(stop_uid)}\nThe price will be {price}$')
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
            time.sleep(2)
            continue
    

def view():
    os.system('cls' if os.name == 'nt' else 'clear')
    Ticket.display()
    input("Press enter to finish viewing...")


menu = {
    1: view,
    2: buy,
    3: remove,
    0: close
}


def main():
    Station.load()
    Line.load()
    Ticket.load()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("MAIN MENU\n--------------\n[1] => View your tickets\n[2] => Buy tickets\n[3] => Remove tickets\n[0] => Exit")
        try:
            choice = int(input("Enter Option ID: "))
            if choice not in menu:
                raise ValueError
        except ValueError:
            print("Not a valid option!\nTry Again...")
            time.sleep(2)
            continue
        func = menu.get(choice)
        if func:
            func()

if __name__ == "__main__":
    main()