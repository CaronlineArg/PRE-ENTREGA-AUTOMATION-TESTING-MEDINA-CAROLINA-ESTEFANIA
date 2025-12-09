from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    _NAME = (By.ID, "first-name")
    _LAST = (By.ID, "last-name")
    _POSTAL = (By.ID, "postal-code")
    _CONTINUE = (By.ID, "continue")
    _FINISH = (By.ID, "finish")
    _ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    def fill_info(self, first, last, postal):
        self.wait.until(EC.visibility_of_element_located(self._NAME)).send_keys(first)
        self.driver.find_element(*self._LAST).send_keys(last)
        self.driver.find_element(*self._POSTAL).send_keys(postal)
        return self


    def continue_btn(self):
        self.driver.find_element(*self._CONTINUE).click()
        return self


    def finish(self):
        self.driver.find_element(*self._FINISH).click()
        return self


    def has_error(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR))
            return True
        except:
            return False