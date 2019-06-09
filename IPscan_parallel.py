#!/usr/bin/env python
# coding:utf-8
import subprocess
import datetime
import threading

hostname = "192.168.1"
file_name = "IPscan_parallel.txt"

full_response = {}
results = {}



class PingerThread (threading.Thread):
   def __init__(self, scan, ip_adress):
      threading.Thread.__init__(self)
      self.scan = scan
      self.ip_adress = ip_adress
   def run(self):
      #Ping the ip address
      ping_response = subprocess.Popen(["ping", "-a", self.ip_adress, "-n", '1'],   stdout=subprocess.PIPE).stdout.read()
      ping_response = ping_response.decode()
      full_response[self.scan] = ping_response
      stat = ""
      if ("unreachable"  in ping_response) :
         stat = "" + self.ip_adress + " unreachable"
      elif ("timed out"  in ping_response) : 
         stat = "" + self.ip_adress + " timed out"
      else :
         # host resolve
         host = "unknown"
         start_host_str = int(ping_response.find("Pinging")) + 8
         end_host_str   = int(ping_response.find("["+hostname)) - 1
         if ( ( start_host_str > 0 ) and (end_host_str > 0) ) :
            host = ping_response[start_host_str:end_host_str]            
         stat = "" + self.ip_adress + " [" + host + "] alive"
      results[self.scan] = stat


threads = {}
scans = range(1, 255)
for scan in scans :
   ip_address = str(hostname) + "." + str(scan)
   threads[scan] = PingerThread(scan, ip_address)
   threads[scan].start()

for scan in scans :    
   threads[scan].join()

    
with open(str(file_name), "w")as file:
   for scan in scans :    
      print(results[scan])
      file.write(results[scan]+"\n")
   for scan in scans :    
      file.write(full_response[scan]+"\n")
   
print("\n========summary========\n")
for scan in scans :   
   if ( results[scan].find("alive")  > 0 ) :
      print(results[scan])
print("\n")