from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re

list = ["https://anonymsms.com/number/447553799569/","https://anonymsms.com/number/13473938756/","https://anonymsms.com/number/447423127256/",
        "https://anonymsms.com/number/995571085688/","https://anonymsms.com/number/16463273211/"]

fNumber = urlopen(list)
bsobj = soup(fNumber.read())

for link in bsobj.findAll('+'):
    if "href" in link.attrs:
        print(link.attrs['href'])

bsobj.findAll('+')