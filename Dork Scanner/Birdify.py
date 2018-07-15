'''

- Birdify Tool coded by @Subn3t
- Version: 3.0
- GitHub: https://github.com/gdsubn3t/
- Finds and Scans url using a sinlge dork or a file list.
- You can use this code, but please give credits.
- Have fun and stay legal!

'''


import requests, re, sys, bs4, time
from bs4 import BeautifulSoup as bs


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

help = ''' Usage: %s -d <dork>
		   -f <dork wordlist>''' %(sys.argv[0])

def extract_dork(file):
	# read the dork wordlist 
	with open(file, 'r') as f:
		for dork in f.readlines():
			main(dork.strip('\r').strip('\n'))

def logger(data):
	# save the links in a .txt file
	with open("dumpurl_log.txt", 'a') as f:
		f.write(data + "\n")
		f.close()

def main(dork):
	global sub_pages
	sub_pages = []
	if not dork == '':
		print("%sUsing the dork:%s%s" %(WHITE, BLUE, dork))
		url = 'https://search.yahoo.com/search?p=%s' %(dork)
		search(url)
		if sub == True:
			print('%sSearching in sub pages...' %(WHITE))
			time.sleep(1)
			for page in sub_pages:
				search(page)

def search(url):
	try:
		source = requests.get(url).text
		soup = bs(source, 'lxml') # parse the page's source code
		for link in soup.find_all('a'): # get all 'a' tags
			link = link.get('href')
			log = open("dumpurl_log.txt", 'r')
			if link[:4] == 'http':
				if "cc.bing" in link:
					pass
				elif "yahoo" in link:
					if link[:14] == 'https://search':
						sub_pages.append(link)
				else:
					if not link + "\n" in log:
						print('%sFound %s%s'%(GREEN, WHITE, link)) # prints out the links
						logger(link)
			log.close()

	except KeyboardInterrupt:
		exit()

if __name__ == '__main__':
	print(banner)
	global sub
	if len(sys.argv) == 1:
		print(help)
		sys.exit()
	elif sys.argv[1] == '-d':
		sub = True
		main(sys.argv[2])

	elif sys.argv[1] == '-f':
		oksub = False
		extract_dork(sys.argv[2])
