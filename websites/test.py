import re
from .base import Base


class Test(Base):
    # Match
    menu = re.compile('.*menu.*')
    page = re.compile('.*episode.*')

    # Menu page
    episode = '.episode'
    episodes = []
    episode_name = '#episode_name'

    # View page
    image = 'img'
    next_page = None
