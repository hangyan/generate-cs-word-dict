#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from time import sleep

__author__ = 'Hang Yan'

URL_PREFIX = "http://stackoverflow.com/tags?tab=popular&page="
TOTAL_PAGE = 1275

PAR = 8


def chunks(l, n):
    """Split list l in N-sized chunks"""
    return [l[i:i + n] for i in xrange(0, len(l), n)]


def get_page_source(url):
    import urllib2
    user_agent = """Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US)
  AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3"""
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    return page


def get_soup(url):
    from bs4 import BeautifulSoup
    page = get_page_source(url)
    return BeautifulSoup(page, "html.parser")


def process_tag_one_token(tag, token):
    if token in tag:
        return [x for x in tag.split(token) if x]
    return [tag]


def process_tag(tag):
    r = []
    l = process_tag_one_token(tag, '-')
    for item in l:
        r.extend(process_tag_one_token(item, '.'))
    l = [strip_others(x) for x in l]
    return [x for x in l if x]


def strip_others(tag):
    out = filter(str.isalpha, str(tag))
    if len(out) <= 1:
        return ''
    return out


def uniq(l):
    return list(set(l))


def get_tags(index):
    url = URL_PREFIX + str(index)
    soup = get_soup(url)
    tags = soup.find_all("td", attrs={'class': 'tag-cell'})
    result = {
        index: []
    }

    data = []
    for item in tags:
        tag = item.find('a').get_text()
        l = process_tag(tag)
        data.extend(l)
    result[index] = uniq(data)
    return result


def process(chunk, get_tags):
    from multiprocessing.dummy import Pool as ThreadPool
    pool = ThreadPool(len(chunk))
    return pool.map(get_tags, chunk)


def load_last_state():
    try:
        with open('state.json') as json_file:
            data = json.load(json_file)
            return data['last_index'], data['old']
    except:
        pass
    return 1, {}


def save_current_state(index, data):
    out = {
        'last_index': index,
        'old': data
    }
    with open('state.json', 'w') as outfile:
        json.dump(out, outfile)


def main():
    index, all = load_last_state()
    print "Load from last index: {}".format(index)
    for chunk in chunks(range(index, TOTAL_PAGE + 1), PAR):
        print "CHUNK: {}".format(chunk[0])
        try:
            sleep(1)
            result = process(chunk, get_tags)

            for item in result:
                for k, v in item.items():
                    all[k] = v
        except Exception as e:
            print e
            save_current_state(chunk[0], all)
            return
    l = []
    for k, v in all.items():
        l.extend(v)
    l = sorted(uniq(l))
    print "Total: {}".format(len(l))
    print "Write to file: 'dict'"

    with open('dict', 'wb') as fp:
        for item in l:
            fp.write("%s\n" % item)


if __name__ == '__main__':
    main()
