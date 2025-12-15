import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.ui
def test_agregar_producto_carrito(driver):
    LoginPage(driver).login_completo("standard_user", "secret_sauce")

    inv = InventoryPage(driver)
    inv.add_first_product()

    assert inv.cart_count() >= 1, "No se agregó el producto al carrito"


