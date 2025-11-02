# tests/test_login.py

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.datos import read_login_data_from_csv
##from helpers.login_helper import login

##@pytest.mark.parametrize("username, password", [
##    ("standard_user", "secret_sauce"),
##])
##def test_login_success(driver, username, password):  # driver viene del fixture
##    login(driver, username, password)
##    # Verificar redirección a página de productos
##    WebDriverWait(driver, 10).until(EC.url_contains("inventory"))
##    assert "inventory" in driver.current_url

##@pytest.mark.parametrize("username, password", [
##    ("locked_out_user", "secret_sauce"),
##])
##def test_login_failure(driver, username, password):  # driver viene del fixture
##    login(driver, username, password)
    # Verificar que aparece el mensaje de error
##    error_message = WebDriverWait(driver, 10).until(
##        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
##    )
##    assert "locked out" in error_message.text.lower()

class LoginPage:
    URL = "https://www.saucedemo.com/"
    _USERNAME_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get(self.URL)
        return self

    def complete_username(self, username):
        campo = self.wait.until(EC.visibility_of_element_located(self._USERNAME_INPUT))
        campo.clear()
        campo.send_keys(username)
        return self

    def complete_password(self, password):
        campo = self.wait.until(EC.visibility_of_element_located(self._PASSWORD_INPUT))
        campo.clear()
        campo.send_keys(password)
        return self

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable(self._LOGIN_BUTTON)).click()
        return self

    def complete_login(self, username, password):
        return (
            self.load()
                .complete_username(username)
                .complete_password(password)
                .click_login()
        )

    def there_is_an_error(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR_MESSAGE))
            return True
        except:
            return False

    def get_error_message(self):
        if self.there_is_an_error():
            return self.driver.find_element(*self._ERROR_MESSAGE).text
        return ""

    def is_logged_in(self):
        """✅ Comprueba si el login redirige a /inventory."""
        try:
            self.wait.until(EC.url_contains("/inventory"))
            return True
        except:
            return False


@pytest.mark.parametrize(
    "username,password,access_granted",
    read_login_data_from_csv("tests/datos/login.csv")
)
def test_login_from_csv(driver, username, password, access_granted):
    """Verifica si el login funciona o falla según el CSV."""
    page = LoginPage(driver)
    page.complete_login(username, password)

    result = page.is_logged_in()

    if access_granted:
        print(f"✅ [{username}] debía acceder → Resultado real: {result}")
        assert result, f"❌ {username} debía acceder, pero no entró. Error: {page.get_error_message()}"
    else:
        print(f"🚫 [{username}] NO debía acceder → Resultado real: {result}")
        assert not result, f"❌ {username} no debía acceder, pero entró al inventario"
        if page.there_is_an_error():
            print(f"   🧾 Mensaje mostrado: {page.get_error_message()}")