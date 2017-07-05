import requests
from queue import Queue

proxies = ["61.183.8.51:3128",
			"175.155.24.19:808"]

invalidStringList = ["Inserisci i caratteri visualizzati nello spazio sottostante","To discuss automated access to Amazon data please contact","For automated access to price change or offer listing change events","Our systems have detected unusual traffic from your computer network","please type the characters below","Permission denied","Geben Sie die angezeigten",'hogy szokatlanul nagy a forgalom az oldalon','Validare acces pagina','Te rugam sa verifici pentru a continua','500 Service Unavailable Error','banned your IP', 'DDoS protection by CloudFlare', 'To continue, please type the characters below', 'your computer or network may be sending automated queries','Enter the characters you see below']

def isBanned(response):
	for keyword in invalidStringList:
		if keyword in response.text:
			print("Found banning phrase:{}".format(keyword))
			return True
	return False

def rotate(proxiesQueue, currentProxy):
	newProxy = proxiesQueue.get()
	proxiesQueue.put(currentProxy)
	proxy = proxy = { "http" : newProxy }
	return proxiesQueue, proxy
	

def loadProxiesToQueue():
	proxiesQueue = Queue()
	for proxy in proxies:
		proxiesQueue.put(proxy)
	return proxiesQueue

def test(url):
	proxiesQueue = loadProxiesToQueue()
	newProxy = proxiesQueue.get()
	proxy = { "http" : newProxy }
	print(proxy)
	response = requests.get(url, proxies = proxy)
	while isBanned(response):
		print("Making rotation")
		proxiesQueue, proxy = rotate(proxiesQueue, newProxy)
		print(proxy)
		response = requests.get(url, proxies = proxy)
	print("Success")


if __name__ == '__main__':
	url = "https://www.amazon.de/HP-Officejet-Multifunktionsdrucker-kompatibel-4800x1200/dp/B00VRNL4TA/ref=cm_cr_arp_d_product_top?ie=UTF8"
	for i in range(0,10):
		test(url)