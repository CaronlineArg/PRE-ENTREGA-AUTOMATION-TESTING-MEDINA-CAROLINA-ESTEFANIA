# tests/test_login.py

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.login_helper import login

@pytest.mark.parametrize("username, password", [
    ("standard_user", "secret_sauce"),
])
def test_login_success(driver, username, password):  # driver viene del fixture
    login(driver, username, password)
    # Verificar redirección a página de productos
    WebDriverWait(driver, 10).until(EC.url_contains("inventory"))
    assert "inventory" in driver.current_url

@pytest.mark.parametrize("username, password", [
    ("locked_out_user", "secret_sauce"),
])
def test_login_failure(driver, username, password):  # driver viene del fixture
    login(driver, username, password)
    # Verificar que aparece el mensaje de error
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    assert "locked out" in error_message.text.lower()
