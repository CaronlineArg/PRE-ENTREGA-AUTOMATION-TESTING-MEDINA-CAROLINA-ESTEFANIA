import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.mark.ui
def test_inventory_elements(driver):
    LoginPage(driver).login_completo("standard_user", "secret_sauce")

    inv = InventoryPage(driver)

    assert inv.get_title() == "Products"
    assert inv.menu_visible()
    assert inv.sort_visible()

    productos = inv.get_all_products()
    assert len(productos) > 0, " No se encontraron productos"
