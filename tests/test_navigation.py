from helpers.login_helper import login
from selenium.webdriver.common.by import By

def test_navigation(driver):
    login(driver, "standard_user", "secret_sauce")

    assert "inventory" in driver.current_url

    product_title = driver.find_element(By.CLASS_NAME, "title")
    assert product_title.text == "Products"

    assert driver.title == "Swag Labs"
