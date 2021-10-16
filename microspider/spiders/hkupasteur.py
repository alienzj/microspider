import scrapy


class HkupasteurSpider(scrapy.Spider):
    name = 'hkupasteur'
    allowed_domains = ['http://www.hkupasteur.hku.hk']
    start_urls = ['http://www.hkupasteur.hku.hk/']

    def start_requests(self):
        urls = []
        for i in range(0, 228, 6):
            urls.append(f"http://www.hkupasteur.hku.hk/index.php/Teaching/News/list/P{i}/")

        for url in urls:
            print(f"Accessing {url}")
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page_number = response.url.split("/")[-2]
        print(page_number)
        filename = f"data/hkupasteur/Teaching/News/{page_number}.html"

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        for news in response.css('div.news'):
            yield {
                'publication_year': news.css('p.publication_year:text').get(),
                'title': news.css()
            }