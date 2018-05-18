import requests
import json
from bs4 import BeautifulSoup
import random
import time
import traceback
import os
import sys
import csv

"""
@author: Ademola Oyewale
saopayne@gmail.com
"""


class PlayReviews:

    def get_reviews(self, app_id):
        sort_by_helpfulness = '1'
        reviews = []
        page_num = 0
        is_last_page = False

        while is_last_page is False:
            if page_num % 3 == 0:
                time.sleep(random.random() + 1)
            (reviews_html_string, is_last_page) = self.fetch_reviews(app_id, page_num, sort_by_helpfulness)
            if len(reviews_html_string) > 0:
                reviews.extend(self.parse_reviews(reviews_html_string))
            page_num = page_num + 1
            print('Downloading reviews on page:', page_num)
        return reviews

    def fetch_reviews(self, app_id, page_num, sort_by):
        url = "https://play.google.com/store/getreviews"
        querystring = {"authuser": "0"}
        payload = {'reviewType': '0', 'pageNum': page_num, 'id': app_id, 'xhr': '1', 'reviewSortOrder': sort_by}
        response = requests.request("POST", url, data=payload, params=querystring)

        if len(response.content) > 4:
            response = response.content[4:]
            try:
                response = json.loads(response)
                if len(response) > 0:
                    if len(response[0]) == 4:
                        reviews_html = response[0][2]
                        if response[0][1] == 1:
                            is_last_page = False
                        else:
                            is_last_page = True
                        return reviews_html, is_last_page
                    else:
                        return '', True
                else:
                    return '', True

            except ValueError as e:
                traceback.print_exc()
                print("Fetch prevented by Google")
                return '', True
        else:
            return '', True

    def parse_reviews(self, reviews_html_string):

        soup = BeautifulSoup(reviews_html_string, 'html.parser')
        review_body_list = soup.findAll("div", {"class": "review-body"})
        review_author_list = soup.findAll("span", {"class": "author-name"})
        review_date_list = soup.findAll("span", {"class": "review-date"})
        review_title_list = soup.findAll("span", {"class": "review-title"})
        review_rating_list = soup.findAll("div", {"class": "tiny-star"})
        reviews = []
        data_path = 'data/'
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        writer = csv.writer(open('data/reviews.csv', 'a'))
        writer.writerow(['Title', 'Body:', 'Date', 'Author', 'Rating'])
        for i in range(len(review_body_list)):
            current_row = [review_title_list[i].text, review_body_list[i].text, review_date_list[i].text,
                           review_author_list[i].text,
                           review_rating_list[i]['aria-label']]
            writer.writerow(current_row)
            reviews.append(current_row)
        return reviews

    def fetch_and_write_reviews(self, application_id):
        self.get_reviews(application_id)
        return


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app_id = sys.argv[1]
        plr = PlayReviews()
        plr.fetch_and_write_reviews(app_id)
