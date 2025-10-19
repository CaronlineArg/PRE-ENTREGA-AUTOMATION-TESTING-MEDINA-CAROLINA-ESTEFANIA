from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC


# Función para iniciar el navegador con Edge
def get_edge_driver():
    edge_driver_path = "C:\\path\\to\\msedgedriver.exe"  # Actualiza esta ruta al lugar donde tengas el msedgedriver
    options = webdriver.EdgeOptions()
    options.add_argument("start-maximized")  # Iniciar el navegador en pantalla completa
    driver = webdriver.Edge(executable_path=edge_driver_path, options=options)
    return driver

def close_modal(driver):
    try:
        # Esperar hasta que el modal esté visible
        modal = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "modal-class"))  # Cambia por la clase correcta del modal
        )
        
        # Ahora espera hasta que el botón de cerrar sea visible y clickeable
        close_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "modal-close-button"))  # Cambia por el selector correcto
        )
        close_button.click()

        # Esperar hasta que el modal se cierre completamente (verifica que ya no esté visible)
        WebDriverWait(driver, 15).until(
            EC.invisibility_of_element(modal)
        )
    except Exception as e:
        print("Error al intentar cerrar el modal: ", e)
        pass  # Si no aparece el modal, simplemente continuamos sin hacer nada


def login(driver, username, password):
    driver.get("https://www.saucedemo.com/")

    wait = WebDriverWait(driver, 20)  # Aumentar tiempo de espera
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    # Verificar si hay un modal emergente de seguridad (si aplica)
    try:
        # Si aparece una ventana modal, esperamos que se cierre
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal_class_name")))
    except:
        pass  # Si no aparece, se continúa normalmente
