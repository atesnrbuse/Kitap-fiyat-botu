# Kitap Fiyat Takip & Analiz Botu (Web Scraper & Analyzer)

Bu proje; popüler web kazıma test platformu olan [Books to Scrape](https://books.toscrape.com) üzerindeki kitap verilerini dinamik olarak toplayan, Nesne Yönelimli Programlama (OOP) prensipleriyle modelleyen, **NumPy** kütüphanesiyle istatistiksel fiyat analizleri gerçekleştiren ve sonuçları yapılandırılmış formatlarda dışa aktaran kapsamlı bir Python otomasyon aracıdır.

---

## Projenin Amacı ve Özellikleri

- **Dinamik Web Kazıma (Pagination & Generator):** Python'ın `yield` tabanlı üreteç (generator) yapısını kullanarak sayfalar arası gezinir ve ağ kaynaklarını tüketmeden bellek dostu bir biçimde URL üretir.
- **Hata Yönetimi (Fault Tolerance):** `requests` isteklerinde zaman aşımı (`timeout`) ve ağ bağlantı hatalarına (`RequestException`) karşı dayanıklıdır. Olası bir sayfa kopmasında program çökmeden toplanan verilerle süreci tamamlar.
- **Veri Temizleme & Normalizasyon:** Kazınan ham fiyat metinlerindeki para birimi simgeleri (`£`) ve bozuk karakterler (`Â`) temizlenerek sayısal `float` tipine dönüştürülür.
- **OOP (Nesne Yönelimli Programlama):** Her kitap bir `Book` sınıfı nesnesi olarak modellenmiştir. Sınıf içi `to_dict()` ve `__str__()` metodları sayesinde veriler kolayca serileştirilebilir ve yazdırılabilir.
- **İstatistiksel Analiz (NumPy):** Toplanan fiyatlar üzerinden ortalama fiyat, en düşük fiyat, en yüksek fiyat ve standart sapma (volatilite) değerleri hesaplanır.
- **Bütçe Bazlı Filtreleme:** Belirlenen azami bütçenin (`max_price`) altında kalan kitapları hızlıca filtreler.
- **Çift Katmanlı Dışa Aktarım (Export):**
  - Yapılandırılmış tam veri tabanı için: `books.json`
  - Yönetici/Kullanıcı özeti ve ucuz kitap listesi için: `report.txt`

---

## Proje Mimarisi ve Kod Yapısı

| Fonksiyon / Sınıf | Görevi |
| :--- | :--- |
| `class Book` | Başlık, fiyat ve stok durumunu kapsülleyen nesne modeli. |
| `page_url_generator(total_pages)` | İstenilen sayfa sayısı kadar sayfa linki üreten generator fonksiyonu. |
| `get_page_content(hedef_url)` | Sayfa içeriğini güvenli bir şekilde `requests` ile indiren fonksiyon. |
| `clean_price(price_text)` | Ham fiyat dizesini temizleyip `float` sayıya dönüştüren yardımcı metot. |
| `parse_books(html_content)` | `BeautifulSoup` ile HTML DOM ağacını tarayarak `Book` nesneleri türeten parser. |
| `analyze_prices(books)` | `NumPy` dizileriyle temel tanımlayıcı istatistikleri çıkaran fonksiyon. |
| `find_books_under_price(books, max_price)` | Bütçe kriterine uygun kitapları filtreleyen metot. |
| `save_books_to_json(...)` | Kitap nesnelerini JSON formatında diske yazan fonksiyon. |
| `save_report(...)` | İstatistikleri ve ucuz kitapları biçimlendirilmiş bir metin raporu olarak kaydeden fonksiyon. |

---
