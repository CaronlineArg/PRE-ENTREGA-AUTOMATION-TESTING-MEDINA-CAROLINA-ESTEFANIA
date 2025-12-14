import pytest
from pages.login_page import LoginPage
from utils.datos import leer_csv_login

CASOS = leer_csv_login("datos/login.csv")

@pytest.mark.ui
@pytest.mark.parametrize("usuario, clave, debe", CASOS)
def test_login_parametrizado(driver, usuario, clave, debe):
    login = LoginPage(driver)
    login.abrir()

    login.completar_usuario(usuario)
    login.completar_clave(clave)
    login.enviar()

    if debe:
        assert "inventory.html" in driver.current_url, "El usuario válido no ingresó"
    else:
        mensaje = login.obtener_mensaje_error()
        assert "Epic sadface" in mensaje, "El mensaje de error no es correcto"