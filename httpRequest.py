import urllib2
#from urllib.request import urlopen
import json


def basic_authorization(user, password):
    s = user + ":" + password
    return "Basic " + s.encode("base64").rstrip()


def submit_pull_request():
    url = 'http://www.csiro.au/awap/'
    params = {'title': 'My Title', 'body': 'My Boday'}
    req = urllib2.Request(url,
                          headers={
                              "Content-Type": "application/json",
                              "Accept": "*/*",
                              "User-Agent": "Myapp/Gunio",
                          }, data=json.dumps(params))
    f = urllib2.urlopen(req)
    print(f)


if __name__ == '__main__':
    submit_pull_request()
