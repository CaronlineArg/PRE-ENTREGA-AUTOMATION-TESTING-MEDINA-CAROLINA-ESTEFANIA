import csv
import pathlib

def read_login_data_from_csv(filepath):
    """Lee user,password,access_granted del CSV y devuelve una lista de tuplas."""
    data = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row["user"]
            password = row["password"]
            access_granted = row["access_granted"].strip().lower() == "true"
            data.append((username, password, access_granted))
    return data

