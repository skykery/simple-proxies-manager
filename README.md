# simple-proxies-manager
### I made a simple proxy manager in Python based on a Queue of proxies.
### The logic is simple, after a proxy is used, it gets back at the end of queue.
### Also, the system has a rotation logic, when in body of response finds a banning message, the system is changing the proxy used.
#### The system is wraped on requests library so you can use any methods with any arguments from requests.
