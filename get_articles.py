from bs4 import BeautifulSoup
import requests
import re

def clean_articles(concert_list):
    results = []
    
    for idx, event in enumerate(concert_list[:10], start=0):
            article_link = event['href']

            article_page = requests.get(article_link)
            article_page.raise_for_status()
            article_page_soup = BeautifulSoup(article_page.text, 'html.parser')

            article_title = article_page_soup.find('h1').get_text(strip=True)
            article_description = article_page_soup.find('div', class_='concert_details_description_description_inner')

            if article_description:

                article_description_text = article_description.get_text(strip=True)

                sentences = re.split(r'(?<=[.!?])\s+', article_description_text)

                clean_sentences = [
                        sentence for sentence in sentences 
                        if not re.search(r'(http[s]?://\S+|www\.\S+)', sentence)
                    ]
                clean_description = ' '.join(clean_sentences)

            results.append({
                    'title': article_title,
                    'description': clean_description,
                    'link': article_link
                })
    return results
