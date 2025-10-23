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
    def buy(cls):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("TICKET PURCHASE\n----------------------------------------------------------\n\nChoose a starting station:")
        Station.display()
        try:
            start_id = int(input("Enter Station ID:\t"))
            if start_id not in Station.stations.keys():
                raise ValueError
        except ValueError:
            print("Not a valid Station ID!\nTry Again...")
            cls.buy()
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        print("TICKET PURCHASE\n----------------------------------------------------------\n\nChoose an ending station:")
        Station.display()
        try:
            stop_id = int(input("Enter Station ID:\t"))
            if stop_id not in Station.stations.keys():
                raise ValueError
        except ValueError:
            print("Not a valid Station ID!\nTry Again...")
            cls.buy()
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        if start_id == stop_id:
            print("Start and Destination cannot be the same!\nTry Again...")
            return
        price = cls.calc_price(start_id, stop_id)
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                print(f'Start:\t{Station.name_from_id(start_id)}\nDestination:\t{Station.name_from_id(stop_id)}\nThe price will be ${price}')
                choice = input("Do you wish to purchase this ticket? (Y/N)").lower()
                if choice == "y":
                    ticket = [secrets.token_hex(8), start_id, stop_id]
                    with open("tickets.csv", "a") as file:
                        writer = csv.writer(file)
                        writer.writerow(ticket)
                    cls.tickets.append(ticket)
                    return
                elif choice == "n":
                    return
                else:
                    raise ValueError
            except ValueError:
                print("Error!\nTry again...")
                continue
            
    @classmethod
    def display(cls):
        for ticket in cls.tickets:
            print(f'[{ticket.id}]: {Station.name_from_id(ticket.start_id)} => {Station.name_from_id(ticket.stop_id)}')
    
    @classmethod
    def remove(cls, id: int):
        for ticket in cls.tickets:
            if ticket.id == id:
                cls.tickets.remove(ticket)


def main():
    pass