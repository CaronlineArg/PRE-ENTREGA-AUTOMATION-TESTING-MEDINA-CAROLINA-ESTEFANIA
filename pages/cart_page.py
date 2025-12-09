from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    _REMOVE_BUTTON = (By.CSS_SELECTOR, "button[data-test*='remove']")
    _CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def obtener_items(self):
        return self.driver.find_elements(*self._CART_ITEMS)

    def obtener_nombres(self):
        items = self.obtener_items()
        return [item.find_element(*self._ITEM_NAME).text for item in items]

    def obtener_precios(self):
        items = self.obtener_items()
        return [item.find_element(*self._ITEM_PRICE).text for item in items]

    def remover_primer_producto(self):
        remove_buttons = self.driver.find_elements(*self._REMOVE_BUTTON)
        if remove_buttons:
            remove_buttons[0].click()
        return self

    def ir_a_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self._CHECKOUT_BUTTON)).click()
        return self
    
    # Alias para mantener compatibilidad con el test
    def checkout(self):
        return self.ir_a_checkout()