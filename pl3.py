import socket
from socket import *
# import requests
import sys
import socket
import http.client
import urllib.parse
import ssl
import re
from datetime import datetime


def requestTest():
    contents = requests.get("https://www.netbank.com/")
    print(contents.headers)
    # for test the answer


def httpRequest(serverName, path, port, sslNeed=0):
    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    if sslNeed:
        clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLSv1)
    clientSocket.connect((serverName, port))
    # serverip = clientSocket.getsockname()[0]
    serverip = socket.gethostbyname(serverName)
    clientport = clientSocket.getsockname()[1]
    clientip = clientSocket.getsockname()[0]
    sentence = bytes('GET ' + path + ' HTTP/1.0\r\nHost: ' + serverName + '\r\n\r\n', 'utf-8')
    clientSocket.send(sentence)
    modifiedSentence = clientSocket.recv(1024)
    # print(modifiedSentence.decode())
    stri = modifiedSentence.decode()
    output(stri, serverName, path, port, serverip, clientip, clientport)
    clientSocket.close()


def output(stri, host, path, serverport, serverip, clientip, clientport):
    strs = stri.split('\n')
    print('URL Requested: ' + host + path)
    print('IP Address, # Port of the Server: ' + str(serverip) + ', ' + str(serverport))
    print('IP Address # Port of this Client: ' + str(clientip) + ', ' + str(clientport))
    code = strs[0].split(' ')
    print('Reply Code: ' + code[1])
    print('Reply Code Meaning: ' + strs[0].split(' ', 2)[-1])
    if int(code[1]) > 399 or int(code[1]) < 299:
        print('Date:' + changeTime(re.findall('Date.+', stri)[0].split(' ', 1)[-1]))
    last = re.findall('Last-Modified.+', stri)
    last = 'not specified' if len(last) is 0 else changeTime(last[0].split(' ', 1)[-1])
    print('Last-Modified: ' + last)
    move = re.findall('Location.+', stri)
    if (len(move) is not 0):
        print('Moved to: ' + move[0].split(' ', 1)[-1])


def changeTime(string):
    weeks = ['Mon,', 'Tue,', 'Wed,', 'Thu,', 'Fri,', 'Sat,', 'Sun,']
    months = ['Jan', 'Fab', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    date = string.split(' ')
    mon = date[2]
    year = date[3]
    day = int(date[1])
    time = date[4]
    week = date[0]
    hours = time.split(':')
    hour = hours[0]
    min = hours[1]
    sec = hours[2]
    hour = int(hour) + 10
    if hour > 24:
        day += 1
        if (mon in ['Jan', 'Mar', 'May', 'Jul', 'Aug', 'Oct', 'Dec'] and day == 32) or (
                mon in ['Apr', 'Jun', 'Sep', 'Nov'] and day == 31) or (mon == 'Feb' and day == 29):
            day = 1
            ind = months.index(mon)
            ind = ind + 1 if index < 11 else 0
            mon = months[ind]
        hour -= 24
        index = weeks.index(week)
        index = index + 1 if index < 6 else 0
        week = weeks[index]
    return week + ' ' + str(day) + ' ' + mon + ' ' + year + ' ' + str(hour) + ':' + min + ':' + sec + ' AEST'


if __name__ == '__main__':
    print('HTTP Protocol Analyzer, Written by YingLuo Peng, s4425909')
    print('-------------------------www.csiro.au/awap/---------------------------')
    httpRequest('www.csiro.au', '/awap/', 80)
    print('-------------------------abc.net.au/---------------------------')
    httpRequest('abc.net.au', '/', 80)
    print('-------------------------www.abc.net.au/news/sport---------------------------')
    httpRequest('www.abc.net.au', '/news/sport/', 80)
    print('-------------------------www.abc.net.au/missing---------------------------')
    httpRequest('www.abc.net.au', '/missing', 80)
    print('-------------------------www.netbank.com/---------------------------')
    httpRequest('www.netbank.com', '/', 443, 1)
