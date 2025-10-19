# helpers/login_helper.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    wait = WebDriverWait(driver, 10)

    username_field = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()
