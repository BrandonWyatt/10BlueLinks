// TO-DO
// - Figure out why there are discrepancies between website and API (even though API results seem better)
// - Write up work done so far in report
// - What next?

var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var request = new XMLHttpRequest();
var resultRequest = new XMLHttpRequest();

var siteStr = "https://api.cognitive.microsoft.com/bing/v5.0/search?q=";
var key = "f696d60cdc8a4cc68a8f39f33bb150be";
var count = 5
var query = process.argv.slice(2).join(" ");

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
      console.log(values.snippet)
      console.log(values.url)
      var newurl = values.url.substring(20, values.url.length)
      newurl = newurl.substring(newurl.search("http"), newurl.length)
      newurl = newurl.substring(0, newurl.search("&p=DevEx"))
      newurl = decodeURIComponent(newurl)
      console.log(newurl)
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
      console.log(xmlhttp.status)
      //console.log(xmlhttp.responseText)
      reqCount++
      console.log(""); //print an extra line for "prettiness"

    }
    //console.log(reqCount)
}
if (Math.floor(request.status/100)!=2){
  console.log("Unable to complete request. Did you specify a search query in the command line?")
}
