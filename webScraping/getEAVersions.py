import os
import requests
import platform
import logging
import json
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from colorama import init, Fore, Back, Style

init()

# urllib3.disable_warnings()
logging.captureWarnings(True)

# Initialize options
options = webdriver.ChromeOptions()
options.headless = True
# Initialize options
# cap = webdriver.DesiredCapabilities()
# profile.set_preference("browser.cache.disk.enable", False)
# profile.set_preference("browser.cache.memory.enable", False)
# profile.set_preference("browser.cache.offline.enable", False)
# profile.set_preference("network.http.use-cache", False)
# profile.update_preferences()

# Launch driver
dir_path = os.path.dirname(os.path.realpath(__file__))
ostype = "macos"
if platform.system() == 'Linux':
    ostype = "linux"


def get_elem(url, class_name):
    """Wait and fetch on element from url for a class"""

    try:
        r = requests.get(url, verify=False, timeout=3)
        r.raise_for_status()
        try:
            driver.get(url)
            version = WebDriverWait(driver=driver, timeout=2).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            return version.get_attribute('innerHTML')
        except TimeoutException:
            raise Exception('timeout')
    except requests.exceptions.Timeout:
        raise Exception('timeout')
    except requests.exceptions.ConnectTimeout:
        raise Exception('unreachable')
    except requests.exceptions.RequestException as e:
        raise Exception(e)


print("Start webscraping EA webapps Versions")

with open(f'{dir_path}/config.json', 'r') as f:
    loaded_json = json.loads(f.read())
sorted_list = sorted(loaded_json, key=lambda k: k['env'])

if len(sorted_list) > 0:
    print("Initializing Chromedriver...")
    driver = webdriver.Chrome(executable_path=f'{dir_path}/drivers/{ostype}/chromedriver')

    for item in sorted_list:

        catch = "unknown"
        name = item['name']
        env = item['env']
        url = item['url']
        class_name = item['className']

        try:
            catch = get_elem(url=url, class_name=class_name)
            print(f'{name} [{env}]: {Fore.GREEN}{catch}{Style.RESET_ALL}')
        except Exception as err:
            print(Fore.RED + f'{name} [{env}]: {err}' + Style.RESET_ALL)

    driver.close()
