from bs4 import BeautifulSoup
import requests
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

# @luiz ardezzoni 2024

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
            print(f"{Fore.RED}Error fetching static page: {e}")
            return None


class ParsingModule:
    def parse_product_details(self, html_content):
        """Extract product details (name, price, availability)."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract the product name
            name = soup.find('span', {'id': 'productTitle'})
            name = name.text.strip() if name else "Name not found"

            # Extract the price
            price_whole = soup.find('span', {'class': 'a-price-whole'})
            price_decimal = soup.find('span', {'class': 'a-price-decimal'})
            price = (
                f"{price_whole.text.strip()}{price_decimal.text.strip() if price_decimal else ''}"
                if price_whole
                else "Price not found"
            )

            # Extract availability (optional)
            availability = soup.find('div', {'id': 'availability'})
            availability = availability.text.strip() if availability else "Availability not found"

            return {
                "name": name,
                "price": price,
                "availability": availability
            }
        except Exception as e:
            print(f"{Fore.RED}Error parsing content: {e}")
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
            print(f"{Fore.RED}Error finding lowest price: {e}")
            return None, None

# Main implementation of BargainBot

if __name__ == "__main__":
    # Banner
    print(f"{Fore.GREEN}{Style.BRIGHT}BargainBot 1.0")
    print(f"{Fore.GREEN}{'-' * 30}")

    # URLs to test with
    urls = [
        "https://www.amazon.com/HP-DeskJet-2755e-Wireless-Printer/dp/B08XYP6BJV/?_encoding=UTF8&pd_rd_w=HK0EC&content-id=amzn1.sym.9929d3ab-edb7-4ef5-a232-26d90f828fa5&pf_rd_p=9929d3ab-edb7-4ef5-a232-26d90f828fa5&pf_rd_r=Q5CCPEWHPPA3Z2NJMPRS&pd_rd_wg=3gH2V&pd_rd_r=064203df-e209-4f1e-b483-cac8db4b312c&ref_=pd_hp_d_btf_crs_zg_bs_541966",
        "https://www.amazon.com/dp/B0BSMSYM9N/ref=sspa_dk_detail_1?psc=1&pd_rd_i=B0BSMSYM9N&pd_rd_w=TxFTu&content-id=amzn1.sym.386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_p=386c274b-4bfe-4421-9052-a1a56db557ab&pf_rd_r=PVW1ZT7KAS0RCJ603X68&pd_rd_wg=fIsol&pd_rd_r=d6fc4c07-4a05-42f5-b268-f9b4d8bece8a&s=office-products&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM"
    ]

    print(f"{Fore.CYAN}Selected URLs:")
    for url in urls:
        print(f"{Fore.BLUE}{url}")
    print(f"{Fore.GREEN}{'-' * 30}")

    print(f"{Fore.YELLOW}Testing connection to URLs...")
    print(f"{Fore.GREEN}{'-' * 30}")

    # Initialize modules
    crawler = CrawlingModule()
    parser = ParsingModule()
    comparator = ComparisonModule()

    # Fetch and parse product details
    products = []
    for url in urls:
        print(f"{Fore.YELLOW}Fetching: {url}")
        html = crawler.fetch_static_page(url)
        if html:
            print(f"{Fore.GREEN}Successfully fetched content from {url}")
            details = parser.parse_product_details(html)
            if details:
                print(f"{Fore.CYAN}Product found: {details['name']}, Price: {details['price']}")
                details["url"] = url
                products.append(details)
            else:
                print(f"{Fore.RED}Failed to parse product details.")
        else:
            print(f"{Fore.RED}Failed to fetch content from {url}")
    
    print(f"{Fore.GREEN}{'-' * 30}")

    # Find the lowest price
    lowest_url, lowest_price = comparator.find_lowest_price(products)
    if lowest_price:
        print(f"{Fore.MAGENTA}The lowest price is:")
        print(f"{Fore.MAGENTA}${lowest_price} at {lowest_url}")
    else:
        print(f"{Fore.RED}No valid prices found.")
    print(f"{Fore.GREEN}{'-' * 30}")
