import requests
# from queue import Queue
from collections import deque


class proxyManager:
	def __init__(self):
		self.proxies = ["121.244.91.62:3128",
			            "104.154.205.214:1080",
			            "200.108.35.60:8087",
			            "180.250.159.67:80",
			            "67.205.179.195:3128",
			            "180.250.159.69:80",
			            "137.59.44.47:8080",
			            "199.193.188.94:80",
			            "195.190.124.202:8080",
			            "150.187.5.100:8080",
			            "96.9.250.117:8888",
			            "109.75.254.139:8080",
			            "176.62.77.212:8080",
			            "95.143.192.200:80",
			            "46.163.119.138:3128",
			            "185.145.129.106:8080",
			            "144.217.248.180:80",
			            "47.52.24.117:80",
			            "189.40.191.95:8080",
			            "199.193.188.84:80"]
						# https://free-proxy-list.net/
		self.invalidStringList = ["500 Internal Server Error","You’re not barking up the wrong tree",
									"not allowed to access this page","Our systems have detected unusual traffic from your computer network",
									"please type the characters below","Permission denied",
									"Geben Sie die angezeigten",'hogy szokatlanul nagy a forgalom az oldalon',
									'Validare acces pagina',
									'Te rugam sa verifici pentru a continua',
									'500 Service Unavailable Error',
									'banned your IP',
									'DDoS protection by CloudFlare',
									'To continue, please type the characters below',
									'your computer or network may be sending automated queries','Enter the characters you see below']
		# self.checkProxies()
		self.proxiesQueue = deque(self.proxies)
		self.maxRotations = len(self.proxies)
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
		self.proxyConnectionTimeout = 3


	def checkProxies(self):
		print("Checking proxies list...")
		testUrl = "https://httpbin.org/ip"
		connectionTimeout = 1
		for i,proxy in enumerate(self.proxies):
			try:
				response = requests.get(testUrl, proxies = {"http":proxy}, timeout=(connectionTimeout, 10) )
				print("Proxy {} from {}".format(i+1, len(self.proxies)))
			except Exception as e:
				print("Removing {} for {}".format(proxy, e))
				self.proxies.remove(proxy)


	def isBanned(self,response):
		for keyword in self.invalidStringList:
			if keyword in response.text:
				print("Found banning phrase:{}".format(keyword))
				return True
		return False

	def rotate(self, currentProxy):
		newProxy = self.proxiesQueue.popleft()
		self.proxiesQueue.append(currentProxy)
		proxy  = { "http" : newProxy }
		return proxy


	def makeRequest(self,*args,**kwargs):
		proxyError = False
		requestsMethod = kwargs.pop("requestsMethod")
		newProxy = self.proxiesQueue.popleft()
		proxy = { "http" : newProxy }
		print(proxy)
		kwargs["proxies"] = proxy
		response = requestsMethod(*args, **kwargs)
		# print(response.text)
		i = 1
		while self.isBanned(response) and i<= self.maxRotations or proxyError:
			print("Making rotation")
			proxy = self.rotate(newProxy)
			print(proxy)
			kwargs["proxies"] = proxy

			response = requestsMethod(*args, **kwargs)
			i += 1
		return response
		# print(response.text)


	def __getattr__(self,name):
		def handlerFunction(*args,**kwargs):
			if 'headers' not in kwargs:
				kwargs['headers'] = self.headers
			kwargs["requestsMethod"] = getattr(requests, name)
			kwargs["timeout"] = (self.proxyConnectionTimeout,25)
			try:
				response = self.makeRequest(*args, **kwargs)
			except Exception as e:
				print(e)
				response = requests.Response()

			return response
		return handlerFunction

#TODO: check for long response proxies or dead ones
"""
	a method is to check at init
	another one is to check at request
"""

if __name__ == '__main__':
	url = "http://ip-api.com/json"
	manager = proxyManager()

	for i in range(0,10):
		manager.get(url)
