import time
import socket
import struct
import select
import random
import sys
import math
import array

ERROR_DESCR = {
    1: ' - Note that ICMP messages can only be '
       'sent from processes running as root.',
    10013: ' - Note that ICMP messages can only be sent by'
           ' users or processes with administrator rights.'
}


def receive_ping(my_socket, time_sent, timeout):
    # Receive the ping from the socket.
    time_left = timeout
    while True:
        started_select = time.time()
        ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = time.time() - started_select
        if ready[0] == []:  # Timeout
            return

        rec_packet, addr = my_socket.recvfrom(1024)
        time_received = time.time()
        icmp_header = rec_packet[20:28]
        type, code, checksum, p_id, sequence = struct.unpack(
            'bbHHh', icmp_header)
        total_time_ms = (time_received - time_sent) * 1000
        if total_time_ms:
            return total_time_ms

        time_left -= time_received - time_sent
        if time_left <= 0:
            return


def ping(addr, timeout):
    IPPROTO_ICMP = socket.getprotobyname('icmp')
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, IPPROTO_ICMP)
    icmp_header = struct.pack('!BBHHH', 8, 0, 0, 1, 1)
    icmp_payload = 'Hello, World!'
    csum = checkSum(icmp_header + icmp_payload)
    icmp_header = struct.pack('!BBHHH', 8, 0, csum, 1, 1)
    packet = icmp_header + icmp_payload
    while packet:
        sent_bytes = sock.sendto(packet, (host, 0))
        packet = packet[sent_bytes:]
    return receive_ping(sock, time.time(), timeout)


def checkSum(msg):
    msg_short_len = len(msg) // 2 * 2
    total = 0
    for i in range(0, msg_short_len, 2):
        total += (ord(msg[i + 1]) << 8) + ord(msg[i])
    if len(msg) % 2 != 0:
        total += ord(msg[-1])
    while (total >> 16) > 0:
        total = (total & 0xffff) + (total >> 16)
    total = total >> 8 | (total << 8 & 0xff00)
    return ~total & 0xffff


if __name__ == '__main__':
    Hosts = []
    Hosts.append("google.com")
    Hosts.append("uq.edu.au")
    Hosts.append("nist.gov")
    Hosts.append("not.correct.au")
    Hosts.append("us.dd.imdb.com")
    for host in Hosts:
        # multiple_ping(host)
        a = 0
        count = 3
        for i in range(count):
            try:
                IP = socket.gethostbyname(host)
            except socket.gaierror:
                print('Not a valid host name' + '(' + host + ')')
                break
            delay = ping(host, 2)
            if delay is None:
                print('Request timed out for ' + host)
                break
            else:
                a = delay + a
        average_ms = str(round(a / count, 1))
        if delay is not None:
            print(str(count) + ' PINGs to ' + host + '(' + IP + ')')
            print('replies received with average ' + average_ms + 'ms,')
