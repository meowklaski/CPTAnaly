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
