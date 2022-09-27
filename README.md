# simple-proxies-manager
- I made a simple proxy manager in Python based on a Queue of proxies.
- The logic is simple, after a proxy is used, it gets back at the end of queue.
- Also, the system has a rotation logic, when the system finds a banning message in body of response, a new proxy is used.
- The system is wrapped on requests library so you can use any methods with any arguments from requests.
