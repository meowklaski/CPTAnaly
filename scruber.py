__author__ = 'Ryan Soklaski'


def scrub_player_data(rank, name, chars, pts):
    """ Cleans entry from top-16 standings.
        Parameters
        ----------
            data : tuple
             - element of data from: scraper.scrape_url_standings(url) -> title, [(rank0, name0, chars0, pts0), ...]
        Returns
        -------
        rank : int
            - Player rank in tournament.
        tag : str
            - Player's sponsor tag. tag=None if no sponsor is listed.
        name : str
            - Player name. No surrounding whitespace.
        chars : list
            - String entry for each character used by player in tournament.
        pts : int
            - Number of CPT points earned by player.
            """
    rank = int(''.join([i for i in rank if i.isdigit()]))  # 1st -> 1, ...,13th -> 13
    spl = name.split('|')
    if len(spl) == 2:
        tag, name = spl
    else:
        tag, name = None, spl[0]
    chars = [str(i.strip()) for i in chars.split('/')]
    pts = int(pts)
    return rank, tag, str(name.strip()), chars, pts


def scrub_tourney_title(name):
    """ Remove (CPTA Qualifier) and 2015 suffixes from CPT-event title.
        Parameters
        ----------
        name : str
            - CPT-event name taken from scraper.scrape_url_standings(url)

        Returns
        -------
        status : str
            - 'Premier', 'Ranked', or None
        title : str
            - CPT-event name with no suffix decorators or surrounding whitespace."""
    tmp = name.split(':')
    if len(tmp) == 2:
        status = str(tmp[0].split()[0].capitalize())
        name = tmp[1]
    else:
        status = None
        name = tmp[0]
    return status, str(name.rstrip('(CPTA Qualifier)').rstrip('2015').strip())