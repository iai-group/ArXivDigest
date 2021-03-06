# -*- coding: utf-8 -*-
"""This module contains the the methods related to scraping articles from arXiv.
To only scrape the metadata from the articles in the rss-stream use the
harvestMetaDataRss method.
It's also possible to scrape articles between any two dates,
to accomplish this use the get_records_by_date method."""
import datetime

import requests

__author__ = 'Øyvind Jekteberg and Kristian Gingstad'
__copyright__ = 'Copyright 2020, The arXivDigest project'

import urllib
import xml.etree.ElementTree as ET
from time import sleep
from urllib.request import urlopen

import feedparser

OAI = '{http://www.openarchives.org/OAI/2.0/}'
ARXIV = '{http://arxiv.org/OAI/arXiv/}'


def prepare_record(record):
    """Formats the data to a dictionary structure that is easy to work with."""
    if record.find(OAI + 'header').get('status', None) == 'deleted':
        return {}
    info = record.find(OAI + 'metadata').find(ARXIV + 'arXiv')
    result = {'title': info.find(ARXIV + 'title').text.replace('\n', ' '),
              'description': info.find(ARXIV + 'abstract').text.replace('\n', ' '),
              'id': info.find(ARXIV + 'id').text,
              'categories': info.find(ARXIV + 'categories').text.split(),
              }
    doi = info.find(ARXIV + 'doi')
    comments = info.find(ARXIV + 'comments')
    licenses = info.find(ARXIV + 'license')
    journal = info.find(ARXIV + 'journal-ref')

    # check that element is not None before trying to access the text
    result['doi'] = doi.text if doi is not None else None
    result['comments'] = comments.text if comments is not None else None
    result['license'] = licenses.text if licenses is not None else None
    result['journal'] = journal.text if journal is not None else None

    authors = []
    for author in info.find(ARXIV + 'authors'):
        a = {}
        firstname = author.find(ARXIV + 'forenames')
        a['firstname'] = '' if firstname is None else firstname.text
        a['lastname'] = author.find(ARXIV + 'keyname').text
        a['affiliations'] = []
        for affiliation in author.findall(ARXIV + 'affiliation'):
            a['affiliations'].append(affiliation.text)

        authors.append(a)
    result['authors'] = authors
    datestamp = record.find(OAI + 'header').find(OAI + 'datestamp')
    result['datestamp'] = datestamp.text
    return result


def get_records_by_date(start_date, end_date=None):
    """Scrapes the OAI-api for articles submitted from the n previous days."""
    base_url = 'http://export.arxiv.org/oai2'
    params = {'verb': 'ListRecords',
              'metadataPrefix': 'arXiv',
              'from': start_date}
    if end_date:
        params['until'] = end_date

    result = {}
    while True:
        r = requests.get(base_url, params=params)
        print('Fetching', r.url)
        if r.status_code == 503:
            time_out = int(r.headers.get('retry-after', 5))
            msg = '503: Have to wait before further requests. Retrying in {} seconds.'
            print(msg.format(time_out))
            sleep(time_out)
            continue

        # generate elementtree from responsedata
        root = ET.fromstring(r.text)
        # parse the response and add it to result
        for record in root.find(OAI + 'ListRecords').findall(OAI + 'record'):
            element = prepare_record(record)
            if element:
                result[element['id']] = element
        # If the xmlfile contains more than 1000 articles arXiv will add a
        # resumptiontoken to the response, if we already have all the articles
        # there will be no resumptiontoken and we can safely break
        token = root.find(OAI + 'ListRecords').find(OAI + 'resumptionToken')
        if token is None or token.text is None:
            break
        # update url to use resumptiontoken in the next request
        params = {'verb': 'ListRecords', 'resumptionToken': token.text}
    return result


def get_record(id):
    """Gets metadata for a single record."""
    url = 'http://export.arxiv.org/oai2?verb=GetRecord&identifier=oai:arXiv.org:%s&metadataPrefix=arXiv' % id
    print('Fetching', url)
    response = urlopen(url)
    root = ET.fromstring(response.read())
    record = root.find(OAI + 'GetRecord').find(OAI + 'record')
    return prepare_record(record)


def get_categories():
    """Returns a dict of all the main categories available with info."""
    url = 'http://export.arxiv.org/oai2?verb=ListSets'
    print('fetching', url)
    while True:
        try:
            response = urlopen(url)
        except urllib.error.HTTPError as e:
            if e.code == 503:
                timeOut = int(e.headers.get('retry-after', 30))
                print(
                    '503: Have to wait before further requests. Retrying in %d seconds.' % timeOut)
                sleep(timeOut)
                continue
            else:
                raise
        break
    root = ET.fromstring(response.read())
    categories = root.find(OAI + 'ListSets').findall(OAI + 'set')
    result = {}
    for category in categories:
        categoryID = category.find(OAI + 'setSpec').text
        categoryName = category.find(OAI + 'setName').text
        categoryInfo = {'name': categoryName}
        categoryID = categoryID.split(':')
        if len(categoryID) > 1:
            categoryInfo['masterCategory'] = categoryID[0].capitalize()
        result[categoryID[-1]] = categoryInfo

    return result


def get_id_from_rss():
    """Returns a set of all the article-ids found in the rss stream, which will
    be approximately the same as the articles uploaded the previous day."""
    rssUrl = 'http://export.arxiv.org/rss/'
    result = set()
    for category in get_categories():
        print('Fetching IDs from the %s rss-feed' % category)
        feed = feedparser.parse(rssUrl + category)
        for entry in feed['entries']:
            id = entry['link'].split('abs/')[1]
            result.add(id)
    return result


def harvest_metadata_rss():
    """This function will return the metadata from all the articles present
    in any of the arXiv rss-streams."""
    rss_ids = get_id_from_rss()
    yesterday = datetime.datetime.utcnow().date() - datetime.timedelta(days=1)
    articles = get_records_by_date(yesterday)
    result = {}
    for item in rss_ids:
        if item not in articles:  # download missing articles, if any
            element = get_record(item)
            result[element['id']] = element
        else:
            result[item] = articles[item]
    return result
