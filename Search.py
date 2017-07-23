import urllib
import urllib2
import re
import webbrowser
import time
import Tkinter as tk
from bs4 import BeautifulSoup
from py_ms_cognitive import PyMsCognitiveWebSearch
    
API_KEY = "f696d60cdc8a4cc68a8f39f33bb150be"
search_term = raw_input("Please enter a search query: ")
limit = 10
search_array = search_term.split()
search_service = PyMsCognitiveWebSearch(API_KEY, search_term)
results = search_service.search(limit=limit, format='json')
x=0
height = 600
width = 600

top = tk.Tk()
C = tk.Canvas(top, bg="white", height=height+50, width=width)

freq_array = []
url_array = []

while x<limit:
    try:
        word_freq = [] 
        print results[x].url
        
        dirty_url = results[x].url[20:]

        clean_url = dirty_url[dirty_url.find("http"):]
        clean_url = clean_url[:clean_url.find("&p=DevEx")]
        clean_url = urllib.unquote(clean_url)

        try:
            response = urllib2.urlopen(clean_url)
        except urllib2.HTTPError:
            response = urllib2.urlopen("http://blank.org/")
            print "Failed to retrieve data from", clean_url
            
        url_array.append(clean_url)

        html = response.read()   
        soup = BeautifulSoup(html,'html.parser').get_text()
        soup = re.sub(r"\s+", ' ', soup)

        words = soup.split()

        count = 0

        for sWord in search_array:
            count = 0
            for word in words:
                if word.upper()[:len(sWord)] == sWord.upper():
                    count = count + 1
            #print sWord + " : " + str(count) + "/" + str(len(words))
            try:
                word_freq.append(float(count)/float(len(words)))
            except ZeroDivisionError:
                word_freq.append(0)
        if len(word_freq) == 1:
            word_freq.append(0.5)
        if len(word_freq) == 2:
            word_freq.append(0.5)
        freq_array.append(word_freq) 
        x = x+1
    except IndexError:
        print "Less than 10 results"
        limit = x

xaxis = 0
yaxis = 0
radius = 0

for x in range(0, limit):
    if freq_array[x][0] > xaxis:
        xaxis = freq_array[x][0]
    if freq_array[x][1] > yaxis:
        yaxis = freq_array[x][1]
    if freq_array[x][2] > radius:
        radius = freq_array[x][2]

for x in range(0, limit):
    freq_array[x][0] = (freq_array[x][0]/xaxis)*(height-100)
    if len(search_array) >= 2:
        freq_array[x][1] = (freq_array[x][1]/yaxis)*(width-100)
    else:
        freq_array[x][1] = height/2
    if len(search_array) >= 3:
        freq_array[x][2] = ((freq_array[x][2]/radius)*40)+10
    elif len(search_array) == 1:
        freq_array[x][2] = ((freq_array[x][2]/radius)*20)
    else:
        freq_array[x][2] = 25
    
    
for x in range(0, limit):
    C.create_oval(freq_array[x][0], 600 - freq_array[x][1],
                  freq_array[x][0]+freq_array[x][2], 600 - (freq_array[x][1]+freq_array[x][2]),
                  fill = "black")

if len(search_array) == 1:
    search_array.append("null")
if len(search_array) == 2:
    search_array.append("null")
    
key = "x = \"" + search_array[0] + "\"     y = \"" + search_array[1] + "\"     size = \"" + search_array[2] + "\""

C.create_text(width/2, 25, text=key)
C.pack()
def key(event):
    print "pressed", repr(event.char)

def callback(event):
    #print "clicked at", event.x, event.y
    for x in range(0, limit):
        a = freq_array[x]
        x1 = a[0]
        x2 = a[0] + a[2]
        y1 = width - a[1]
        y2 = width - a[1] - a[2]
        if event.x >= x1 and event.x <= x2 and event.y <= y1 and event.y >= y2:
            webbrowser.open(url_array[x])

C.bind("<Key>", key)
C.bind("<Button-1>", callback)
top.mainloop()
time.sleep(5)




    
    
