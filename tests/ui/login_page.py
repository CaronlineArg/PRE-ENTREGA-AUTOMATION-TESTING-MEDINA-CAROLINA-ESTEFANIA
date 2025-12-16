import pytest
from pages.login_page import LoginPage
from utils.datos import leer_csv_login
from utils.logger import logger

CASOS = leer_csv_login("datos/login.csv")

@pytest.mark.ui
@pytest.mark.parametrize("usuario, clave, debe", CASOS)
def test_login_parametrizado(driver, usuario, clave, debe):
    logger.info(f"Iniciando test_login_parametrizado con usuario={usuario}")

    login = LoginPage(driver)
    login.abrir()

    logger.info("Completando usuario y contraseña")
    #Completa el formulario de login y hace submit
    login.completar_usuario(usuario)
    login.completar_clave(clave)
    login.enviar()

    if debe:
        logger.info("Validando login exitoso")
        assert "inventory.html" in driver.current_url, "El usuario válido no ingresó"
        logger.info("Login exitoso validado")
    else:
        logger.info("Validando mensaje de error")
        mensaje = login.obtener_mensaje_error()
        assert "Epic sadface" in mensaje, "El mensaje de error no es correcto"
        logger.info("Mensaje de error validado correctamente")
