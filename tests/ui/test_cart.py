import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger import logger

@pytest.mark.ui
def test_agregar_producto_carrito(driver):
    logger.info("Iniciando test_agregar_producto_carrito")

    LoginPage(driver).login_completo("standard_user", "secret_sauce")

    inv = InventoryPage(driver)
    logger.info("Agregando primer producto al carrito")
    # Agregando primer producto al carrito
    inv.add_first_product()

    # Verificar que el producto se haya agregado
    assert inv.cart_count() >= 1, "No se agregó el producto al carrito"
    logger.info("Producto agregado correctamente al carrito")
