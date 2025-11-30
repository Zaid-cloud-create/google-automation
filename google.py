from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Open Google search for "github"
driver.get("https://www.google.com/search?q=github")

# Handle Google cookie/consent popup if it appears
try:
    consent_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'I agree') or contains(text(),'Agree')]")
        )
    )
    consent_button.click()
except:
    pass  # No popup appeared

# Wait for search results to appear
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='http']"))
    )
except:
    print("Search results did not load.")
    driver.quit()
    exit()

# Collect all external links
results = driver.find_elements(By.CSS_SELECTOR, "a[href^='http']")
links = []
seen = set()

for r in results:
    url = r.get_attribute("href")
    # Filter out Google internal links and duplicates
    if url and "google.com" not in url and url not in seen:
        links.append(url)
        seen.add(url)

# Print number of links found
if not links:
    print("No links found.")
else:
    print(f"Total links found: {len(links)}")
    for link in links:
        print(link)

# Save links to CSV
with open("google_results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Link"])
    for link in links:
        writer.writerow([link])

print("Saved all links to google_results.csv")

# Close the browser
driver.quit()
