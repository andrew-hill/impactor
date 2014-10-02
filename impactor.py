#!/usr/bin/env python

import logging
import urllib2
import re
import pickle

# http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup
# https://code.google.com/p/prettytable/
from prettytable import PrettyTable


class Impactor(object):
    BASE_URL_PREFIX=r'http://www.citefactor.org/journal-impact-factor-list-'
    BASE_URL_SUFFIX=r'.html'
    URL_REGEX_PREFIX=r'http://www\.citefactor\.org/journal-impact-factor-list-'
    URL_REGEX_SUFFIX=r'_?[A-Z]?\.html'

    def __init__(self, journal_db_file=None, year=2014):
        logging.debug('journal_db_file={}, year={}'.format(journal_db_file, year))

        self.year = year
        self.journal_db_file = journal_db_file
        self.journal_data = None
        self.matches = set()

        self.base_url = self.BASE_URL_PREFIX + str(year) + self.BASE_URL_SUFFIX
        self.url_regex = self.URL_REGEX_PREFIX + str(year) + self.URL_REGEX_SUFFIX
        self.re = re.compile(self.url_regex)
        assert self.re.match(self.base_url)
        assert self.re.match(self.BASE_URL_PREFIX + str(year) + '_A' + self.BASE_URL_SUFFIX)

        self.load()
        self.save()

    def match(self, search_terms):
        # If no terms specified, show all entries
        if search_terms is None or len(search_terms) == 0:
            for j in self.journal_data.values():
                self.matches.add(j['ISSN'])
        # Otherwise do search
        issn_re = re.compile(r'\d{4}-\d{4}')
        for s in search_terms:
            if issn_re.match(s):
                self.matches.add(s)
            else:
                for j in self.journal_data.values():
                    if j['JOURNAL'].lower().find(s.lower()) >= 0:
                        self.matches.add(j['ISSN'])

    def print_table(self, sort_field='JOURNAL'):
        if len(self.matches) == 0:
            print 'No matches found.'
            return
        matches = list(self.matches)
        headers = self.journal_data[matches[0]].keys()
        logging.debug(headers)
        t = PrettyTable(headers, sortby=sort_field)
        #from prettytable import PLAIN_COLUMNS
        #t.set_style(PLAIN_COLUMNS)
        for j in matches:
            t.add_row(self.journal_data[j].values())
        print t


    def load(self):
        # Try to load from file
        if self.journal_db_file is not None:
            try:
                with open(self.journal_db_file, 'rb') as f:
                    self.journal_data = pickle.load(f)
                    logging.debug('loaded journals from {}'.format(self.journal_db_file))
            except:
                pass
        # If cannot load from file, load from URL
        if self.journal_data is None:
            self.journal_data = self.get_all_journal_data()

    def save(self):
        if self.journal_db_file is not None:
            try:
                with open(self.journal_db_file, 'wb') as f:
                    pickle.dump(self.journal_data, f, -1)
                    logging.debug('saved journals to {}'.format(self.journal_db_file))
            except:
                pass

    def get_all_urls(self, base_url=None):
        if base_url is None:
            base_url = self.base_url
        main_page_content = urllib2.urlopen(base_url).read()
        soup = BeautifulSoup(main_page_content)
        soup.prettify()  # necessary?
        return [base_url,] + [anchor['href'] for anchor in soup.find_all('a', href=self.re)]

    def get_journal_table(self, url):
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
        soup.prettify()  # necessary?
        t = soup.table
        caption_re = re.compile(r'^Impact Factor ' + str(self.year))
        while t is not None:
            if t.caption is None or t.caption.string is None or caption_re.match(t.caption.string) is None:
                t = t.find_next()
                continue
            return t

    def get_table_headers(self, table):
        return [str(x.string) for x in table.tr.find_all('td')]

    def get_journal_data(self, table):
        headers = self.get_table_headers(table)
        journals = dict()
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            j = dict( zip(headers, [str(x.string) for x in cells] ) )
            logging.debug('importing: {}'.format(j))
            journals[j['ISSN']] = j
        return journals

    def get_all_journal_data(self):
        journals = dict()
        for url in self.get_all_urls():
            table = self.get_journal_table(url)
            journals.update(self.get_journal_data(table))
        logging.info('imported {} journal entries from citefactor.org database'.format(len(journals)))
        return journals


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', '-y', default=2014, type=int)
    parser.add_argument('--db', default=None, type=str, help='file to load/save journal data')
    parser.add_argument('search', nargs='*', help='journal ISSNs')
    parser.add_argument('--debug', '-d', default=False, action='store_true')
    parser.add_argument('--sort', '-s', default='JOURNAL', help='sort by column')
    args = parser.parse_args()

    # Logging setup
    if args.debug is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.debug(args)

    i = Impactor(year=args.year, journal_db_file=args.db)
    i.match(args.search)
    i.print_table(args.sort)
