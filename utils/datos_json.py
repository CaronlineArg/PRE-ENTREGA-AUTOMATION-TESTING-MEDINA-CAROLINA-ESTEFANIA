# utils/datos_json.py
import json
import pathlib

def read_products_from_json(filepath):
    """Lee productos desde JSON y devuelve la lista completa."""
    with open(filepath, 'r', encoding="utf-8") as archivo:
        productos = json.load(archivo)
    return productos  # devolvemos la lista completa con 'nombre', 'precio', 'descripcion'
