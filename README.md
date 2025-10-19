# Proyecto de Automatización - Saucedemo

# Repositorio con ejercicios de todas las clases

Github: [https://github.com/CaronlineArg/talentTechMed]

# Test cases manuales
Excel: [https://docs.google.com/spreadsheets/d/1MAF1m6u6Qeivu1B7kOLxRv069PX5ZePx5HgPgwOTeJ4/edit?usp=sharing]

## Propósito

Este proyecto tiene como objetivo la **verificación automatizada** de:

-  Login de usuarios (válido e inválido)
-  Navegación a la página de productos
-  Verificación de productos listados
-  Validación de precios y nombres
-  Agregado de productos al carrito

Se utiliza el sitio de prueba: [https://www.saucedemo.com](https://www.saucedemo.com) para practicar pruebas funcionales usando automatización.

---

## Tecnologías utilizadas

- [Python 3.x](https://www.python.org/)
- [Pytest](https://docs.pytest.org/)
- [Selenium WebDriver](https://www.selenium.dev/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (para Google Chrome)

---

##  Instalación

pip install selenium pytest

## Instalar requirements.txt
Comando para instalarlas

Ubicate en la carpeta raíz del proyecto (donde está tu requirements.txt) y ejecutá:

pip install -r requirements.txt

## Cómo ejecutar las pruebas

- Desde la raíz del proyecto, ejecutá:
pytest tests/

- Para ver los prints y mensajes en consola:
pytest tests/ -s

- Para generar un reporte HTML (si tenés pytest-html instalado):
pytest --html=report.html

# Generar reporte
pytest -v --html=reports/reporte.html