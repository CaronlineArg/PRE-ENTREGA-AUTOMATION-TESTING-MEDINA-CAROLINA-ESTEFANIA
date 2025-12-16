import pytest
from utils.logger import get_logger
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from datetime import datetime, timezone, timedelta
import base64

PROJECT_NAME = "SauceDemo"
EXECUTION_TYPE = "AllTests"
BROWSER = "edge"
PROJECT_ROOT = Path.cwd()  # Directorio de ejecución

# Crear carpetas
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
    tz_argentina = timezone(timedelta(hours=-3))
    now = datetime.now(tz_argentina)
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"{PROJECT_NAME}_{BROWSER}_{EXECUTION_TYPE}_{timestamp}.html"
    report_path = REPORTS_DIR / report_name

    if not config.option.htmlpath:
        config.option.htmlpath = str(report_path)
        config.option.self_contained_html = True  # Importante para incrustar screenshots

    print(f"\n📊 Generando reporte HTML")
    print(f"   📄 Nombre: {report_name}")
    print(f"   📁 Ruta: {report_path}")
    print(f"   🕐 Hora Argentina: {now.strftime('%d/%m/%Y %H:%M:%S')}\n")


@pytest.fixture
def driver():
    options = EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    
    service = EdgeService()
    drv = webdriver.Edge(service=service, options=options)
    yield drv
    drv.quit()



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    drv = item.funcargs.get("driver", None)
    
    if report.when == "call" and report.failed and drv:
        tz_argentina = timezone(timedelta(hours=-3))
        timestamp = datetime.now(tz_argentina).strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{item.name}_{timestamp}.png"
        file_path = SCREEN_DIR / file_name

        try:
            drv.save_screenshot(str(file_path))
            report.extra = getattr(report, "extra", [])
            pytest_html = item.config.pluginmanager.getplugin("html")
            
            if pytest_html:
                # Leer el archivo y convertir a base64
                with open(file_path, "rb") as f:
                    img_base64 = base64.b64encode(f.read()).decode("utf-8")
                
                # Incrustar la imagen directamente en el HTML
                report.extra.append(
                    pytest_html.extras.html(
                        f'<div><b>Screenshot del fallo:</b><br>'
                        f'<img src="data:image/png;base64,{img_base64}" '
                        f'style="width:600px;border:1px solid #ccc"/></div>'
                    )
                )

            
            print(f"📸 Screenshot guardado e incrustado: {file_path}")
        except Exception as e:
            logger.error(f"No se pudo guardar screenshot: {e}")


def pytest_html_report_title(report):
    report.title = "Framework SauceDemo – Reporte General"


def pytest_html_results_summary(prefix, summary, postfix):
    tz_argentina = timezone(timedelta(hours=-3))
    timestamp = datetime.now(tz_argentina).strftime("%d-%b-%Y a las %H:%M:%S")
    
    prefix.extend([
        f"<p><b>Proyecto:</b> Framework SauceDemo</p>",
        f"<p><b>Autor:</b> Carolina Medina</p>",
        f"<p><b>Fecha de ejecución:</b> {timestamp} (Argentina)</p>",
    ])


def pytest_sessionfinish(session, exitstatus):
    """Al finalizar la sesión mostrar reporte"""
    if hasattr(session.config.option, 'htmlpath') and session.config.option.htmlpath:
        report_path = Path(session.config.option.htmlpath)
        if report_path.exists():
            print(f"\n✅ Reporte HTML generado exitosamente!")
            print(f"📁 Ubicación: {report_path}")
            print(f"🌐 Abre en el navegador: file:///{report_path}\n")
        else:
            print(f"\n⚠️ Advertencia: El reporte no se generó en {report_path}\n")
