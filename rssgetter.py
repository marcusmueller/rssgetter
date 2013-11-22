#!/usr/bin/python
# this is GPL'ed code -- see LICENSE
from lxml import etree, html
import urllib2, urlparse, datetime

def download(url):
	parsed = etree.parse(url)
	links = parsed.findall(".//item/link")
	for link in links:
			retrieve_images(link.text)
def retrieve_images(url):
	parsed = html.parse(url)
	unique_id = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S:%f ")
	links = parsed.findall(".//a[@href]")
	for link in links:
		rel = link.get("href")
		print "considering", rel
		if rel.endswith(".jpg") or rel.endswith(".jpeg") or rel.endswith(".png"):
			print "ends with typical image suffix, downing it"
			retrieve_image(urlparse.urljoin(url,rel), unique_id)
		elif rel.startswith("http") or rel.find(":") == -1:
			print "asking server for type"
			joinedurl = urlparse.urljoin(url,rel)
			req = urllib2.Request(joinedurl)
			req.get_method = lambda : "HEAD"
			try:
				response = urllib2.urlopen(joinedurl, timeout=0.5)
				print response.headers.type 
				if response.headers.type.find('image') != -1:
					retrieve_image(joinedurl, unique_id)
			except:
				pass

def retrieve_image(url, uid = ""):
				lastslash = url.rfind("/")
				filename = url[lastslash+1:]
				filename = uid  + filename
				fp = open(filename, "w")
				fp.write(urllib2.urlopen(url).read())
				fp.close()
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("URL")
	args = parser.parse_args()
	download(args.URL)

