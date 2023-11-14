import requests
from bs4 import BeautifulSoup as BS
import csv


def parser():
    with open("date.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Name",
                "State",
                "Price",
                "Discounted price",
                "Link",
            )
        )
    url = input("Введите URL с сайта https://telemart.ua/ ")
    r = requests.get(url)
    soup = BS(r.text, "html.parser")
    page_total = soup.find("li", class_="page-item last")
    if page_total:
        page_total = int(page_total.text.strip())
    else:
        page_total = 1
    page = 1
    while page_total >= page:
        r = requests.get(f"{url}?page={page}")
        soup = BS(r.text, "html.parser")
        products = soup.find_all("div", class_="product-item__inner product_wrapper")
        page += 1
        for product in products:
            title = product.get("data-prod-name")
            link = product.find("a", class_="product-item__pic__img").get("href")
            avail = product.find("div", class_="product-status product-status_in-stock")
            if avail:
                avail = avail.text.strip()
            else:
                avail = "Нет в наличии"
            price = product.find("div", class_="product-cost product-cost_new")
            if price:
                old_price = product.find(
                    "div", class_="product-cost product-cost_old"
                ).text.strip()
                price = price.text.strip()
            else:
                price = product.find("div", class_="product-cost")
                if price:
                    price = price.text.strip()
                    old_price = price
                else:
                    price = str(None)
                    old_price = str(None)
            with open("date.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        avail,
                        old_price,
                        price,
                        link,
                    )
                )


if __name__ == "__main__":
    parser()
