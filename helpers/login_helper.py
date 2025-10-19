from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_edge_driver():
    edge_driver_path = r"C:\Drivers\msedgedriver.exe"  # Asegúrate que exista
    options = Options()
    options.use_chromium = True  # Obligatorio para Edge Chromium
    options.add_argument("start-maximized")
    driver = webdriver.Edge(service=Service(edge_driver_path), options=options)
    return driver


def login(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    wait = WebDriverWait(driver, 20)
    
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()
