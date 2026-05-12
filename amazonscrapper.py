from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()
driver.get("https://www.amazon.in/dp/178633089X")

time.sleep(3)

# 🔽 Scroll slowly to trigger lazy loading
for i in range(3):
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(2)

# 🔽 Now find reviews (product page ones)
reviews = driver.find_elements(By.CLASS_NAME, "a-profile-name")

print("Found:", len(reviews))

for r in reviews:
    try:
        print({
            "name":r.text
        })
    except Exception as e:
        print("skip", e)

driver.quit()