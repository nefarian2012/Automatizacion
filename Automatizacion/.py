from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_browser():
    """Configura el navegador Chrome para las pruebas."""
    print("Configurando el navegador...")
    driver = webdriver.Chrome()  #ChromeDriver instalado
    driver.maximize_window()
    return driver

def test_login(driver, username, password):
    """
    Prueba el login con credenciales específicas.
    Retorna:
        - "Éxito" si el login funciona.
        - Mensaje de error si falla.
    """
    try:
        print(f"\nProbando usuario: '{username}'...")
        
        # 1. Ir a la página de login
        driver.get("https://www.saucedemo.com/")
        time.sleep(1)  # Pequeña pausa para ver la página
        
        # 2. Llenar campos
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        print("Credenciales ingresadas.")
        time.sleep(1)
        
        # 3. Click en Login
        driver.find_element(By.ID, "login-button").click()
        print("Boton de login presionado.")
        time.sleep(2)  # Pausa para ver el resultado
        
        # 4. Verificar resultado
        if "inventory.html" in driver.current_url:
            print("Login exitoso!")
            return "Éxito"
        else:
            error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
            print(f"Error: {error}")
            return error
            
    except Exception as e:
        print(f"Fallo inesperado: {str(e)}")
        return f"Error: {str(e)}"

def run_tests():
    """Ejecuta todos los casos de prueba."""
    driver = setup_browser()
    
    # Casos de prueba (username, password, resultado_esperado)
    test_cases = [
        # Caso 1: Credenciales válidas
        {"username": "standard_user", "password": "secret_sauce", "expected": "Éxito"},
        # Caso 2: Usuario bloqueado
        {"username": "locked_out_user", "password": "secret_sauce", "expected": "locked out"},
        # Caso 3: Usuario inexistente
        {"username": "usuario_fake", "password": "123456", "expected": "do not match"},
        # Caso 4: Contraseña vacía
        {"username": "standard_user", "password": "", "expected": "Password is required"},
        # Caso 5: Campos vacíos
        {"username": "", "password": "", "expected": "Username is required"},
    ]
    
    print("\nIniciando pruebas de SauceDemo...\n")
    
    for case in test_cases:
        result = test_login(driver, case["username"], case["password"])
        
        # Validar resultado
        if case["expected"].lower() in str(result).lower():
            print(f"PASO: Esperado '{case['expected']}' | Obtenido: '{result}'\n")
        else:
            print(f"FALLO: Esperado '{case['expected']}' | Obtenido: '{result}'\n")
        
        # Volver al login (excepto en el último caso)
        if case != test_cases[-1]:
            print("Volviendo a la pagina de login...")
            driver.get("https://www.saucedemo.com/")
            time.sleep(2)
    
    driver.quit()
    print("\nPruebas completadas con exito!")

if __name__ == "__main__":
    run_tests()