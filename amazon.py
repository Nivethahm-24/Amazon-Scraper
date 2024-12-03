from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up options for headless browsing
options = Options()
options.add_argument('--headless')  # No GUI
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Set up ChromeDriver path (Colab-specific path)
chrome_driver_path = '/usr/lib/chromium-browser/chromedriver'  # Colab path

# Set up the Service object with the correct path to chromedriver
service = Service(executable_path=chrome_driver_path)

# Initialize the driver with the Service object
driver = webdriver.Chrome(service=service, options=options)

# Open a page (for example, search for "laptop" on Amazon)
driver.get('https://www.amazon.com/s?k=laptop')

# Let the page load
time.sleep(3)

# Print the page title to verify the script works
print(driver.title)

# Close the browser
driver.quit()