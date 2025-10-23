import os
import csv
import secrets


class Station:
    
    stations: dict = {}

    def __init__(self, id: int):
        self.id = id

    def __repr__(self) -> str:
        return str(self.name)

    @property
    def name(self):
        with open("stations.csv", "r") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                if int(row["id"]) == self.id:
                    return row["name"]
                
    @property
    def neighbours(self):
        with open("stations.csv", "r") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                if int(row["id"]) == self.id:
                    return row["neighbours"].split("$")
                
    @classmethod
    def load(cls):
        with open("stations.csv", "r") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                cls.stations[int(row["id"])] = Station(int(row["id"]))

    @classmethod
    def display(cls):
        for station in cls.stations:
            print(f'[{station}]: {cls.stations[station].name}')

    @classmethod
    def name_from_id(cls, id: int):
        for station in cls.stations:
            if station.id == id:
                return station.name


class Line:

    lines: list = []

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name
                
    @property
    def stations(self) -> list:
        with open("lines.csv", "r") as file:
            reader = csv.DictReader(file, delimiter = ",")
            for row in reader:
                if row["name"] == self.name:
                    return row["stations"].split("$")
            else:
                return []

    @classmethod
    def load(cls):
        with open("lines.csv", "r") as file:
            reader = csv.DictReader(file, delimiter = ",")
            for row in reader:
                cls.lines.append(Line(row["name"]))


class Ticket:

    tickets: list = []

    def __init__(self, id: int):
        self.id = id

    def __repr_(self):
        return self.id

    @property
    def start_id(self):
        with open("tickets.csv", "r") as file:
            reader = csv.DictReader(file, delimiter = ",")
            for row in reader:
                if row["id"] == self.id:
                    return row["start_id"]
                
    @property
    def stop_id(self):
        with open("tickets.csv", "r") as file:
            reader = csv.DictReader(file, delimiter = ",")
            for row in reader:
                if row["id"] == self.id:
                    return row["stop_id"]
                
    @classmethod
    def load(cls):
        with open("lines.csv", "r") as file:
            reader = csv.DictReader(file, delimiter = ",")
            for row in reader:
                cls.tickets.append(Ticket(int(row["id"])))

    @classmethod
    def calc_price(cls, start_id: int, stop_id: int):
        pass

    @classmethod
    def buy(cls, start_id: int, stop_id: int):
        ticket = [secrets.token_hex(8), start_id, stop_id]
        with open("tickets.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(ticket)
        cls.tickets.append(ticket)
            
    @classmethod
    def display(cls):
        for ticket in cls.tickets:
            print(f'[{ticket.id}]: {Station.name_from_id(ticket.start_id)} => {Station.name_from_id(ticket.stop_id)}')
    
    @classmethod
    def remove(cls, id: int):
        for ticket in cls.tickets:
            if ticket.id == id:
                cls.tickets.remove(ticket)


def close():
    os._exit(0)

def remove():
    os.system('cls' if os.name == 'nt' else 'clear')
    Ticket.display()
    choice: int = int(input("Enter the ID of the ticket to remove:\t"))
    Ticket.remove(choice)
    print(f'Ticket with ID: {choice} has been deleted')

def buy():
    start_id: int
    stop_id: int
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        Station.display()
        try:
            start_id = int(input("Enter starting Station ID:\t"))
            if start_id not in Station.stations.keys():
                raise ValueError
            break
        except ValueError:
            print("Not a valid Station ID!\nTry Again...")
            continue
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        Station.display()
        try:
            stop_id = int(input("Enter destination Station ID:\t"))
            if stop_id not in Station.stations.keys():
                raise ValueError
            break
        except ValueError:
            print("Not a valid Station ID!\nTry Again...")
            continue
    if start_id == stop_id:
            print("Start and Destination cannot be the same!\nTry Again...")
            buy()
            return
    price = Ticket.calc_price(start_id, stop_id)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            print(f'Start:\t{Station.name_from_id(start_id)}\nDestination:\t{Station.name_from_id(stop_id)}\nThe price will be ${price}')
            choice = input("Do you wish to purchase this ticket? (Y/N)").lower()
            if choice == "y":
                Ticket.buy(start_id, stop_id)
                return
            elif choice == "n":
                return
            else:
                raise ValueError
        except ValueError:
            print("Error!\nTry again...")
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
    while True:
        print("""MAIN MENU
              --------------
              1 => View your tickets
              2 => Buy tickets
              3 => Remove tickets
              0 => Exit
              """)
        try:
            choice = int(input("Enter option ID:\t"))
            if choice not in menu:
                raise ValueError
        except ValueError:
            print("Not a valid option!\nTry Again...")
            continue
        func = menu.get(choice)
        if func:
            func()

if __name__ == "__main__":
    main()