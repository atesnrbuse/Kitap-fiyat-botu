# kitap fiyat takip botu

import requests
from bs4 import BeautifulSoup
import numpy as np
import json

class Book:
    def __init__(self, title, price, stock):
        self.title = title
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "stock": self.stock
                    }

    def __str__(self):
        return f"{self.title} - £{self.price} -{self.stock}"

def get_page_content(hedef_url):
    try:
        response = requests.get(hedef_url, timeout = 10)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"Sayfa alınamadı. Durum kodu: {response.status_code}")
            return None
    except requests.exceptions.RequestException as error:
        print(f"Bağlantı hatası oluştu: {error}")
        return None
    
def clean_price(price_text):
    cleaned_price = price_text.replace("£", "").replace("Â", "").strip()
    return float(cleaned_price)

def parse_books(html_content):

    soup = BeautifulSoup(html_content, "html.parser")
    book_items = soup.find_all("article", class_= "product_pod")
    books = []

    for item in book_items:

        title = item.h3.a["title"]
        price_text = item.find("p",class_="price_color").text
        price = clean_price(price_text)
        stock = item.find("p",class_="instock availability").text.strip()
        book = Book(title, price, stock)
        books.append(book)
    return books

def page_url_generator(total_pages):
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"

    for page_number in range(1, total_pages + 1):
        yield base_url.format(page_number)

def scrape_books(total_pages):

    all_books = []
    for url in page_url_generator(total_pages):
        print(f"Veri çekiliyor:{url}")
        html_content = get_page_content(url)

        if html_content is not None:
            books = parse_books(html_content)
            all_books.extend(books)
    return all_books

def analyze_prices(books):
    if len(books) == 0:
        print("Analiz yapılacak kitap bulunamadı")
        return None
    prices = np.array([book.price for book in books]) 
    
    analysis = {
        "total_books": len(books),
        "average_price": float(np.mean(prices)),
        "min_price": float(np.min(prices)),
        "max_price": float(np.max(prices)),
        "std_price": float(np.std(prices))
    }
    return analysis

def find_books_under_price(books, max_price):
    cheap_books= []
    for book in books:
        if book.price <= max_price:
            cheap_books.append(book)
    return cheap_books

def save_books_to_json(books, filename):

    book_dicts= []

    for book in books:
        book_dicts.append(book.to_dict())

    with open(filename,"w",encoding="utf-8") as file:
        json.dump(book_dicts, file, ensure_ascii = False, indent=4)
    print(f"Kitap verileri{filename} dosyasına kaydedildi.")

def save_report(analysis, cheap_books, filename):
    with open(filename,"w",encoding="utf-8") as file:
        file.write("KİTAP FİYAT TAKİP BOTU RAPORU\n")
        file.write("="*35+"\n\n")

        file.write("GENEL ANALİZ\n")
        file.write(f"Toplam kitap sayısı:{analysis['total_books']}\n")
        file.write(f"Ortalama fiyat: £{analysis['average_price']:.2f}\n")
        file.write(f"En düşük fiyat: £{analysis['min_price']:.2f}\n")
        file.write(f"En yüksek fiyat: £{analysis['max_price']:.2f}\n")
        file.write(f"Standart sapma: £{analysis['std_price']:.2f}\n\n")

        file.write("UCUZ KİTAPLAR\n")

        if len(cheap_books) == 0:
            file.write("Belirlenen fiyatın altında kitap bulunamadı.\n")
        else:
            for book in cheap_books:
                file.write(str(book)+"\n")
        print(f"Rapor{filename} dosyasına kaydedildi.")

def main():

    print("Kitap Fiyat Takip Botu Başlatıldı")
    total_pages = 3
    max_price = 20

    books = scrape_books(total_pages)

    if len(books) == 0:
        print("Hiç kitap bulunamadı.")
        return

    analysis = analyze_prices(books)
    cheap_books = find_books_under_price(books,max_price)

    save_books_to_json(books, "books.json")
    save_report(analysis, cheap_books, "report.txt")

    print("\nAnaliz Özeti")
    print(f"Toplam kitap:{analysis['total_books']}")
    print(f"Ortalama fiyat: £{analysis['average_price']:.2f}")
    print(f"En ucuz kitap fiyatı: £{analysis['min_price']:.2f}")
    print(f"En pahalı kitap fiyatı: £{analysis['max_price']:.2f}")
    print(f"\n£{max_price} altındaki kitap sayısı:{len(cheap_books)}")

    for book in cheap_books[:10]:
        print(book)

if __name__ == "__main__":
    main()