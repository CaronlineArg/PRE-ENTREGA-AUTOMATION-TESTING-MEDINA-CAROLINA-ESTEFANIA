from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    _REMOVE_BUTTON = (By.CSS_SELECTOR, "button[data-test^='remove']")
    _CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _obtener_items(self):
        return self.wait.until(
            EC.visibility_of_all_elements_located(self._CART_ITEMS)
        )


    def obtener_nombres(self):      
        return [
            item.find_element(*self._ITEM_NAME).text
            for item in self._obtener_items()
        ]

    
    def obtener_precios(self):
       return [
            item.find_element(*self._ITEM_PRICE).text
            for item in self._obtener_items()
        ]
    

    def obtener_productos(self):
        productos = []
        for item in self._obtener_items():
            productos.append({
                "nombre": item.find_element(*self._ITEM_NAME).text,
                "precio": item.find_element(*self._ITEM_PRICE).text
            })
        return productos


    
    def remover_producto_por_indice(self, indice=0):
        items = self._obtener_items()
        if indice >= len(items):
            raise IndexError("Índice fuera de rango en el carrito")

        items[indice].find_element(*self._REMOVE_BUTTON).click()
        return self

    def remover_todos_los_productos(self):
        for item in self._obtener_items():
            item.find_element(*self._REMOVE_BUTTON).click()
        return self

    def ir_a_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self._CHECKOUT_BUTTON)).click()
        return self
    
    # Alias para mantener compatibilidad con el test
    def checkout(self):
        return self.ir_a_checkout()