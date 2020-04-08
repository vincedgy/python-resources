from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Initialize options
options = Options()
options = webdriver.FirefoxOptions()
options.headless = True
# Initialize options
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)
profile.update_preferences()

# Launch driver
DRIVER = webdriver.Firefox(firefox_profile=profile,
                           executable_path=r'drivers/macos/geckodriver',
                           options=options)
DRIVER.delete_all_cookies()

PATHS = [{
    "name": "DO",
    "env": "PROD",
    "url": "https://donneursdordre.e-attestations.com/EAttestationsDO/",
    "className": "invisible-version-label"
}, {
    "name": "DO",
    "env": "DEMO",
    "url": "https://demo.e-attestations.com/EAttestationsDO/",
    "className": "invisible-version-label"
}, {
    "name": "DO",
    "env": "SANDBOX",
    "url": "https://donneursdordre.dev-e-attestations.com/EAttestationsDO/",
    "className": "invisible-version-label"
}, {
    "name": "DO",
    "env": "RECETTE",
    "url": "https://do01.dev-uservice.dev-e-attestations.com/EAttestationsDO/",
    "className": "invisible-version-label"
}, {
    "name": "DE",
    "env": "PROD",
    "url":
    "https://declarants.e-attestations.com/EAttestationsFO/fo/E-Attestations.html",
    "className": "invisible-version-label"
}, {
    "name": "DE",
    "env": "DEMO",
    "url":
    "https://demo.e-attestations.com/EAttestationsFO/fo/E-Attestations.html",
    "className": "invisible-version-label"
}, {
    "name": "DE",
    "env": "SANDBOX",
    "url":
    "https://declarant.dev-e-attestations.com/EAttestationsFO/fo/E-Attestations.html",
    "className": "invisible-version-label"
}, {
    "name": "DE",
    "env": "RECETTE",
    "url":
    "https://fo01.dev-uservice.dev-e-attestations.com/EAttestationsFO/fo/E-Attestations.html",
    "className": "invisible-version-label"
}]


def get_elem(url, class_name):
    """Wait and fetch on element from url for a class"""
    DRIVER.get(url)
    try:
        version = WebDriverWait(DRIVER, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        return version.get_attribute('innerHTML')
    except TimeoutException:
        pass


for item in PATHS:
    print("%s [%s]: %s" %
          (item['name'], item['env'],
           get_elem(url=item['url'], class_name=item['className'])))

DRIVER.close()
