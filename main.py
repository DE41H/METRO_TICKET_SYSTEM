import csv


class Station:

    stations: dict = {}

    def __init__(self, id: int):
        self.id = id

    @property
    def name(self):
        with open("stations.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["id"]) == self.id:
                    return row["name"]
                
    @classmethod
    def load_stations(cls):
        with open("stations.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cls.stations[row["id"]] = Station(int(row["id"]))

    @classmethod
    def display_stations(cls):
        for station in cls.stations:
            print(f'Station Name: {cls.stations[station].name}\nStation ID: {station}\n')


class Line:

    lines: list = []

    def __init__(self):
        pass


class Ticket:

    tickets = []

    def __init__(self, id: int):
        self.id = id

    @property
    def start_id(self):
        pass
