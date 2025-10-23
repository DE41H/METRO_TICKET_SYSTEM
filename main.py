import csv


class Station:
    
    stations: dict = {}

    def __init__(self, id: int):
        self.id = id

    def __repr__(self) -> str:
        return str(self.name)

    @property
    def name(self):
        with open("stations.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["id"]) == self.id:
                    return row["name"]
                
    @property
    def neighbours(self):
        with open("stations.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["id"]) == self.id:
                    return row["neighbours"].split("$")
                
    @classmethod
    def load(cls):
        with open("stations.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cls.stations[int(row["id"])] = Station(int(row["id"]))

    @classmethod
    def display(cls):
        for station in cls.stations:
            print(f'[{station}] => {cls.stations[station].name}')


class Line:

    lines: list = []

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name
                
    @property
    def stations(self) -> list:
        with open("lines.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["name"] == self.name:
                    return row["stations"].split("$")
            else:
                return []

    @classmethod
    def load(cls):
        with open("lines.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cls.lines.append(Line(row["name"]))


class Ticket:

    tickets = []

    def __init__(self, id: int):
        self.id = id

    @property
    def start_id(self):
        pass
