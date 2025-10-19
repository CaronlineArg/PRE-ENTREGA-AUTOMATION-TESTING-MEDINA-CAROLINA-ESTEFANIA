from helpers.login_helper import login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_product_items_and_cart(driver):
    login(driver, "standard_user", "secret_sauce")

    wait = WebDriverWait(driver, 10)
#validar presencia de elementos filtro y menu
    filter_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product_sort_container")))
    assert filter_button.is_displayed()
    menu_button = wait.until(EC.visibility_of_element_located((By.ID, "react-burger-menu-btn")))
    assert menu_button.is_displayed()
    

    product_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(product_items) > 0

    expected_products = [
        {"name": "Sauce Labs Backpack", "price": "$29.99"},
        {"name": "Sauce Labs Bike Light", "price": "$9.99"},
        {"name": "Sauce Labs Bolt T-Shirt", "price": "$15.99"}
    ]

    for i in range(3):
        name = product_items[i].find_element(By.CLASS_NAME, "inventory_item_name").text
        price = product_items[i].find_element(By.CLASS_NAME, "inventory_item_price").text
        assert name == expected_products[i]["name"]
        assert price == expected_products[i]["price"]

    # Agregar al carrito
    add_to_cart = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_to_cart.click()

    # Verificar que se agregó
    cart_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert cart_badge.text == "1"
