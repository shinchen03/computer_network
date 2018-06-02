import socket
from socket import *
import dnslib
from dnslib import *
from tkinter import *


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("DNS")
        self.pack(fill=BOTH, expand=1)
        quitButton = Button(self, text="quit", command=self.client_exit)
        quitButton.place(x=700, y=550)

    def client_exit(self):
        exit()


def predns():
    t.delete(1.0, END)
    dns("A")
    dns("AAAA")


def dns(qtype):
    text = ""
    dnsAddress = dnsname.get()
    testName = qname.get()
    if qtype is "PTR":
        text += "IP:\n" + testName + "\n"
        strs = testName.split(".")
        testName = ""
        for st in strs:
            testName = st+"."+testName
        testName += "in-addr.arpa"
    q = dnslib.DNSRecord.question(testName, qtype)
    data = q.pack()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)
    client_socket.connect((dnsAddress, 53))
    client_socket.send(data)
    r_data, r_address = client_socket.recvfrom(512)
    r = dnslib.DNSRecord.parse(r_data)
    print(r)
    if qtype is "A":
        text += "Host Name:\n" + testName + "\n"
        for s in r.rr:
            if s.rtype is 1:
                text += "IPV4:\n" + str(s.rdata) + "\n"
            if s.rtype is 5:
                text += "CNAME:\n" + str(s.rdata) + "\n"
    if qtype is "AAAA":
        for s in r.rr:
            if s.rtype is 28:
                text += "IPV6:\n" + str(s.rdata) + "\n"
    if qtype is "PTR":
        for s in r.rr:
            text += "Host name:\n" + str(s.rdata) + "\n"
    if qtype is "MX":
        text += "Host Name:\n" + testName + "\n"
        for s in r.rr:
            text += "MX:\n" + str(s.rdata) + "\n"
    t.insert(INSERT, text)
    client_socket.close()


def reverse():
    t.delete(1.0, END)
    dns("PTR")


def mx():
    t.delete(1.0, END)
    dns("MX")


def clear():
    t.delete(1.0, END)


def close():
    exit()


if __name__ == '__main__':
    root = Tk()
    root.geometry("550x400")
    app = Window(root)
    Tops = Frame(root, width=400, height=50, relief=SUNKEN)
    Tops.pack(side=TOP)
    f = Frame(root, width=400, height=300, relief=SUNKEN)
    f.pack(side=BOTTOM)
    top = Label(Tops, font=('arial', 16), text="DNS request", relief=SUNKEN)
    top.grid(row=0, column=0)
    # -------------------------------------------------------------------------------------------
    qname = StringVar()
    dnsname = StringVar()
    l1 = Label(f, font=('arial', 10, 'bold'), text="Enter a hostname or domain name:        ", anchor="w")
    l1.grid(row=1, column=1)
    t1 = Entry(f, font=('arial', 10, 'bold'), textvariable=qname, insertwidth=4)
    t1.grid(row=1, column=2)
    l2 = Label(f, font=('arial', 10, 'bold'), text="Enter a DNS name:                                  ", anchor="w")
    l2.grid(row=2, column=1)
    t2 = Entry(f, font=('arial', 10, 'bold'), textvariable=dnsname, insertwidth=4)
    t2.grid(row=2, column=2)
    b1 = Button(f, padx=8, pady=5, font=('arial', 10, 'bold'), width=10, text="Send Request", command=predns).grid(
        row=3,
        column=2)
    b2 = Button(f, padx=8, pady=5, font=('arial', 10, 'bold'), width=10, text="Reverse", command=reverse).grid(
        row=3,
        column=1)
    b3 = Button(f, padx=8, pady=5, font=('arial', 10, 'bold'), width=10, text="MX", command=mx).grid(
        row=3,
        column=0)
    t = Text(f, height=20, width=40)
    t.grid(row=4, column=1)
    b4 = Button(f, padx=8, pady=5, font=('arial', 10, 'bold'), width=10, text="Clear", command=clear).grid(row=4,
                                                                                                           column=2)
    root.mainloop()
    # -------------------------------------------------------------------------------------------
    # dns1("eait.uq.edu.au", "A")
    # dns1("eait.uq.edu.au", "AAAA")
    # dns1('microsoft.com', "A")
    # dns1('microsoft.com', "AAAA")
