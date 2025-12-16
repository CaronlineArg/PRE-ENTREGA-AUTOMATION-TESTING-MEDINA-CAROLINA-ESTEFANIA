import pytest
from pages.login_page import LoginPage
from utils.logger import logger

credenciales = [
    ("standard_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("wrong", "wrong", False),
]

@pytest.mark.ui
@pytest.mark.parametrize("usuario, clave, debe_loguear", credenciales)
def test_login_page_pom(driver, usuario, clave, debe_loguear):
    logger.info(f"Iniciando test_login_page_pom con usuario={usuario}")

    login = LoginPage(driver)
    login.login_completo(usuario, clave)

    if debe_loguear:
        logger.info("Validando login exitoso")
        assert "inventory.html" in driver.current_url
        logger.info("Login exitoso validado")
    else:
        # Intentando login con credenciales inválidas
        logger.info("Validando mensaje de error")
        mensaje = login.obtener_mensaje_error()
        assert "Epic sadface" in mensaje
        logger.info("Mensaje de error validado correctamente")
