import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.ui
def test_checkout_completo(driver):
   
    LoginPage(driver).login_completo("standard_user", "secret_sauce")

   
    inv = InventoryPage(driver)
    inv.add_first_product()
    inv.open_cart()

 
    cart = CartPage(driver)
    cart.ir_a_checkout()  

    chk = CheckoutPage(driver)
    chk.fill_info("Carolina", "Medina", "1234")
    chk.continue_btn()
    chk.finish()

   
    assert "checkout-complete" in driver.current_url
    print(" Checkout completado exitosamente")