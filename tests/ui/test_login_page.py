import pytest
from pages.login_page import LoginPage

credenciales = [
    ("standard_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("wrong", "wrong", False),
]

@pytest.mark.ui
@pytest.mark.parametrize("usuario, clave, debe_loguear", credenciales)
def test_login_page_pom(driver, usuario, clave, debe_loguear):
    login = LoginPage(driver)
    login.login_completo(usuario, clave)

    if debe_loguear:
        assert "inventory.html" in driver.current_url
    else:
        assert login.hay_error()
