import pytest
from utils.logger import get_logger
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from time import time
from datetime import datetime, timezone, timedelta
import os

# Obtener la raíz del proyecto usando el directorio de trabajo actual
# Esto garantiza que siempre use donde se ejecuta pytest
PROJECT_ROOT = Path.cwd()  # Directorio desde donde ejecutas pytest

# Crear directorios
SCREEN_DIR = PROJECT_ROOT / "screens"
SCREEN_DIR.mkdir(parents=True, exist_ok=True)

REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

logger = get_logger('framework')

# Mostrar rutas para debug
print(f"\n{'='*70}")
print(f"🔍 Configuración de rutas:")
print(f"   🏠 Directorio de trabajo: {PROJECT_ROOT}")
print(f"   📊 Carpeta de reportes: {REPORTS_DIR}")
print(f"   📸 Carpeta de screenshots: {SCREEN_DIR}")
print(f"{'='*70}\n")


def pytest_configure(config):
    """Configurar el nombre del reporte con timestamp"""
    # Zona horaria de Argentina (UTC-3)
    tz_argentina = timezone(timedelta(hours=-3))
    now = datetime.now(tz_argentina)
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    report_name = f"report_{timestamp}.html"
    report_path = REPORTS_DIR / report_name
    
    # Configurar el plugin HTML solo si no está ya configurado
    if not config.option.htmlpath:
        config.option.htmlpath = str(report_path)
        config.option.self_contained_html = True
    
    print(f"📊 Generando reporte HTML: {report_name}")
    print(f"📁 Ruta completa: {report_path}")
    print(f"🕐 Hora Argentina: {now.strftime('%d/%m/%Y %H:%M:%S')}\n")


@pytest.fixture(scope='session')
def browser_name():
    return 'edge'


@pytest.fixture
def driver():
    edge_options = EdgeOptions()
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-infobars")
    edge_options.add_argument("--disable-extensions")
    edge_options.add_argument("--disable-popup-blocking")
    
    service = EdgeService()
    driver = webdriver.Edge(service=service, options=edge_options)
    
    yield driver
    
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    drv = item.funcargs.get("driver", None)
    
    if drv:
        try:
            report.page_url = drv.current_url
        except Exception:
            report.page_url = "-"
    
    if report.when == "call" and report.failed and drv:
        timestamp = int(time())
        file_path = SCREEN_DIR / f"{item.name}_{timestamp}.png"
        
        try:
            drv.save_screenshot(str(file_path))
            report.extra = getattr(report, "extra", [])
            report.extra.append(
                {"name": "Screenshot", "format": "image", "content": str(file_path)}
            )
            print(f"📸 Screenshot guardado: {file_path}")
        except Exception as e:
            logger.error(f"No se pudo guardar screenshot: {e}")


def pytest_html_report_title(report):
    report.title = "Framework SauceDemo – Reporte General"


def pytest_html_results_summary(prefix, summary, postfix):
    # Zona horaria de Argentina (UTC-3)
    tz_argentina = timezone(timedelta(hours=-3))
    timestamp = datetime.now(tz_argentina).strftime("%d-%b-%Y a las %H:%M:%S")
    
    prefix.extend([
        "<p><b>Proyecto:</b> Framework SauceDemo</p>",
        "<p><b>Autor:</b> Carolina Medina</p>",
        f"<p><b>Fecha de ejecución:</b> {timestamp} (Argentina)</p>",
    ])


def pytest_sessionfinish(session, exitstatus):
    """Hook que se ejecuta al finalizar la sesión"""
    if hasattr(session.config.option, 'htmlpath') and session.config.option.htmlpath:
        report_path = Path(session.config.option.htmlpath)
        if report_path.exists():
            print(f"\n✅ Reporte HTML generado exitosamente!")
            print(f"📁 Ubicación: {report_path}")
            print(f"🌐 Abre en el navegador: file:///{report_path}\n")
        else:
            print(f"\n⚠️  Advertencia: El reporte no se generó en {report_path}\n")