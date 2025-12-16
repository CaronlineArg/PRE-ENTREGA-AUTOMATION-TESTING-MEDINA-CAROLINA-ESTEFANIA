import pytest
from utils.logger import logger

logger.info("Mensaje de prueba")

@pytest.mark.framework
def test_falla_ui(driver):
    driver.get("https://www.saucedemo.com/")
    assert False, "Falla intencional para probar screenshot en reporte"




