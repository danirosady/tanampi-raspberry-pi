#! /usr/bin/env python
# -*- coding: utf-8 -*-

#import RPi.GPIO as GPIO
import datetime
import csv
import spidev
import time

# Establish SPI device on Bus 0,Device 0
spi = spidev.SpiDev()
spi.open(0,0)

def main():
    collectData(0).getData()

class collectData(object):
    def __init__(self, channel):
        self.channel = channel

        #check valid channel
        if ((self.channel>7)or(self.channel<0)):
            return -1

    
    def getData(self): 
        while True:
            # Preform SPI transaction and store returned bits in 'r'
            self.r = spi.xfer([1, (8+self.channel) << 4, 0])
            
            self.adcOut = ((self.r[1]&3) << 8) + self.r[2]
            self.percent = 100 - int(round((self.adcOut - 300)/7.24))
            self.date = datetime.datetime.now().strftime("%B %d %Y")
            self.time = datetime.datetime.now().strftime("%H:%M")
            self.weekday = datetime.datetime.today().weekday()
            
            with open('data.csv', 'a') as out:
                fileWriter = csv.writer(out, delimiter= ',')
                fileWriter.writerow([self.adcOut, self.percent, self.date, self.time, self.weekday])
            time.sleep(60)


