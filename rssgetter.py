#!/usr/bin/python
from lxml import etree, html
import urllib2, urlparse, datetime

def download(url):
	parsed = etree.parse(url)
	links = parsed.findall(".//item/link")
	for link in links:
			retrieve_images(link.text)
def retrieve_images(url):
	parsed = html.parse(url)
	links = parsed.findall(".//a[@href]")
	unique_id = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S:%f ")
	for link in links:
		rel = link.get("href")
		if rel.endswith(".jpg") or rel.endswith(".jpeg") or rel.endswith(".png"):
				lastslash = rel.rfind("/")
				filename = rel[lastslash+1:]
				filename = unique_id  + filename
				fp = open(filename, "w")
				joinedurl = urlparse.urljoin(url,rel)
				print rel, joinedurl
				fp.write(urllib2.urlopen(joinedurl).read())
				fp.close()
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("URL")
	args = parser.parse_args()
	download(args.URL)

