import plantower
from datetime import datetime
import time
import csv
import spidev
import Adafruit_DHT

pt = plantower.Plantower(port= '/dev/serial0') #sets serial port for plantower sensor

spi = spidev.SpiDev() 
spi.open(0,0)

sensor = Adafruit_DHT.DHT11 #set sensor type 
gpio = 17 #sets sensor pin

def analogInput(channel): 
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1, (8+channel)<<4, 0]) 
  data = ((adc[1]&3) << 8) + adc[2] 
  return data

def write_csv(data):
  with open('pms.csv', 'a') as outfile:
    writer = csv.writer(outfile) 
    writer.writerow(data)

while True:
  humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio) 
  try:
    output = analogInput(0) 
    pt.mode_change(0) 
    time.sleep(5) 
    pt.set_to_wakeup() 
    time.sleep(30) #time for the sensor to start reading accurate values
    PM = pt.read_in_passive() 
    pt.set_to_sleep() #turns off fan when not being used to save power and lengthen experiment time
  except: plantower.plantower.PlantowerException("No message received") 
    else:
      pass
    write_csv([PM, output, temperature, humidity])  #writes output data to csv file
    time.sleep(300)
