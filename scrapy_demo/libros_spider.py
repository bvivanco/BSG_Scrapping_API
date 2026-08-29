"""
Demo de Scrapy — el mismo scraping de los scripts 13 y 14, en 25 líneas
=======================================================================
Capítulo 4 · Librerías

★ ESTO NO SE EJECUTA CON `python libros_spider.py` NI DESDE JUPYTER.
  Scrapy levanta su propio motor de eventos y necesita la terminal:

      pip install scrapy
      cd scrapy_demo
      scrapy runspider libros_spider.py -o ../salidas/libros_scrapy.csv

  Para explorar selectores ANTES de escribir el spider:
      scrapy shell "https://books.toscrape.com/"
      >>> response.css("article.product_pod h3 a::attr(title)").getall()
      >>> response.xpath("//p[@class='price_color']/text()").getall()

Compara con 14_paginacion_y_detalle.py: aquí no hay bucle while, ni time.sleep,
ni urljoin, ni pandas para guardar. Scrapy hace todo eso solo.
"""

import scrapy


class LibrosSpider(scrapy.Spider):
    name = "libros"
    start_urls = ["https://books.toscrape.com/"]

    # Scrapy sí respeta robots.txt y limita la velocidad, si se lo pides:
    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 1.0,           # el time.sleep(), pero automático
        "CLOSESPIDER_PAGECOUNT": 3,      # el MAX_PAGINAS, pero automático
        "USER_AGENT": "BSG-Curso-Scraping/1.0 (ejercicio academico)",
        "FEED_EXPORT_ENCODING": "utf-8-sig",
    }

    def parse(self, response):
        for libro in response.css("article.product_pod"):
            yield {
                "titulo": libro.css("h3 a::attr(title)").get(),
                "precio_gbp": libro.css("p.price_color::text").re_first(r"[\d.]+"),
                "rating": libro.css("p.star-rating::attr(class)").get().split()[-1],
                "url": response.urljoin(libro.css("h3 a::attr(href)").get()),
            }

        # La paginación: dos líneas. Scrapy encola la nueva URL y sigue solo.
        siguiente = response.css("li.next a::attr(href)").get()
        if siguiente:
            yield response.follow(siguiente, callback=self.parse)
