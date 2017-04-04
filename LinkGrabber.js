var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var request = new XMLHttpRequest();
var siteStr = "https://api.cognitive.microsoft.com/bing/v5.0/search?q=";
var query = "Andrew Trotmans papers";
var key = "f696d60cdc8a4cc68a8f39f33bb150be";
request.open("GET", siteStr+query, false);
request.setRequestHeader("Ocp-Apim-Subscription-Key", key, "BingAPIs-Market", "en-NZ");

request.responseType = 'document';

request.send();

var test = JSON.parse(request.responseText)

console.log(test.webPages)

//console.log(request.status);
//console.log(request.statusText);
//console.log(request.responseText);
