import sys
import pycurl
import validators
from io import BytesIO
from lxml import etree
from html.parser import HTMLParser


class KeywordCounterCrawler:

    def __init__(self, url):
        super(KeywordCounterCrawler, self).__init__()
        self.keywords = []
        self.data = []
        self.body = ""
        self.tree = False
        self.url = url
        self.curl = self.get_curl()

    def reset_data(self):
        self.keywords = []
        self.data = []
        self.body = ""
        self.tree = False

    def set_url(self, url):
        self.reset_data()
        self.url = url

    def get_curl(self):
        curl = pycurl.Curl()
        curl.setopt(curl.URL, self.url)
        curl.setopt(curl.HEADER, 1);
        curl.setopt(curl.FOLLOWLOCATION, 1)
        curl.setopt(curl.USERAGENT, 'KEYWORD COUNTER')
        curl.setopt(curl.REFERER, self.url)
        curl.setopt(curl.COOKIEFILE, '')
        return curl

    def read_keywords(self):
        result = []
        keywords = self.tree.xpath("//meta[@name='Keywords' or @name='keywords']")
        if len(keywords) > 0:
            result = keywords[0].get("content")
            result = result.split(',')
            for key, word in enumerate(result):
                result[key] = word.strip()
        return result

    def calculate_data(self):
        result = []
        body_content = self.tree.xpath("//body")
        if len(body_content) > 0:
            body_content = str(etree.tostring(body_content[0]))
            stripper = KeywordCounterStripper()
            stripper.feed(body_content)
            body_content = stripper.get_data()
            for keyword in self.keywords:
                result.append([keyword, str(body_content.count(keyword))])
        return result

    def analyse(self):
        self.keywords = self.read_keywords()
        self.data = self.calculate_data()

    def get_encoding(self, html):
        result = 'utf-8'
        tmp_tree = etree.HTML(str(html).lower())
        encoding = tmp_tree.xpath("//meta[@http-equiv='content-type']/@content")
        if len(encoding) > 0 and len(encoding[0].split("charset=")) > 1:
            result = encoding[0].split("charset=")[1]
        return result

    def download(self):
        result = False
        self.body = ""
        if validators.url(self.url):
            buffer = BytesIO()
            self.curl.setopt(self.curl.WRITEDATA, buffer)
            self.curl.perform()
            result = buffer.getvalue()
            encoding = self.get_encoding(result)
            try:
                self.body = result.decode(encoding)
                self.tree = etree.HTML(result.decode(encoding))
            except:
                self.body = str(result)
                self.tree = etree.HTML(str(result))
            self.analyse()
        return result


class KeywordCounterStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
