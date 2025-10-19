from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.login_helper import login
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
def get_edge_driver():
    edge_driver_path = "C:\\path\\to\\msedgedriver.exe"  # Asegúrate de actualizar esta ruta al lugar donde tengas el msedgedriver.exe
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

def test_product_items_and_cart(driver):
    login(driver, "standard_user", "secret_sauce")

    wait = WebDriverWait(driver, 10)

    # Validar presencia de elementos filtro y menú
    filter_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product_sort_container")))
    assert filter_button.is_displayed()
    menu_button = wait.until(EC.visibility_of_element_located((By.ID, "react-burger-menu-btn")))
    assert menu_button.is_displayed()

    product_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(product_items) > 0

    # Agregar el campo "id" a cada producto
    expected_products = [
        {"name": "Sauce Labs Backpack", "price": "$29.99", "id": "add-to-cart-sauce-labs-backpack"},
        {"name": "Sauce Labs Bike Light", "price": "$9.99", "id": "add-to-cart-sauce-labs-bike-light"},
        {"name": "Sauce Labs Bolt T-Shirt", "price": "$15.99", "id": "add-to-cart-sauce-labs-bolt-t-shirt"}
    ]

    # Validar productos
    for i in range(3):
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

        # Esperar y verificar que el badge del carrito aumente
        cart_badge = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )

        # Verificar que el badge del carrito sea correcto
        WebDriverWait(driver, 10).until(lambda driver: cart_badge.text == str(i + 1))
        assert cart_badge.text == str(i + 1), f"Badge debería mostrar {i + 1}, muestra {cart_badge.text}"

    # Cerrar el modal si aparece
    close_modal(driver)

    # Esperar hasta que el carrito se actualice después de cerrar el modal
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_link"))
    )

    # Ir al carrito
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    # Esperar explícitamente hasta que la URL contenga "cart.html" para asegurarnos de que estemos en el carrito
    WebDriverWait(driver, 10).until(EC.url_contains("cart.html"))
    assert "cart.html" in driver.current_url, "No redirigió al carrito"

    # Verificar que TODOS los productos agregados estén en el carrito
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == len(productos_agregados), \
        f"Se esperaban {len(productos_agregados)} productos en el carrito, se encontraron {len(cart_items)}"

    # Obtener nombres de productos en el carrito
    productos_en_carrito = []
    for item in cart_items:
        nombre = item.find_element(By.CLASS_NAME, "inventory_item_name").text
        productos_en_carrito.append(nombre)

    # Verificar que cada producto agregado esté en el carrito
    for producto_esperado in productos_agregados:
        assert producto_esperado in productos_en_carrito, \
            f"El producto '{producto_esperado}' no está en el carrito"

    print(f"✅ Productos agregados correctamente: {productos_agregados}")
