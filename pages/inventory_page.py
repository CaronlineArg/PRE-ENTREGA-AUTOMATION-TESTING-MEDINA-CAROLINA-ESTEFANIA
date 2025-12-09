from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    _TITLE = (By.CLASS_NAME, "title")
    _ITEM = (By.CLASS_NAME, "inventory_item")
    _PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    _PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    _SORT = (By.CLASS_NAME, "product_sort_container")
    _MENU_BTN = (By.ID, "react-burger-menu-btn")
    _ADD_BTN = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_title(self):
        return self.wait.until(EC.visibility_of_element_located(self._TITLE)).text

    def menu_visible(self):
        return self.wait.until(EC.visibility_of_element_located(self._MENU_BTN)).is_displayed()

    def sort_visible(self):
        return self.wait.until(EC.visibility_of_element_located(self._SORT)).is_displayed()

    def get_all_products(self):
        return self.driver.find_elements(*self._ITEM)

    def add_first_product(self):
        self.driver.find_elements(*self._ADD_BTN)[0].click()
        return self

    def open_cart(self):
        self.driver.find_element(*self._CART_LINK).click()
        return self

    def cart_count(self):
        try:
            return int(self.driver.find_element(*self._CART_BADGE).text)
        except:
            return 0
