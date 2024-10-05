from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from get_articles import clean_articles
import os



app = Flask(__name__)


@app.get("/scrape")
def response():

    url = request.args.get('url', default='https://www.piletilevi.ee/eng/tickets/koik/', type=str)
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        concert_list = soup.find('div', class_='concertslist_page events events_count_3')

        return jsonify(
            clean_articles(concert_list)
            )


    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)