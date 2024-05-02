import scrapy
from bs4 import BeautifulSoup


class BlogSpider(scrapy.Spider):
    name = 'narutospider'
    start_urls = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse(self, response):
        for href in response.css('div.smw-columnlist-container')[0].css('a::attr(href)').extract():
            extracted_data = scrapy.Request("https://naruto.fandom.com" + href,
                                            callback=self.parse_jutsu
                                            )
            yield extracted_data

        for next_page in response.css('a.mw-nextlink'):
            yield response.follow(next_page, self.parse)


    def parse_jutsu(self, response):

        jutsu_name = response.css('span.mw-page-title-main::text').get()
        print("jutsu:", jutsu_name)

        div_selector = response.css('div.mw-parser-output')[0]
        div_html = div_selector.extract()

        soup = BeautifulSoup(div_html).find('div')

        # Extract classification
        if soup.find('div',{'id':'quiz_module_desktop_placement_styles'}):
            soup.find('div',{'id':'quiz_module_desktop_placement_styles'}).decompose()
        
        if soup.find('h2',{'id':'quiz_module_destkop_header_styles'}):
            soup.find('h2',{'id':'quiz_module_destkop_header_styles'}).decompose()
        
        if soup.find('a',{'id':'quiz_module_desktop_link_styles'}):
            soup.find('a',{'id':'quiz_module_desktop_link_styles'}).decompose()

        jutsu_type=""
        if soup.find('aside'):
            aside= soup.find('aside')
            for cell in aside.find_all('div',{'class':'pi-data'}):
                if cell.find('h3'):
                    cell_name = cell.find('h3').text.strip()
                    if cell_name=='Classification':
                        jutsu_type = cell.find('div').text.strip()

            soup.find('aside').decompose()

        # Extract description
        jutsu_description = soup.text
        jutsu_description = jutsu_description.split('Trivia')[0].strip()

        yield dict(
            jutsu_name= jutsu_name,
            jutsu_type = jutsu_type,
            jutsu_description = jutsu_description,
        )



        
