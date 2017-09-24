from PIL import Image,ImageDraw
import cStringIO
import sys
import cgi
import os
import cgi, cgitb
import urllib
import urllib2
import re
import webbrowser
import time
import ssl
import datetime
import Tkinter as tk
from unidecode import unidecode
from bs4 import BeautifulSoup
from py_ms_cognitive import PyMsCognitiveWebSearch
from multiprocessing.dummy import Pool as ThreadPool


visi = True #Set to true to use VISI, false to use 10Blue
identifier = "DFEACB06"
logfile = open(identifier+".txt", "a+")

logfile.write(str(datetime.datetime.now()))
logfile.write("\n")



def freqcalc(x):
    try:
        #name_array.insert(x, unidecode(results[x].name))
        #snippet_array.insert(x, unidecode(results[x].snippet))
        word_freq = [] 
        #print results[x].url+"<br>"
           
        clean_url = url_array[x]
        context = ssl._create_unverified_context()
        

        try:
            response = urllib2.urlopen(clean_url,context=context)
        except urllib2.HTTPError:
            response = urllib2.urlopen("http://blank.org/",context=context)
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

logfile.write(query)
logfile.write("\n")


#query = "moon snails"

API_KEY = "54bcf3e9f555466fa24f529b88311f65"
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
    try:
        dirty_url = results[x].url[20:]
        clean_url = dirty_url[dirty_url.find("http"):]
        clean_url = clean_url[:clean_url.find("&p=DevEx")]
        clean_url = urllib.unquote(clean_url)
        url_array.append(unidecode(clean_url))
    except IndexError:
        limit = x
        if (limit==0):
            print "Content-type: text/html\n"
            print """<h1>No Results Found</h1><br><form action="../"><input type="submit" value="New Search">"""
            sys.exit()


pool = ThreadPool(limit) 
array_array = pool.map(freqcalc,range(limit))
pool.close() 
pool.join()

for x in range(0, limit):
    freq_array.insert(x, array_array[x][0])
    url_array.insert(x, str(array_array[x][1]).replace('"', '\\"'))
    name_array.insert(x, str(array_array[x][2]).replace('"', '\\"'))
    snippet_array.insert(x, str(array_array[x][3]).replace('"', '\\"'))
    logfile.write(str(array_array[x][1]))
    logfile.write("\n")

xaxis = 0.0000001
yaxis = 0.0000001
radius = 0

for x in range(0, limit):
    if freq_array[x][0] > xaxis:
        xaxis = freq_array[x][0]
    if freq_array[x][1] > yaxis:
        yaxis = freq_array[x][1]


for x in range(0, limit):
    freq_array[x][0] = (freq_array[x][0]/xaxis)*(h-70)+30
    if len(search_array) >= 2:
        freq_array[x][1] = (freq_array[x][1]/yaxis)*(w-70)+30
    else:
        freq_array[x][1] = w/2
    freq_array[x][2] = 10

if len(search_array) == 1:
    search_array.append("")



print "Content-type: text/html\n"

print "Search Query =", query
print "<br>"



if visi:
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

    document.getElementById("label").innerHTML = "X: " + qvalues[1]+ ", Y: " + qvalues[0] 
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
    ctx.fillStyle = "#FF0000"; 
    ctx.font = "normal normal 10px Helvetica";
    ctx.fillText(qvalues[1], 275-(2*qvalues[1].length), 540);
    ctx.fillText(qvalues[0],8,270)
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
else:
    htmlstr = """
    <html>
    <head><meta charset="UTF-8"></head>
    <title>10Blue</title>
    <body>

    <div>


    <table width = "450px" border = "0">
             
             <tr>

                
                <td width = "350">
                <h4 id="label"></h4>

                <br>
                <form action="../">
                <input type="submit" value="New Search"> <br> <br>


                <a id="name{0}" target="_blank" style = "color:blue"> </a>
                
                <p id="snippet{0}"> </p>
                <br>
                <a id="name{1}" target="_blank" style = "color:blue"> </a>
                
                <p id="snippet{1}"> </p>
                <br>
                <a id="name{2}" target="_blank" style = "color:blue"> </a>
                
                <p id="snippet{2}"> </p>
                <br>
                <a id="name{3}" target="_blank" style = "color:blue"> </a>
                
                <p id="snippet{3}"> </p>
                <br>
                <a id="name{4}" target="_blank" style = "color:blue"> </a>
                
                <p id="snippet{4}"> </p>
                <br>
                <a id="name{5}" target="_blank" style = "color:blue"> </a>
                
                <p id="snippet{5}"> </p>
                <br>
                <a id="name{6}" target="_blank" style = "color:blue"> </a>
                
                <p id="snippet{6}"> </p>
                <br>
                <a id="name{7}" target="_blank" style = "color:blue"> </a>
                
                <p id="snippet{7}"> </p>
                <br>
                <a id="name{8}" target="_blank" style = "color:blue"> </a>
                
                <p id="snippet{8}"> </p>
                <br>
                <a id="name{9}" target="_blank" style = "color:blue"> </a>
                
                <p id="snippet{9}"> </p>
                <br>
                <br>
                <form action="../">
                <input type="submit" value="New Search">

                

             </tr>
             
          </table>


    </div>

    <script>

    """.format(0,1,2,3,4,5,6,7,8,9)


    for x in range(0,limit):  
        htmlstr += "document.getElementById(\"name"+str(x)+"\").innerHTML = \"" + str(name_array[x]) + "\"\n"
        htmlstr += "document.getElementById(\"snippet"+str(x)+"\").innerHTML = \"" + str(snippet_array[x]) + "\"\n"
        htmlstr += "document.getElementById(\"name"+str(x)+"\").href = \"" + str(url_array[x]) + "\"\n"

    htmlstr = htmlstr + """

    </script>

    </body>
    </html>
    """
    

print htmlstr


logfile.close()


