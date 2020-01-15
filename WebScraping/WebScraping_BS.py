import requests 
from bs4 import BeautifulSoup 
import lxml 
import html 

url = "https://www.myprotein.com/sports-nutrition/impact-whey-protein/10530943.html"
r = requests.get(url) 
html = r.text
soup = BeautifulSoup(html, "lxml")

formatted = []
matches = soup.find_all("div", class_="productDescription_synopsisContent")[4:5]

for match in matches:
    formatted += match.text.split("\n")
    
for item in formatted:
    print(item)
    print(" ")


reduced = []
for item in formatted[2:]:
    print("")
    print(item)
    reduced.append(item) 
len(reduced)

