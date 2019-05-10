import re

import requests
from bs4 import BeautifulSoup
from apps.whippet import utils

class JcinkPage():
    def __init__(self, url):
        self.url = url
        self.soup = self.set_soup()

    def set_soup(self):
        page = requests.get(self.url)
        return BeautifulSoup(page.text, 'html.parser')

    @property
    def raw_posts(self):
        tag = 'div'
        attrs = {'class': 'postcolor'}
        return self.soup.find_all(tag, attrs)

    @property
    def users(self):
        tag = 'span'
        attrs = {'class': 'postdetails'}
        # [1::2] b/c posdetails include miniprofile
        return self.soup.find_all(tag, attrs)[1::2]

    @property
    def current_page(self):
        tag = 'span'
        attrs = {'class': 'pagination_current'}
        p = self.soup.find(tag, attrs)
        # parent doesn't exist on unipage
        if not p:
            return 1
        else:
            return int(p.get_text())

    @property
    def user_order(self):
        return [self.user_name(i) for i in self.users]

    def parsed_post(self, post):
        # ignores style children
        return (''.join(
            text for text in post.find_all(text=True)
            if text.parent.name != "style"
        ))

    def user_name(self, user):
        user_text = user.get_text()
        return user_text.split('posted')[-2].strip()

class JcinkThread():
    def __init__(self, url):
        self.url = url
        self.set_pages()
        self.set_titles()

    def set_pages(self):
        # instantiate all pages at beginning
        pages = []
        for i in range(self.n_pages):
            url = '{pref}&st={st}'.format(pref=self.url, st=20*i)
            pages.append(JcinkPage(url))
        self.pages = pages

    def set_titles(self):
        page = JcinkPage(self.url)
        tag = 'span'
        title_attrs = {'class': 'topic-title'}
        subtitle_attrs = {'class': 'topic-desc'}

        raw_title = page.soup.find(tag, title_attrs)
        self.title = raw_title.text

        raw_subtitle = page.soup.find(tag, subtitle_attrs)
        # subtitles start with ', ' by default
        self.subtitle = raw_subtitle.text[2:]

    @property
    def n_pages(self):
        page = JcinkPage(self.url)
        tag = 'a'
        last_attrs = {'class': 'pagination_last'}
        norm_attrs = {'class': 'pagination_page'}
        pagination_last = page.soup.find(tag, last_attrs)
        if pagination_last:
            num = int(re.search('\d+', pagination_last.get('title')).group(0))
        elif page.soup.find(tag, norm_attrs):
            all_found_pages = page.soup.find_all(tag, norm_attrs)
            pages = {int(i.get_text()) for i in all_found_pages}
            num = max(set(pages))
        else:
            num = 1
        return num

    def ordered_posts(self):
        posts = []
        users = []
        for page in self.pages:
            raw_posts = page.raw_posts
            users.extend(page.user_order)
            for raw_post in raw_posts:
                post = page.parsed_post(raw_post)
                posts.append(post)
        return posts, users
