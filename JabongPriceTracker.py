import lxml.html as html
import requests
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from robobrowser import RoboBrowser
from requests import Session
session = Session()
session.verify = False

url = input("Enter the url : ")
br = RoboBrowser(parser = 'lxml')

import re
br.open(url)

brand = str(br.select('span.brand')[0])
pat = r'.*>(.*)<.*'
res = re.match(pat, brand)
brand = res.group(1)

product = str(br.select('span.product-title')[0])
res = re.match(pat, product)
product = res.group(1)

mrp = str(br.select('span.standard-price')[1])
res = re.match(pat, mrp)
mrp = int(res.group(1))

sp = str(br.select('span.actual-price')[0])
res = re.match(pat, sp)
sp = int(res.group(1))

wallet = str(br.select('span.wallet-title')[0])
res = re.match(pat, wallet)
wallet = res.group(1)

offer = str(br.select('span.wallet-desc')[0])
res = re.match(pat, offer)
offer = res.group(1)

print('Product Brand : %s'%(brand))
print('Product Description : %s'%(product))
print('MRP of the product : %d'%(mrp))
print('Current Selling Price : %d'%(sp))
print('%s %s'%(wallet,offer))

print('-------------------------Tracking Started-------------------------')

xaxis = []
actual_price = []
selling_price = []

matplotlib.rc('font', size=8)
matplotlib.rc('font', family='sans-serif')
c=1
while(c<48):
    br.open(url)
    
    mrp = str(br.select('span.standard-price')[1])
    res = re.match(pat, mrp)
    mrp = int(res.group(1))

    sp = str(br.select('span.actual-price')[0])
    res = re.match(pat, sp)
    sp = int(res.group(1))
    
    wallet = str(br.select('span.wallet-title')[0])
    res = re.match(pat, wallet)
    wallet = res.group(1)

    offer = str(br.select('span.wallet-desc')[0])
    res = re.match(pat, offer)
    offer = res.group(1)
    
    actual_price.append(mrp)
    selling_price.append(sp)
    
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    xaxis.append(t)
    print('Current Price : %d  %s %s        Time : %s' %(sp, wallet, offer, t))
    time.sleep(900)
    c+=1

x_pos = np.arange(len(xaxis))
plt.title('Price Variation')
plt.xlabel('Time')
plt.ylabel('Price')
plt.xticks(x_pos, xaxis, rotation=90)
plt.plot(xaxis, actual_price , label='original')
plt.plot(xaxis, selling_price , label='discounted', marker='o')
plt.legend()
plt.grid(color='lightblue', linestyle='-.')
plt.tight_layout()
plt.savefig('output.png', dpi=600)
