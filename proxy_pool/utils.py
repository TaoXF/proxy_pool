import requests
import logging; logging.basicConfig(level=logging.INFO)

from requests.exceptions import ConnectionError


def get_page(url):

	headers = {
        'user-agent':  'mozilla/5.0 (macintosh; intel mac os x 10_13_1) applewebkit/537.36 (khtml, like gecko) chrome/65.0.3325.181 safari/537.36',
	}
	logging.info('Start Crawling %s' %url)
	try:
		r = requests.get(url, headers=headers)
		if 200 == r.status_code:
			logging.info('The request is successful %s' %url)
			return r.text
	except ConnectionError:
		logging.info('Crawling Failed %s' %url)

if __name__ == '__main__':
	url = 'http://www,66ip.cn/87.html'
	get_page(url)