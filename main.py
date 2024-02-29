#!/usr/bin/env python

import multiprocessing
import cgi
import os
import os.path
import signal

import getdata

print "Content-type: text/html"
print
print "<html>"
print "<head>"
print "</head>"
print "<body>"

processes = []
form = cgi.FieldStorage()

print "Selamat datang di Sistem Irigasi Pintar."

def abort():
    f = open('RUN.txt', 'r')
    process = f.readline()
    process = filter(None, process.split(","))
	
    for p in process:
        os.kill(int(p), signal.SIGQUIT)
	
    f.close()
    os.remove('RUN.txt')
		
def main():
    if not os.path.isfile("RUN.txt"):
        f = open('RUN.txt', 'w+')
	
        for func in [getdata.main]:
            processes.append(multiprocessing.Process(target=func))
            processes[-1].start()

        for p in processes:
            f.write(str(p.pid))
            f.write(",")
        f.close()

        choice = raw_input("Tekan X untuk keluar: ")
        if choice == "X":
            abort()
    else:
        print "program sudah berjalan."
        if form.getvalue('offline') == "True":
            abort()
	
if __name__ == '__main__':
	main()
	

print "</body>"
print "</html>"
