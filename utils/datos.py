import csv
from pathlib import Path


def leer_csv_login(relative_path: str):
    """
    Lee un archivo CSV desde la raíz del proyecto.
    """
    data = []

 
    project_root = Path(__file__).resolve().parent.parent

   
    file_path = (project_root / relative_path).resolve()

    if not file_path.exists():
        raise FileNotFoundError(f"❌ No se encontró el archivo CSV en: {file_path}")

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            data.append((
                fila["user"],
                fila["password"],
                fila["access_granted"].strip().lower() == "true"
            ))

    return data
