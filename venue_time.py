from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime


def getVenueTime(article_page_soup):
    venue_link_tag = article_page_soup.find('a', class_='info_sidebar_component_content_title')

    if venue_link_tag:
        venue_page_url = venue_link_tag['href']
        venue_response = requests.get(venue_page_url)

        if venue_response.status_code == 200:
            venue_soup = BeautifulSoup(venue_response.content, 'html.parser')
            location_details = venue_soup.find_all('span', class_='venue_details_location_detail')

            if location_details:
                detailed_location = " ".join([detail.get_text(strip=True) for detail in location_details if detail.get_text(strip=True)])
                location = detailed_location if detailed_location else location

    event_datetime = None
    time_tag = article_page_soup.find('div', class_='concert_details_spec_content')       
    if time_tag:
        date_match = re.search(r'\d{2}/\d{2}/\d{4}', time_tag.get_text())
        time_tag_span = time_tag.find('span', class_='concert_details_date_time')
                
        if date_match and time_tag_span:
            event_date = date_match.group()  # Extracts the date in 'dd/mm/yyyy' format
            event_time = time_tag_span.get_text(strip=True)  # Extracts the time (e.g., '19:00')
            # Combine date and time into a single datetime object
            event_datetime_str = f"{event_date} {event_time}"
            event_datetime = datetime.strptime(event_datetime_str, '%d/%m/%Y %H:%M')

    return location, event_datetime
