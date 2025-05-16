import scrapy
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from quotes_to_scrape.items import QuoteItem, AuthorItem, TagItem

def join_url(base_url, relative_url):
    return urljoin(base_url, relative_url)

class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            loader = ItemLoader(item=QuoteItem(), selector=quote)

            # Carrega a frase
            loader.add_css('phrase', 'span.text::text')

            # Carrega as tags
            tags = quote.css('div.tags a::text').getall()
            tag_urls = quote.css('div.tags a::attr(href)').getall()

            # Preencher a lista de tags como TagItem
            tag_items = []
            for tag, url in zip(tags, tag_urls):
                tag_loader = ItemLoader(item=TagItem())
                tag_loader.add_value('tag', tag)
                tag_loader.add_value('url', join_url(response.url, url))
                tag_items.append(tag_loader.load_item())

            loader.add_value('tags', tag_items)

            # Obter o nome do autor e o link para sua página
            author_name = quote.css('small.author::text').get()
            author_relative_url = quote.css('span a::attr(href)').get()

            # Se há um link do autor, faz uma nova requisição para a página do autor
            if author_relative_url:
                author_url = join_url(response.url, author_relative_url)
                request = scrapy.Request(
                    author_url,
                    callback=self.parse_author,
                    meta={'quote_loader': loader, 'author_name': author_name},
                    errback=self.handle_error,
                    dont_filter=True
                )
                yield request

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_author(self, response):
        # Recupera o loader de quotes
        loader = response.meta['quote_loader']

        # Carrega os dados do autor
        author_loader = ItemLoader(item=AuthorItem(), response=response)
        author_loader.add_value('name', response.meta['author_name'])
        author_loader.add_css('birth_date', 'span.author-born-date::text')
        author_loader.add_css('birth_place', 'span.author-born-location::text')
        author_loader.add_css('description', 'div.author-description::text')

        author_loader.add_value('url', response.url)

        # Adiciona os dados do autor ao campo `author` do item de quote
        loader.add_value('author', author_loader.load_item())

        # Retorna o item
        yield loader.load_item()

    def handle_error(self, failure):
        # Captura erros HTTP, como o status 308
        response = failure.value.response

        # Se for um redirecionamento (código 308)
        if response.status == 308:
            redirected_url = response.headers.get('Location', None)
            if redirected_url:
                redirected_url = response.urljoin(redirected_url.decode('utf-8'))
                self.logger.info(f"Redirecionado para: {redirected_url}")
                yield scrapy.Request(redirected_url, callback=self.parse_author, meta=failure.request.meta)
        else:
            self.logger.error(f"Erro HTTP inesperado: {response.status}")
