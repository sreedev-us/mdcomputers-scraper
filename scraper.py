import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin

BASE_URL = "https://mdcomputers.in/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/139.0 Mobile Safari/537.36"
    )
}


def scrape_products(search_term):
    search_url = (
        BASE_URL
        + "?route=product/search&search="
        + quote(search_term)
    )

    print(f"Searching MDComputers for: {search_term}")
    print(f"URL: {search_url}\n")

    response = requests.get(
        search_url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    for product in soup.select(".product-thumb"):
        name_tag = product.select_one(".name a")
        price_tag = product.select_one(".price")
        image_tag = product.select_one(".image img")
        link_tag = product.select_one(".image a")

        if not name_tag:
            continue

        product_data = {
            "name": name_tag.get_text(" ", strip=True),
            "price": (
                price_tag.get_text(" ", strip=True)
                if price_tag else "N/A"
            ),
            "url": (
                urljoin(BASE_URL, link_tag.get("href"))
                if link_tag and link_tag.get("href")
                else "N/A"
            ),
            "image": (
                urljoin(BASE_URL, image_tag.get("src"))
                if image_tag and image_tag.get("src")
                else "N/A"
            )
        }

        products.append(product_data)

    return products


def main():
    search_term = input("Enter product to search: ").strip()

    if not search_term:
        print("Please enter a search term.")
        return

    try:
        products = scrape_products(search_term)

        if not products:
            print("No products found.")
            return

        print(f"Found {len(products)} products.\n")

        for i, product in enumerate(products, start=1):
            print("=" * 60)
            print(f"Product {i}")
            print(f"Name   : {product['name']}")
            print(f"Price  : {product['price']}")
            print(f"URL    : {product['url']}")
            print(f"Image  : {product['image']}")

        print("=" * 60)

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
