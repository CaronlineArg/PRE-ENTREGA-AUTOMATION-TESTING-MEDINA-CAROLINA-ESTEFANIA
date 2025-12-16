import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger import logger

@pytest.mark.ui
def test_inventory_elements(driver):
    logger.info("Iniciando test_inventory_elements")

    LoginPage(driver).login_completo("standard_user", "secret_sauce")

    inv = InventoryPage(driver)
    logger.info("Validando elementos del inventario")

    assert inv.get_title() == "Products"
    assert inv.menu_visible()
    assert inv.sort_visible()

    productos = inv.get_all_products()
    assert len(productos) > 0, "No se encontraron productos"

    logger.info("Inventario validado correctamente")
