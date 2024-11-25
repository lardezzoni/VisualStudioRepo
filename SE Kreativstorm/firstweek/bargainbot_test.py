from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class CrawlingModule:
    def fetch_static_page(self, url):
        """Fetch static web pages."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching static page: {e}")
            return None

    def fetch_dynamic_page(self, url):
        """Fetch dynamic web pages using Selenium."""
        try:
            service = Service("path_to_chromedriver")  # Replace with your ChromeDriver path
            driver = webdriver.Chrome(service=service)
            driver.get(url)
            content = driver.page_source
            driver.quit()
            return content
        except Exception as e:
            print(f"Error fetching dynamic page: {e}")
            return None

            class ParsingModule:
    def parse_product_details(self, html_content):
        """Extract product details (name, price, availability)."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            name = soup.find('h1', {'class': 'product-name'}).text.strip()
            price = soup.find('span', {'class': 'price'}).text.strip()
            availability = soup.find('div', {'class': 'availability'}).text.strip()
            return {"name": name, "price": price, "availability": availability}
        except Exception as e:
            print(f"Error parsing content: {e}")
            return None

            class ComparisonModule:
    def find_lowest_price(self, products):
        """Compare prices and return the lowest."""
        try:
            if not products:
                return None, None
            lowest_product = min(products, key=lambda x: x["price"])
            return lowest_product["url"], lowest_product["price"]
        except Exception as e:
            print(f"Error finding lowest price: {e}")
            return None, None

            if __name__ == "__main__":
    # URLs to test with (use dummy or publicly available product pages)
    urls = [
        "http://example.com/product1",
        "http://example.com/product2",
        "http://example.com/product3"
    ]

    # Initialize modules
    crawler = CrawlingModule()
    parser = ParsingModule()
    comparator = ComparisonModule()

    # Fetch and parse product details
    products = []
    for url in urls:
        html = crawler.fetch_static_page(url)  # Replace with `fetch_dynamic_page` for JS pages
        if html:
            details = parser.parse_product_details(html)
            if details:
                details["url"] = url
                products.append(details)

    # Find the lowest price
    lowest_url, lowest_price = comparator.find_lowest_price(products)
    if lowest_price:
        print(f"The lowest price is ${lowest_price} at {lowest_url}")
    else:
        print("No valid prices found.")