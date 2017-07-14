from selenium.webdriver.common.by import By
from .base import Base


class Example(Base):
    # Match
    menu = re.compile('')
    page = re.compile('')

    # Menu page
    episode = '#episode'
    episodes = []
    episode_name = '#episode_name'

    # View page
    image = '#image'
    next_page = '#next_page'
    next_episode = '#next_episode'
