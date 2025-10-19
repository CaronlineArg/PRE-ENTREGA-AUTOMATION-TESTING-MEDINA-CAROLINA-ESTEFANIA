# conftest.py
import pytest
from helpers.login_helper import get_edge_driver

@pytest.fixture
def driver():
    driver = get_edge_driver()  # Inicializa Edge desde tu helper
    yield driver
    driver.quit()  # Cierra Edge al final del test
