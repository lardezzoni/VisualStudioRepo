from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests


# gets two URLS, and finds the lowest price between them
# for this example we are using two amazon products
class CrawlingModule:
    def __init__(self):
        # Mimic a real browser's headers
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def fetch_static_page(self, url):
        """Fetch static web pages with headers."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Ensure the request was successful
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching static page: {e}")
            return None

#after inspecting the AMAZON html using firefox inspect, we discovered that the class where the price is is called `a-price-whole`
class ParsingModule:
    def parse_product_details(self, html_content):
        """Extract product details (name, price, availability)."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract the product name
            name = soup.find('span', {'id': 'productTitle'})
            if name:
                name = name.text.strip()
            else:
                name = "Name not found"

            # Extract the price
            price_whole = soup.find('span', {'class': 'a-price-whole'})
            price_decimal = soup.find('span', {'class': 'a-price-decimal'})
            if price_whole:
                # Concatenate the whole and decimal parts as strings
                price = f"{price_whole.text.strip()}{price_decimal.text.strip() if price_decimal else ''}"
            else:
                price = "Price not found"

            # Extract availability (optional)
            availability = soup.find('div', {'id': 'availability'})
            if availability:
                availability = availability.text.strip()
            else:
                availability = "Availability not found"

            return {
                "name": name,
                "price": price,
                "availability": availability
            }
        except Exception as e:
            print(f"Error parsing content: {e}")
            return None

class ComparisonModule:
    def find_lowest_price(self, products):
        """Compare prices and return the lowest."""
        try:
            if not products:
                return None, None
            
            # Compare prices numerically by converting them to integers
            lowest_product = min(products, key=lambda x: int(x["price"].replace('.', '').replace(',', '')))
            return lowest_product["url"], lowest_product["price"]
        except Exception as e:
            print(f"Error finding lowest price: {e}")
            return None, None
if __name__ == "__main__":
    # URLs to test with (use dummy or publicly available product pages)
    urls = [
        "https://www.amazon.com/HP-DeskJet-2755e-Wireless-Printer/dp/B08XYP6BJV/?_encoding=UTF8&pd_rd_w=HK0EC&content-id=amzn1.sym.9929d3ab-edb7-4ef5-a232-26d90f828fa5&pf_rd_p=9929d3ab-edb7-4ef5-a232-26d90f828fa5&pf_rd_r=Q5CCPEWHPPA3Z2NJMPRS&pd_rd_wg=3gH2V&pd_rd_r=064203df-e209-4f1e-b483-cac8db4b312c&ref_=pd_hp_d_btf_crs_zg_bs_541966",
        "https://www.amazon.com/dp/B0BSMSYM9N/ref=sspa_dk_detail_1?psc=1&pd_rd_i=B0BSMSYM9N&pd_rd_w=TxFTu&content-id=amzn1.sym.386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_p=386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_r=PVW1ZT7KAS0RCJ603X68&pd_rd_wg=fIsol&pd_rd_r=d6fc4c07-4a05-42f5-b268-f9b4d8bece8a&s=office-products&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM"
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