// TO-DO
// Parse HTML from webpages
// From webpage text, find frequency of words

var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var DOMParser = require("domparser").DOMParser;
var sanitizeHtml = require('sanitize-html');
var request = new XMLHttpRequest();

var siteStr = "https://api.cognitive.microsoft.com/bing/v5.0/search?q=";
var key = "f696d60cdc8a4cc68a8f39f33bb150be";
var count = 1;
var query = process.argv.slice(2).join(" ");

var queryArray = query.split(" ");

request.open("GET", siteStr+encodeURIComponent(query)+"&count="+count, false);
request.setRequestHeader("Ocp-Apim-Subscription-Key", key, "BingAPIs-Market", "en-NZ");

request.responseType = 'document';

request.send();

var jsontext = JSON.parse(request.responseText)

if (Math.floor(request.status/100)==2){ // If status code indicates success
var reqCount = 0
    for(values of jsontext.webPages.value){
      console.log(values.name)
      console.log(values.displayUrl)
      //console.log(values.snippet)
      //console.log(values.url)
      var newurl = values.url.substring(20, values.url.length)
      newurl = newurl.substring(newurl.search("http"), newurl.length)
      newurl = newurl.substring(0, newurl.search("&p=DevEx"))
      newurl = decodeURIComponent(newurl)
      //console.log(newurl)
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.open("GET", newurl, false);
      xmlhttp.responseType = 'document'
      xmlhttp.send();
      if (xmlhttp.status === 301){
        newurlsecure = newurl.slice(0, 4) + "s" + newurl.slice(4)
        xmlhttp.open("GET", newurlsecure, false);
        xmlhttp.responseType = 'document'
        xmlhttp.send();
      }
      console.log(xmlhttp.status);
      //var text = sanitizeHtml(xmlhttp.responseText);
      var text = (new DOMParser().parseFromString(xmlhttp.responseText, "text/html").documentElement.textContent);
      text = text.replace(/\s/g, " ");
      var words = text.split(" ").filter(Boolean);
      //console.log(text);
      var count;
      for (word in queryArray){
        count = 0;
        for (var i = 0; i<words.length; i++){
          if (words[i].toUpperCase().slice(0,queryArray[word].length) === queryArray[word].toUpperCase()){
            count++
          }
        }
        console.log(queryArray[word] + " : " + count + "/" + words.length)
      }
      //console.log(words);

      //console.log(xmlhttp.responseText)

      reqCount++
      console.log(""); //print an extra line for "prettiness"

    }
    //console.log(reqCount)
}
if (Math.floor(request.status/100)!=2){
  console.log("Unable to complete request. Did you specify a search query in the command line?")
}
