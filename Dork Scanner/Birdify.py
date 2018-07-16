'''

- Birdify Tool coded by @Subn3t
- Version: 3.0
- GitHub: https://github.com/gdsubn3t/
- Finds and Scans url using a sinlge dork or a file list.
- You can use this code, but please give credits.
- Have fun and stay legal!

'''


import argparse, requests, re, sys, bs4, time
from bs4 import BeautifulSoup as bs
from modules import sql

HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
WHITE = '\033[97m'
RED = '\033[91m'
ENDC = '\033[0m'
BRIGHT = '\033[1m'
EBRIGHT = '\033[0m'

banner = '''%s%s
                 ,
     ,_     ,     .'<_   > %sBirdify Tool%s
    _> `'-,'(__.-' __<   > %s%sMake hacking simple with Dorks!%s%s
    >_.--(.. )  =;`      > %s%sCoded by %s%sSubnet%s
         `V-'`'\\/`       > %s%sVersion: %s%s1.2%s

''' %( BRIGHT, RED, BLUE, RED, EBRIGHT, WHITE, BRIGHT, RED, EBRIGHT, WHITE, BRIGHT, BLUE, RED, EBRIGHT, WHITE, BRIGHT, YELLOW, EBRIGHT)


global sub 
print(banner)
parser = argparse.ArgumentParser(description="Birdify dork analizer Tool")
parser.add_argument("-d", "--dork", help="dork to use")
parser.add_argument("-l", "--list", help="list file of dork to use")
parser.add_argument("-s", "--scan", help="scan the url found", choices=["sql", "xss"])
args = parser.parse_args()

def extract_dork(file, scan):
	# read the dork wordlist 
	with open(file, 'r') as f:
		for dork in f.readlines():
			main(dork.strip('\r').strip('\n'), scan)

def logger(data):
	# save the links in a .txt file
	f = open("birdify_log.txt", 'a+')
	f.write(data + "\n")
	f.close()

def main(dork, scan):
	open("birdify_log.txt", 'a+').close()
	global sub_pages
	sub_pages = []
	if not dork == '':
		print("%sUsing the dork:%s%s" %(WHITE, BLUE, dork))
		url = 'https://search.yahoo.com/search?p=%s' %(dork)
		search(url, scan)
		if sub == True:
			print('%sSearching in sub pages...' %(WHITE))
			time.sleep(1)
			for page in sub_pages:
				search(page, scan)

def search(url, scan):
	try:
		source = requests.get(url).text
		soup = bs(source, 'lxml') # parse the page's source code
		for link in soup.find_all('a'): # get all 'a' tags
			link = link.get('href')
			log = open("birdify_log.txt", 'r')
			if link[:4] == 'http':
				if "cc.bing" in link:
					pass
				elif "yahoo" in link:
					if link[:14] == 'https://search':
						sub_pages.append(link)
				else:
					if not link + "\n" in log:
						if scan == 'sql':
							sql.sqlscan(link)
						else:
							print('%sFound %s%s'%(GREEN, WHITE, link)) # prints out the links
						logger(link)
			log.close()

	except KeyboardInterrupt:
		exit()

if args.dork:
	sub = True
	main(args.dork, args.scan)
if args.list:
	sub = False
	extract_dork(args.list, args.scan)
rgv[2])
