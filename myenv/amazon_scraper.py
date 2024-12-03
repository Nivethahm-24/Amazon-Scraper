import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium with Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Remove this line if you want to see the browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Amazon product URLs (replace with actual product pages)
product_urls = [
    "https://www.amazon.in/s?k=iphone+13+128gb&crid=XHZX1MQN5LFY&sprefix=iphone%2Caps%2C269&ref=nb_sb_ss_ts-doa-p_1_6"
]

# List to store product data
data = []

for url in product_urls:
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load fully

    try:
        product_name = driver.find_element(By.ID, "productTitle").text.strip()
        print(f"Product Name: {product_name}")
    except Exception as e:
        print(f"Error getting product name: {e}")
        product_name = "N/A"

    try:
        # Extract product price using multiple methods
        product_price = driver.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").text.strip()
        if not product_price:
            whole_price = driver.find_element(By.CSS_SELECTOR, ".a-price-whole").text.strip()
            fraction_price = driver.find_element(By.CSS_SELECTOR, ".a-price-fraction").text.strip()
            product_price = f"{whole_price}.{fraction_price}"
        print(f"Product Price: {product_price}")
    except Exception as e:
        print(f"Error getting product price: {e}")
        product_price = "N/A"

    try:
        # Extract product rating
        product_rating = driver.find_element(By.CSS_SELECTOR, "span[data-hook='rating-out-of-text']").text.strip()
        print(f"Product Rating: {product_rating}")
    except Exception as e:
        print(f"Error getting product rating: {e}")
        product_rating = "N/A"

    try:
        # Extract number of reviews
        product_reviews = driver.find_element(By.ID, "acrCustomerReviewText").text.strip()
        print(f"Product Reviews: {product_reviews}")
    except Exception as e:
        print(f"Error getting product reviews: {e}")
        product_reviews = "N/A"

    try:
        # Extract product availability
        product_availability = driver.find_element(By.ID, "availability").text.strip()
        print(f"Product Availability: {product_availability}")
    except Exception as e:
        print(f"Error getting product availability: {e}")
        product_availability = "N/A"

    # Append data to list
    data.append({
        "Product Name": product_name,
        "Price": product_price,
        "Rating": product_rating,
        "Number of Reviews": product_reviews,
        "Availability": product_availability
    })

# Close the Selenium driver
driver.quit()

# Convert data to DataFrame
df = pd.DataFrame(data)

# Check if DataFrame is not empty
if not df.empty:
    print("DataFrame contents:")
    print(df)

    # Define output directory (update the path as needed)
    output_dir = r"D:\intern project"

    # Create the directory if it does not exist
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        print("Output directory verified/created successfully.")
    except Exception as e:
        print(f"Error creating output directory: {e}")
        output_dir = "."  # Fallback to current directory

    # Save data to CSV and JSON files
    try:
        csv_path = os.path.join(output_dir, "amazon_products.csv")
        df.to_csv(csv_path, index=False)
        print(f"CSV file saved successfully at {csv_path}.")
    except Exception as e:
        print(f"Error saving CSV: {e}")

    try:
        json_path = os.path.join(output_dir, "amazon_products.json")
        df.to_json(json_path, orient="records")
        print(f"JSON file saved successfully at {json_path}.")
    except Exception as e:
        print(f"Error saving JSON: {e}")

else:
    print("No data found to save.")
