from bs4 import BeautifulSoup
import requests
from bs4 import XMLParsedAsHTMLWarning
import warnings
import html
from app_database import *
from scraper.text_analysis import *
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def parse_description_cdata(description_cdata:str):
    """This functions parses the content inside the description CDATA tag"""
    inner_soup = BeautifulSoup(description_cdata, "html.parser")
    link = inner_soup.find('a').get('href')
    description = inner_soup.find('p')
    return [link,description]

def parse_content_cdata(content_cdata:str):
    """This functions parses the content inside the 'content' CDATA tag"""
    inner_soup = BeautifulSoup(content_cdata, "html.parser")
    main_articles = inner_soup.find_all('p')
    complete_article = ""
    for item in main_articles:
        complete_article += item.get_text()
    return complete_article

def structure_data(articles):
    """This function structures the data parsed from the webpages into a dictionary.
    It takes a list of <item> tags as input and returns a list of dictionaries as output"""
    final_articles = []
    for article in articles:
        article_data = {}
        article_data['title'] = article.find('title').get_text()
        article_data['link'] = parse_description_cdata(article.description.text)[0]
        article_data['description'] = parse_description_cdata(article.description.text)[1].get_text()
        article_data['publication date'] = article.find('pubdate').get_text()
        article_data['content'] = parse_content_cdata(article.find('content:encoded').text)
        final_articles.append(article_data)

    return final_articles

def fetch_page(URL):
    """This function fetches a webpage and returns the
    contents of that page"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(URL, headers=headers,timeout = 30)
        response.raise_for_status() 
        return response.content
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return True
        
        


def final_function():
    """This function wraps everything and will be called to create a new json file of the articles."""
    i = 1
    page_not_found_error = False
    while not page_not_found_error:
        web_page = fetch_page(f"https://orientalnewsng.com/category/energy/nigeria-oil-gas-news/feed/?paged={i}&")
        if web_page is True:
            #check if webpage is available and break out of loop if not.
            page_not_found_error = True

        else:
            decoded_web_page = html.unescape(web_page.decode("utf-8", errors="replace"))
            main_soup = BeautifulSoup(decoded_web_page,features='html.parser')
            #find all item tags (item tags contain all article data)
            items = main_soup.find_all('item')
            i += 1
            articles = structure_data(items)
            for article in articles:
                compliance = classify_oil_gas_regulation(article['content'])
                add_article(title=article['title'],link=article['link'],description=article['description'],pub_date=article['publication date'],content=article['content'],compliance=compliance)
        if i == 3:
            #Break out of loop if on the 3rd page
            page_not_found_error = True
        

final_function()