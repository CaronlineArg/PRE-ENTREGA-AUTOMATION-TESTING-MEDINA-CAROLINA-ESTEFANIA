import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import logger

@pytest.mark.ui
def test_checkout_completo(driver):
    
    logger.info("Iniciando test_checkout_completo")

    LoginPage(driver).login_completo("standard_user", "secret_sauce")
    logger.info("Login exitoso")

    inv = InventoryPage(driver)
    # Este bloque agrega el primer producto al carrito
    inv.add_first_product()
    inv.open_cart()
    logger.info("Producto agregado y carrito abierto")

    cart = CartPage(driver)
    cart.ir_a_checkout()
    logger.info("Navegando a checkout")

    chk = CheckoutPage(driver)
    chk.fill_info("Carolina", "Medina", "1234")
    chk.continue_btn()
    chk.finish()
    logger.info("Checkout finalizado")

    assert "checkout-complete" in driver.current_url
    logger.info("Checkout completado exitosamente")
