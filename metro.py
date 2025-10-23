import os
import csv
import time
import secrets


class Station:
    
    stations: dict = {}

    def __init__(self, uid: int):
        self.uid = uid

    def __repr__(self) -> str:
        return str(self.name)

    @property
    def name(self):
        with open("stations.csv", "r", newline="") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                if int(row["uid"]) == self.uid:
                    return row["name"]
                
    @property
    def neighbours(self):
        with open("stations.csv", "r", newline="") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                if int(row["uid"]) == self.uid:
                    return row["neighbours"].split("$")
                
    @classmethod
    def load(cls):
        with open("stations.csv", "r", newline="") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                cls.stations[int(row["uid"])] = Station(int(row["uid"]))

    @classmethod
    def display(cls):
        for station in cls.stations:
            print(f'[{station}]: {cls.stations[station].name}')

    @classmethod
    def name_from_uid(cls, uid: int):
        for station in cls.stations:
            if cls.stations[station].uid == uid:
                return cls.stations[station].name


class Line:

    lines: list = []

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name
                
    @property
    def stations(self) -> list:
        with open("lines.csv", "r", newline="") as file:
            reader = csv.DictReader(file, delimiter = ",")
            for row in reader:
                if row["name"] == self.name:
                    return row["stations"].split("$")
            else:
                return []

    @classmethod
    def load(cls):
        with open("lines.csv", "r", newline="") as file:
            reader = csv.DictReader(file, delimiter = ",")
            for row in reader:
                cls.lines.append(Line(row["name"]))


class Ticket:

    tickets: list = []

    def __init__(self, uid):
        self.uid = uid

    def __repr__(self):
        return self.uid

    @property
    def start_uid(self):
        with open("tickets.csv", "r", newline="") as file:
            reader = csv.DictReader(file, delimiter = ",")
            for row in reader:
                if row["uid"] == self.uid:
                    return row["start_uid"]
                
    @property
    def stop_uid(self):
        with open("tickets.csv", "r") as file:
            reader = csv.DictReader(file, delimiter = ",")
            for row in reader:
                if row["uid"] == self.uid:
                    return row["stop_uid"]
                
    @classmethod
    def load(cls):
        with open("tickets.csv", "r") as file:
            reader = csv.DictReader(file, delimiter = ",")
            for row in reader:
                cls.tickets.append(Ticket(row["uid"]))

    @classmethod
    def calc_price(cls, start_uid: int, stop_uid: int):
        pass

    @classmethod
    def buy(cls, start_uid: int, stop_uid: int, newline=""):
        ticket = [secrets.token_hex(8), start_uid, stop_uid]
        with open("tickets.csv", "a", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(ticket)
        cls.tickets.append(Ticket(ticket[0]))
            
    @classmethod
    def display(cls):
        for ticket in cls.tickets:
            print(ticket)
            print(f'[{ticket.uid}]: {Station.name_from_uid(ticket.start_uid)} => {Station.name_from_uid(ticket.stop_uid)}')
    
    @classmethod
    def remove(cls, uid):
        for ticket in cls.tickets:
            if ticket.uid == uid:
                cls.tickets.remove(ticket)
        with open("tickets.csv", "w", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(["uid", "start_uid", "stop_uid"])
            for ticket in cls.tickets:
                writer.writerow([ticket.uid, ticket.start_uid, ticket.stop_uid])


def close():
    os.system('cls' if os.name == 'nt' else 'clear')
    os._exit(0)

def remove():
    os.system('cls' if os.name == 'nt' else 'clear')
    Ticket.display()
    choice = input("Enter the uid of the ticket to remove:\t")
    Ticket.remove(choice)
    print(f'Ticket with uid: {choice} has been deleted')

def buy():
    start_uid: int
    stop_uid: int
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        Station.display()
        try:
            start_uid = int(input("Enter starting Station uid:\t"))
            if start_uid not in Station.stations.keys():
                raise ValueError
            break
        except ValueError:
            print("Not a valuid Station uid!\nTry Again...")
            time.sleep(2)
            continue
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        Station.display()
        try:
            stop_uid = int(input("Enter destination Station uid:\t"))
            if stop_uid not in Station.stations.keys():
                raise ValueError
            break
        except ValueError:
            print("Not a valuid Station uid!\nTry Again...")
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
            print(f'Start:\t{Station.name_from_uid(start_uid)}\nDestination:\t{Station.name_from_uid(stop_uid)}\nThe price will be ${price}')
            choice = input("Do you wish to purchase this ticket? (Y/N)").lower()
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
        print("""MAIN MENU
              --------------
              1 => View your tickets
              2 => Buy tickets
              3 => Remove tickets
              0 => Exit
              """)
        try:
            choice = int(input("Enter option uid:\t"))
            if choice not in menu:
                raise ValueError
        except ValueError:
            print("Not a valuid option!\nTry Again...")
            time.sleep(2)
            continue
        func = menu.get(choice)
        if func:
            func()

if __name__ == "__main__":
    main()