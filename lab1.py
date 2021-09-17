import requests
r = requests.get('https://raw.githubusercontent.com/wuyifanevana/cmput404/master/lab1.py')
print(r.text)
