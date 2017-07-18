import re
from .base import Base


class Test(Base):
    # Match
    menu = re.compile('test')
    page = re.compile('https://static\.runoob\.com/images/icon/html5\.png')

    # Menu page
    episode = '#episode'
    episodes = []
    episode_name = '#episode_name'

    # View page
    image = 'img'
    next_page = None
    next_episode = None
