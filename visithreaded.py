from PIL import Image,ImageDraw
import cStringIO
import cgi
import os
import cgi, cgitb
import urllib
import urllib2
import re
import webbrowser
import time
import Tkinter as tk
from unidecode import unidecode
from bs4 import BeautifulSoup
from py_ms_cognitive import PyMsCognitiveWebSearch
from multiprocessing.dummy import Pool as ThreadPool

def freqcalc(x):
    try:
        #name_array.insert(x, unidecode(results[x].name))
        #snippet_array.insert(x, unidecode(results[x].snippet))
        word_freq = [] 
        #print results[x].url+"<br>"
           
        clean_url = url_array[x]

        try:
            response = urllib2.urlopen(clean_url)
        except urllib2.HTTPError:
            response = urllib2.urlopen("http://blank.org/")
            #print "Failed to retrieve data from", clean_url

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
            #print sWord + " : " + str(count) + "/" + str(len(words))+"<br>"
            try:
                word_freq.append(float(count)/float(len(words)))
            except ZeroDivisionError:
                word_freq.append(0)
        if len(word_freq) == 1:
            word_freq.append(0.5)
        word_freq.append(0)

    except IndexError:
        #print "Less than 10 results"
        limit = x
    return [word_freq, clean_url, unidecode(results[x].name), unidecode(results[x].snippet)];


print "Status: 200 OK"

form = cgi.FieldStorage()
query = form.getvalue('query')


#query = "moon snails"

API_KEY = "f696d60cdc8a4cc68a8f39f33bb150be"
search_term = query
limit = 10
search_array = search_term.split()
search_service = PyMsCognitiveWebSearch(API_KEY, search_term)
results = search_service.search(limit=limit, format='json')
x = 0
h = 550
w = 550

freq_array = []
url_array = []
name_array = []
snippet_array = []

for x in range(0, limit):
    dirty_url = results[x].url[20:]
    clean_url = dirty_url[dirty_url.find("http"):]
    clean_url = clean_url[:clean_url.find("&p=DevEx")]
    clean_url = urllib.unquote(clean_url)
    url_array.append(unidecode(clean_url))


pool = ThreadPool(limit) 
array_array = pool.map(freqcalc,range(limit))
pool.close() 
pool.join()

for x in range(0, limit):
    freq_array.insert(x, array_array[x][0])
    url_array.insert(x, array_array[x][1])
    name_array.insert(x, array_array[x][2])
    snippet_array.insert(x, array_array[x][3])

xaxis = 0
yaxis = 0
radius = 0

for x in range(0, limit):
    if freq_array[x][0] > xaxis:
        xaxis = freq_array[x][0]
    if freq_array[x][1] > yaxis:
        yaxis = freq_array[x][1]


for x in range(0, limit):
    freq_array[x][0] = (freq_array[x][0]/xaxis)*(h-70)+20
    if len(search_array) >= 2:
        freq_array[x][1] = (freq_array[x][1]/yaxis)*(w-70)+20
    else:
        freq_array[x][1] = h/2
    freq_array[x][2] = 20


print "Content-type: text/html\n"

print "Search Query =", query
print "<br>"




htmlstr = """
<html>
<head><meta charset="UTF-8"></head>
<title>VISI - Visual Interactive Search Interface</title>
<body>

<div>


<table width = "100%" border = "0">
         
         <tr>

            
            <td width = "350">
            <h4 id="label"></h4>
            <p>Click on a dot to open the corresponding link.
            A dot further to the right matches the X term better, while a dot closer to the top matches the Y term better.</p>
            <br>
            <br>
            <b>Most Recent Selection:</b>
            <a id="name" target="_blank" style = "color:blue"> </a>
            
            <p id="snippet"> </p>
            <br>
            <br>
            <form action="../">
            <input type="submit" value="New Search">

            
            </td>

            <td width = "650">
            <canvas id="myCanvas" width="550" height="550"
            style="border:2px solid #000000;">
            Your browser does not support the canvas element.

            </canvas>
 
            </td>
         </tr>
         
      </table>


</div>

<script>

var canvas = document.getElementById("myCanvas");
canvas.addEventListener("mousedown", doMouseDown, false);
canvas.addEventListener("mousemove", doMouseMove, false);
var ctx = canvas.getContext("2d");
var urls = {0}
var freqs = {1}
var resulttitles = {2}
var resultcontexts = {3}
var qvalues = {4}
document.getElementById("label").innerHTML = "X: " + qvalues[0]+ ", Y: " + qvalues[1] 
""".format(url_array, freq_array, name_array, snippet_array, search_array)

for x in range(0,limit):
    xpos = freq_array[x][1]
    ypos = freq_array[x][0]
    rad = freq_array[x][2]    
    htmlstr = htmlstr + """
    ctx.beginPath();
    ctx.arc({0}, {1}, {2}, 0, 2 * Math.PI, false);
    ctx.fillStyle = 'black';
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#FFFFFF';
    ctx.stroke();

    
    """.format(xpos,ypos,rad)
    

htmlstr = htmlstr + """
function checkClick(freqs, x, y){
    for (var i = 0; i<"""

htmlstr = htmlstr + str(limit)

htmlstr = htmlstr + """; i++){
        shapex = freqs[i][1];
        shapey = freqs[i][0];
        shaperad = freqs[i][2];
        if (Math.abs(shapex-x)<shaperad){
            if (Math.abs(shapey-y)<shaperad){
                console.log("Successful click");
                window.open(urls[i]);
            }
        }
    }
}
function checkOver(freqs, x, y){
    for (var i = 0; i<"""

htmlstr = htmlstr + str(limit)

htmlstr = htmlstr + """; i++){
        shapex = freqs[i][1];
        shapey = freqs[i][0];
        shaperad = freqs[i][2];
        if (Math.abs(shapex-x)<shaperad){
            if (Math.abs(shapey-y)<shaperad){

                document.getElementById("name").innerHTML = resulttitles[i]
                document.getElementById("snippet").innerHTML = resultcontexts[i]
                document.getElementById("name").href = urls[i]
                
            }
        }
    }
}

function doMouseDown(event){
    canvas_x = event.pageX-455;
    canvas_y = event.pageY-32;
    checkClick(freqs, canvas_x, canvas_y)
    
}

function doMouseMove(event){
    canvas_x = event.pageX-455;
    canvas_y = event.pageY-32;
    checkOver(freqs, canvas_x, canvas_y)
}
</script>

</body>
</html>
"""

print htmlstr


