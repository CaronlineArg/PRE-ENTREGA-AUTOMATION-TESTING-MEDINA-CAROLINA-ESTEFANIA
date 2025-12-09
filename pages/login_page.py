from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    URL = "https://www.saucedemo.com/"
    _USER = (By.ID, 'user-name')
    _PASS = (By.ID, 'password')
    _BTN = (By.ID, 'login-button')
    _ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def abrir(self):
        self.driver.get(self.URL)
        return self

    def completar_usuario(self, usuario: str):
        campo = self.wait.until(EC.visibility_of_element_located(self._USER))
        campo.clear()
        campo.send_keys(usuario)
        return self

    def completar_clave(self, clave: str):
        campo = self.wait.until(EC.visibility_of_element_located(self._PASS))
        campo.clear()
        campo.send_keys(clave)
        return self

    def enviar(self):
        self.wait.until(EC.element_to_be_clickable(self._BTN)).click()
        return self

    def login_completo(self, usuario, clave):
        return (
            self.abrir()
            .completar_usuario(usuario)
            .completar_clave(clave)
            .enviar()
        )

    def hay_error(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR))
            return True
        except:
            return False

    def obtener_mensaje_error(self):
        if self.hay_error():
            return self.driver.find_element(*self._ERROR).text
        return ""
