__author__ = 'Ryan Soklaski'
import urllib2
from bs4 import BeautifulSoup
home = 'https://capcomprotour.com/'


def scrape_results_urls(schedule_url=home+'schedule/'):
    """ Returns list of urls for all CPT-event results pages.
        Parameters
        ----------
        schedule_url : str
         - CPT Schedule page url: 'https://capcomprotour.com/schedule/'
         """
    response = urllib2.urlopen(schedule_url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    return [i.get('href') for i in soup.find_all('a') if i.string == 'View Results']


def scrape_tourney_dates(offset, schedule_url=home+'/schedule/'):
    """ Returns list start-stop dates for CPT.
        Parameters
        ----------
        offset : int
         - Number of entries to skip before reaching completed events.
        schedule_url : str
         - CPT Schedule page url: 'https://capcomprotour.com/schedule/'"""
    response = urllib2.urlopen(schedule_url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    return [str(i.contents[1].strip()) for i in soup.find_all('br')[offset:]]


def scrape_url_standings(url):
    """ Returns list of top-16 standings from CPT-event results page.
        Parameters
        ----------
        url : str
         - CPT-event page url."""
    response = urllib2.urlopen(url)
    soup = BeautifulSoup(response.read(), 'html.parser')

    # scrape tournament name
    tourney_title = soup.title.contents[0].split(' Results')[0]
    # scrape tournament results table
    data = []
    for entry in soup.find_all('tr')[1:]:
        data.append([i.contents[0] for i in entry.contents[::2]])
    return tourney_title, data  # tourney-title, (Rank, PlayerName, Char, Pts)


def scrape_standings_tree(standing_url):
    """ Returns list of tag, name, rank, player-page-url
        Parameters
        ----------
        standing_url : str
         - CPT Full Standings page url"""
    # example url: 'https://capcomprotour.com/full-standings/?season=2015&lang='

    # stand_url_list = ['https://capcomprotour.com/full-standings/?season=2015&lang=',
    #                  'https://capcomprotour.com/full-standings/page/2/?season=2015&lang=en-us',
    #                 'https://capcomprotour.com/full-standings/page/3/?season=2015&lang=en-us',
    #                 'https://capcomprotour.com/full-standings/page/4/?season=2015&lang=en-us',
    #                 'https://capcomprotour.com/full-standings/page/5/?season=2015&lang=en-us',
    #                 'https://capcomprotour.com/full-standings/page/6/?season=2015&lang=en-us']
    player_rank_link = []
    response = urllib2.urlopen(standing_url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    for bit in soup.findAll('tr')[1:]:
        rank = int(bit.td.text)

        name = str(bit.a.text)
        spl = name.split('|')
        if len(spl) == 2:
            tag, name = spl
        else:
            tag, name = None, spl[0]

        url = str(bit.a.get('href'))
        player_rank_link.append([(tag, name), rank, url])
    return player_rank_link


def scrape_player_country(player_page_url):
    """ Return country (string) that player hails from
        Parameters
        ----------
        player_page_url : str"""
    # example url: https://capcomprotour.com/player/?player=7309&lang=en-us
    response = urllib2.urlopen(player_page_url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    return str(soup.findAll('p')[1].text)