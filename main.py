import requests
from pprint3x import pprint
import re
from time import sleep
import random


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36 '
    }


def get_page(url):
    try:
        response = requests.get(url, headers=headers).json()
    except Exception as e:
        print(e)
    articles_ids_list = response['articleIds']
    return articles_ids_list


def parse_page(article_id):
    api_link = f'https://habr.com/kek/v2/articles/{article_id}/?fl=ru&hl=ru'
    try:
        response = requests.get(api_link, headers=headers)
    except Exception as e:
        print(e)
    return response.json()


def get_content(article_content):
    content_list = []
    content_list.append(article_content['titleHtml'])
    content_list.append(article_content['textHtml'])
    for tags in article_content['hubs']:
        content_list.append(tags['title'])
    return content_list


def search_keywords(list_keywords, artice_text):
    flag = False
    for keyword in list_keywords:
        for line in artice_text:
            pattern = rf'\b{keyword}\b'
            match = re.search(pattern, line)
            if match and flag == False:
                flag = True
    return flag


assert search_keywords(['на'], ['на дереве', 'yes'])
assert not search_keywords(['на'], ['под деревом', 'no'])


def main(keywords):
    return_info = {}
    url = 'https://habr.com/kek/v2/articles/most-reading?fl=ru&hl=ru'
    list_articles = get_page(url)
    for article in list_articles:
        article_content = parse_page(article)
        sort_content_article = get_content(article_content)
        if search_keywords(keywords, sort_content_article):
            return_info[article] = {}
            return_info[article]['article_name'] = article_content['titleHtml']
            return_info[article]['time_published'] = article_content['timePublished']
            return_info[article]['url'] = f"https://habr.com/ru/company/{article_content['hubs'][0]['alias']}/blog/{article}/"
        delay_time = random.randint(1, 10)
        sleep(delay_time)
    return return_info


if __name__ == "__main__":
    res = main(['что'])
    pprint(res)