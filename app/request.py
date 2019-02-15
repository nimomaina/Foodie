import urllib.request, json
from .models import Articles, News

# getting api key


api_key = None
base_url = None
articles_url = None

# getting the news base url


def configure_request(app):
    global api_key, base_url, articles_url
    api_key = app.config['NEWS_API_KEY']
    base_url = app.config['NEWS_API_BASE_URL']
    articles_url = app.config['ARTICLES_BASE_URL']


def get_news(category):
    '''function that gets the json response to the url request
    '''
    get_news_url = base_url.format(category, api_key)
    print(get_news_url)

    with urllib.request.urlopen(get_news_url) as url:
        get_news_data = url.read()
        get_news_response = json.loads(get_news_data)

        news_results = None

        if get_news_response['sources']:
            news_results_list = get_news_response['sources']
            news_results = process_results(news_results_list)

    return news_results


def process_results(news_list):
    '''
    '''

    news_results = []
    for news_item in news_list:
        name = news_item.get('name')
        url = news_item.get('url')
        country = news_item.get('country')
        description = news_item.get('description')
        category = news_item.get('category')
        id = news_item.get('id')

        news_object = News(name, url, description, country, category, id)
        news_results.append(news_object)

    return news_results
