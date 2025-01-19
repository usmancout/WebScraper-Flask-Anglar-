from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
CORS(app)


options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")  
options.add_argument("--no-sandbox")  
service = Service('/home/usmancout/Downloads/AP/chromedriver-linux64/chromedriver')  # Update this path to your ChromeDriver

@app.route('/scrape', methods=['GET'])
def scrape():
    url = "https://books.toscrape.com/"
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    books = []
    try:
        
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product_pod')))
        
        
        book_elements = driver.find_elements(By.CLASS_NAME, 'product_pod')
        for book_element in book_elements:
            title = book_element.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('title')
            book_link = book_element.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('href')

            
            driver.get(book_link)
            try:
                
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'meta')))
                description_tag = driver.find_element(By.XPATH, "//meta[@name='description']")
                description = description_tag.get_attribute('content').strip() if description_tag else 'No description available'
            except Exception:
                description = 'No description available'

            books.append({'title': title, 'description': description})
            driver.back()  
    finally:
        driver.quit()  

    return jsonify({"books": books})

if __name__ == '__main__':
    app.run(debug=True)
