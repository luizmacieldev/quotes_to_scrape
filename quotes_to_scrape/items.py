import scrapy
import re
from itemloaders.processors import TakeFirst, MapCompose, Join


def remove_new_lines(text):
    return text.strip().replace('\n','')
    
def remove_incomplete_hyperlinks(text):
    return re.sub(r'\.More: http://.*', '', text)

class TagItem(scrapy.Item):
    tag = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )

class AuthorItem(scrapy.Item):
    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    birth_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    birth_place = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_new_lines,remove_incomplete_hyperlinks),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )

class QuoteItem(scrapy.Item):
    _id = scrapy.Field()
    phrase = scrapy.Field(
        output_processor=TakeFirst()
    )
    tags = scrapy.Field()  
    author = scrapy.Field() 
