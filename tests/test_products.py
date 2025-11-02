# tests/test_product_items_and_cart.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.login_helper import login
from utils.datos_json import read_products_from_json
import pathlib

def test_product_items_and_cart(driver):
    # Hacer login
    login(driver, "standard_user", "secret_sauce")

    wait = WebDriverWait(driver, 10)

    # Validar presencia de elementos filtro y menú
    filter_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product_sort_container")))
    assert filter_button.is_displayed()
    menu_button = wait.until(EC.visibility_of_element_located((By.ID, "react-burger-menu-btn")))
    assert menu_button.is_displayed()

    # Traer productos de JSON
    json_path = pathlib.Path("tests/datos/productos.json")
    productos_json = read_products_from_json(json_path)

    expected_products = []
    for producto in productos_json:
        expected_products.append({
            "name": producto["nombre"],
            "price": f"${producto['precio']:.2f}",
            "id": f"add-to-cart-{producto['nombre'].lower().replace(' ', '-')}"
        })

    # Validar productos en la página
    product_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(product_items) > 0

    for i in range(len(expected_products)):
        name = product_items[i].find_element(By.CLASS_NAME, "inventory_item_name").text
        price = product_items[i].find_element(By.CLASS_NAME, "inventory_item_price").text
        assert name == expected_products[i]["name"]
        assert price == expected_products[i]["price"]

    # Agregar productos al carrito
    productos_agregados = []
    for i, product in enumerate(expected_products):
        add_to_cart = driver.find_element(By.ID, product["id"])
        add_to_cart.click()
        productos_agregados.append(product["name"])

        cart_badge = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        wait.until(lambda d: cart_badge.text == str(i + 1))
        assert cart_badge.text == str(i + 1), f"Badge debería mostrar {i + 1}, muestra {cart_badge.text}"

    # Ir al carrito
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()
    wait.until(EC.url_contains("cart.html"))
    assert "cart.html" in driver.current_url

    # Verificar productos en el carrito
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == len(productos_agregados)

    productos_en_carrito = [item.find_element(By.CLASS_NAME, "inventory_item_name").text for item in cart_items]

    for producto_esperado in productos_agregados:
        assert producto_esperado in productos_en_carrito

    print(f"✅ Productos agregados correctamente: {productos_agregados}")
