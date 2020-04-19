import re

import requests
from bs4 import BeautifulSoup

from apps.jeeves import score as jeeves_score
from apps.secrets import USERNAME, PASSWORD

REMOVE_TAGS = [
    {'name': 'div', 'class_': 'ooc'},
    {'name': 'span', 'class_': 'edit'},
    {'name': 'a', 'alt': 'profile link'}
]


class JcinkBase:
    def __init__(self):
        self._login_credentials = {
            'UserName': USERNAME,
            'PassWord': PASSWORD
        }
        self._login_url = 'http://pokemonaudemus.jcink.net/index.php?act=Login&CODE=01'


class JcinkPage(JcinkBase):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.soup = self.get_soup()

    def get_soup(self):
        with requests.Session() as s:
            login_response = s.post(self._login_url, data=self._login_credentials)
            page_response = s.get(self.url)
        return BeautifulSoup(page_response.text, 'html.parser')

    def decompose_post(self, post):
        for tag_params in REMOVE_TAGS:
            tags = post.find_all(**tag_params)
            for t in tags:
                t.decompose()

    def parse_post(self, post):
        self.decompose_post(post)
        post = post.get_text(separator=' ', strip=True)
        post = re.sub('\n', '', post)
        return ' '.join(post.split())

    @property
    def posts(self):
        tag = 'div'
        attrs = {'class': 'postcolor'}
        posts_raw = self.soup.find_all(tag, attrs)
        return [self.parse_post(p) for p in posts_raw]

    @property
    def users(self):
        tag = 'div'
        attrs = {'class': 'cps-name'}
        users_raw = self.soup.find_all(tag, attrs)
        return [u.text for u in users_raw]

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
    def users_posts(self):
        return zip(self.users, self.posts)


class JcinkThread:
    def __init__(self, url):
        self.url = url
        self.pages = self.get_pages()

    @property
    def n_pages(self):
        page = JcinkPage(self.url)
        tag = 'a'
        last_attrs = {'class': 'pagination_last'}
        norm_attrs = {'class': 'pagination_page'}
        pagination_last = page.soup.find(tag, last_attrs)
        if pagination_last:
            num = int(re.search('Page: (\d+)', pagination_last.get('title')).group(1))
        elif page.soup.find(tag, norm_attrs):
            all_found_pages = page.soup.find_all(tag, norm_attrs)
            pages = {int(i.get_text()) for i in all_found_pages}
            num = max(set(pages))
        else:
            num = 1
        return num

    def get_pages(self):
        # instantiate all pages at beginning
        pages = {}
        for i in range(self.n_pages):
            url = '{pref}&st={st}'.format(pref=self.url, st=20*i)
            pages[i+1] = JcinkPage(url)
        return pages

    @property
    def title(self):
        # get page 1
        page = self.pages[1]
        tag = 'span'
        attrs = {'class': 'topic-title'}
        return page.soup.find(tag, attrs).text

    @property
    def subtitle(self):
        # get page 1
        page = self.pages[1]
        tag = 'span'
        attrs = {'class': 'topic-desc'}
        # subtitles starts with ', ' by default
        return page.soup.find(tag, attrs).text[2:]

    @property
    def all_users_posts(self):
        users = []
        posts = []
        for n in range(self.n_pages):
            page_users_posts = self.pages[n+1].users_posts
            for user, post in page_users_posts:
                users.append(user)
                posts.append(post)
        return users, posts

    @property
    def output(self):
        scorer = jeeves_score.ThreadScore(*self.all_users_posts)
        return scorer.printout()
