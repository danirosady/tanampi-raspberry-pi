#! /usr/bin/python
# python program to communicate with an MCP3008.

# Import SpiDev wrapper and our sleep function
import spidev
import RPi.GPIO as GPIO
from time import sleep
import csv

#buka file konfigurasi
def baca_conf(x,y):
	with open ('conf.csv') as of:
		reader = csv.reader(of,delimiter=',')
		y_count = 0
		for n in reader :
			if y_count == y:
				cell = n[x]
				return cell
			y_count =+ 1
            
# Establish SPI device on Bus 0,Device 0
spi = spidev.SpiDev()
spi.open(0,0)

def getAdc(channel):
    #check valid channel
    if ((channel>7)or(channel<0)):
        return -1
    while True:
        
	#pengecekan data konfigurasi
	value1 = int(baca_conf(1,1))
	dur1 = int(baca_conf(0,1))

        # Perform SPI transaction and store returned bits in 'r'
        r = spi.xfer([1, (8+channel) << 4, 0])
        
        #Filter data bits from retruned bits
        adcOut = ((r[1]&3) << 8) + r[2]
        percent = int(round(adcOut/10.24))
        
	if percent > value1:
		print "tanaman terindikasi kekurangan air < %d " % value1
		sleep(0.5)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(14, GPIO.OUT)
		GPIO.output(14,False)
		print "sedang dilakukan penyiraman selama %s detik" % dur1
		sleep(dur1)
		GPIO.output(14, True)
		GPIO.cleanup()
		print "penyiraman berhasil"
		sleep(0.5)
		print "Sensor: {0:4} Presentasi: {1:3}% (Tanaman kering)".format (adcOut,percent)
		sleep(5)
		continue
	
	print "ADC Output: {0:4d} Percentage: {1:3}% (Kondisi Tanaman Normal)".format (adcOut,percent)
	sleep(5)

if __name__ == '__main__':
    getAdc(0)
