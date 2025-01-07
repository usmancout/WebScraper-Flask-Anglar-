from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['GET'])
def scrape():
    url = "https://books.toscrape.com/"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    books = []
    for book in soup.find_all('article', class_='product_pod'):
        title = book.find('h3').find('a').get('title')
        book_link = book.find('h3').find('a').get('href')
        
        book_page_url = f"https://books.toscrape.com/{book_link}"
        book_page_response = requests.get(book_page_url)
        book_page_soup = BeautifulSoup(book_page_response.content, "html.parser")
        
    
        description_tag = book_page_soup.find('meta', attrs={'name': 'description'})
        description = description_tag.get('content').strip() if description_tag else 'No description available'

        books.append({'title': title, 'description': description})

    return jsonify({"books": books})

if __name__ == '__main__':
    app.run(debug=True)