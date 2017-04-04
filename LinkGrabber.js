var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var request = new XMLHttpRequest();

var siteStr = "https://api.cognitive.microsoft.com/bing/v5.0/search?q=";
var key = "f696d60cdc8a4cc68a8f39f33bb150be";
var count = 10
var query = process.argv.slice(2);


request.open("GET", siteStr+query, false);
request.setRequestHeader("Ocp-Apim-Subscription-Key", key, "BingAPIs-Market", "en-NZ");

request.responseType = 'document';

request.send();

var jsontext = JSON.parse(request.responseText)

console.log(""); //print an extra line for "prettiness"

if (Math.floor(request.status/100)==2){
  for (var c = 0; c<count; c++){
    console.log(jsontext.webPages.value[c].name)
    console.log(jsontext.webPages.value[c].displayUrl)
    console.log(jsontext.webPages.value[c].snippet)
    console.log(jsontext.webPages.value[c].url+"\n")
  }
}
if (Math.floor(request.status/100)!=2){
  console.log("Unable to complete request. Did you specify a search query in the command line?")
}
