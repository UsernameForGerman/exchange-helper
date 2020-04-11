import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from celery.utils.log import get_task_logger

from django.conf import settings


logger = get_task_logger('scraping')


def make_headers(url):
    return {
        'Host': urlparse(url).hostname,
        'User-Agent':  ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'),
        'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                   '*/*;q=0.8'),
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'Accept-Encoding': 'gzip, deflate, sdch'
    }


class BrowserSession(object):
    def __init__(self, use_tor=True, use_fine_proxies=False):
        self.prev_request_time = 0
        self.cur_ip = ''
        self.session = None
        self.prev_request = None
        self.prev_url = None
        self.use_tor = use_tor
        self.use_fine_proxies = use_fine_proxies

    def get_soup(self, url):
        diff = settings.REQUEST_PERIOD - (time.time() - self.prev_request_time)
        if diff > 0:
            time.sleep(diff)

        if self.session is None:
            self.session = requests.Session()
            self.cur_ip = self._get_ip()

        else:
            if self._get_ip() != self.cur_ip:
                self.session = requests.Session()

        self.prev_request_time = time.time()

        r = self._request(url)
        soup = BeautifulSoup(r.text, 'lxml')

        self.prev_request = r
        self.prev_url = url
        return soup

    def _get_ip(self):
        return self._request('https://httpbin.org/ip').json()['origin']

    def _request(self, url):
        params = {}
        if self.use_tor:
            params['proxies'] = {
                'http': 'http://' + settings.TOR_PROXY,
                'https': 'https://' + settings.TOR_PROXY,
            }

        if self.use_fine_proxies:
            params['proxies'] = {
                'http': 'http://' + '',
                'https': 'https://' + '',
            }

        return self.session.get(
            url,
            headers=make_headers(url),
            **params
        )


def get_soup(url):
    logger.info('Requesting url "%s".', url)
    r = requests.get(url, headers=make_headers(url))
    return BeautifulSoup(r.text, 'lxml')