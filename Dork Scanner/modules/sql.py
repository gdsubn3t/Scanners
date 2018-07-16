'''

- SQL Scanner coded by @Subn3t
- Telegram: @gxdlxk
- GitHub: https://github.com/gdsubn3t/
- You can use this code, but please give credits.
- Have fun and stay legal!


'''

import requests

WHITE = '\033[97m'
GREEN = '\033[92m'
RED = '\033[91m'

def sqlscan(url):
	vuln = False
	payloads = ['\'', '"']
	errors = ['You have an error in your SQL syntax', 'mysql_num_rows()']
	try:
		for payload in payloads:
			for error in errors:
				if error in requests.get(url + payload).text:
					vuln = True
		if vuln:
			print("%sFound SQL injection: %s%s" %(WHITE, GREEN, url))
		else:
			print("%sSQL injection not Found: %s%s" %(WHITE, RED, url))
	except KeyboardInterrupt:
		sys.close()
	except:
		pass
