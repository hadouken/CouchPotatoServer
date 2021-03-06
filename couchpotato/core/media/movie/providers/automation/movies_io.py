from couchpotato.core.event import fireEvent
from couchpotato.core.helpers.rss import RSS
from couchpotato.core.helpers.variable import tryInt, splitString
from couchpotato.core.logger import CPLog
from couchpotato.core.media.movie.providers.automation.base import Automation

log = CPLog(__name__)

autoload = 'MoviesIO'


class MoviesIO(Automation, RSS):

    interval = 1800

    def getIMDBids(self):

        movies = []

        enablers = [tryInt(x) for x in splitString(self.conf('automation_urls_use'))]

        index = -1
        for rss_url in splitString(self.conf('automation_urls')):

            index += 1
            if not enablers[index]:
                continue

            rss_movies = self.getRSSData(rss_url, headers = {'Referer': ''})

            for movie in rss_movies:

                nameyear = fireEvent('scanner.name_year', self.getTextElement(movie, 'title'), single = True)
                imdb = self.search(nameyear.get('name'), nameyear.get('year'), imdb_only = True)

                if not imdb:
                    continue

                movies.append(imdb)

        return movies


config = [{
    'name': 'moviesio',
    'groups': [
        {
            'tab': 'automation',
            'list': 'watchlist_providers',
            'name': 'moviesio',
            'label': 'Movies.IO',
            'description': 'Imports movies from <a href="http://movies.io">Movies.io</a> RSS watchlists',
            'options': [
                {
                    'name': 'automation_enabled',
                    'default': False,
                    'type': 'enabler',
                },
                {
                    'name': 'automation_urls_use',
                    'label': 'Use',
                },
                {
                    'name': 'automation_urls',
                    'label': 'url',
                    'type': 'combined',
                    'combine': ['automation_urls_use', 'automation_urls'],
                },
            ],
        },
    ],
}]
