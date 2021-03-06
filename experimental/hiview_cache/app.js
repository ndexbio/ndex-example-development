var path = require('path');
var fs = require('fs');
var util = require('util')
var request = require('request');
var http = require('http');
import cyjs2tree from './cyjs2tree'

var cx2cy_service_base_url = 'http://35.203.154.74:3001/ndex2cyjs/'
var cx2cy_query_string = '?server=test'

function getUuids(){
    var uuidArray = fs.readFileSync('uuids.txt').toString().split("\n");
    return uuidArray;
}

var switchParam = null;

if(process.argv.length > 2){
    switchParam = process.argv[2];
}

var cyjsDir = './cyjs_files';
if (!fs.existsSync(cyjsDir)){
    fs.mkdirSync(cyjsDir);
}

var d3Dir = './D3_files';
if (!fs.existsSync(d3Dir)){
    fs.mkdirSync(d3Dir);
}

//==========================================
//==========================================
// FUNCTIONS TO PROCESS CX TO TARGET FORMAT
//==========================================
//==========================================
function processCXToCyJs() {
    console.log("Processing cyjs files");
    var processTheseUuids = getUuids();
    var uuidLength = processTheseUuids.length;
    for(var i=0; i<uuidLength; i++){
        var uuid = processTheseUuids[i];
        console.log("Processing: " + uuid);
        var cx2cyServiceUrl = cx2cy_service_base_url + uuid + cx2cy_query_string;

        var options = {
            "method":"GET",
            "url": cx2cyServiceUrl,
            "headers": {
                "Accept": "application/json"
            }
        }

        var r = request(options, function(err, response, body){

            if(err){
                console.log(err);
            } else if (response.statusCode == 500) {
                console.log('Response Status Code: ' + response.statusCode + ' Internal Error');
            } else {
                var uriSplit = response.request.uri.pathname.split('/');
                var uuidFromUri = uriSplit[uriSplit.length - 1];
                fs.writeFile("./cyjs_files/" + uuidFromUri + ".json" , response.body, function(err) {
                    if(err) {
                        return console.log(err);
                    }

                    console.log("The file was saved! (" + uuidFromUri + ")");
                });

                console.log('Status Code: ' + response.statusCode)
          }
        });
    }

    console.log('Done loading cyjs files');
}

function processCXToD3() {
    console.log("Processing cyjs files");
    var processTheseUuids = getUuids();
    var uuidLength = processTheseUuids.length;
    for(var i=0; i<uuidLength; i++){
        var uuid = processTheseUuids[i];
        var cx2cyServiceUrl = cx2cy_service_base_url + uuid + cx2cy_query_string;

        var options = {
            "method":"GET",
            "url": cx2cyServiceUrl,
            "headers": {
                "Accept": "application/json"
            }
        }

        var r = request(options, function(err, response, body){

            if(err){
                console.log(err);
            } else if (response.statusCode == 500) {
                console.log('Response Status Code: ' + response.statusCode + ' Internal Error');
            } else {
                var uriSplit = response.request.uri.pathname.split('/');
                var uuidFromUri = uriSplit[uriSplit.length - 1];
                var cyjsResults = cyjs2tree(JSON.parse(response.body));
                var cyjsString = util.inspect(cyjsResults, {compact: false, depth: 10, maxArrayLength: null});
                fs.writeFile("./D3_files/" + uuidFromUri + ".json" , cyjsString, function(err) {
                    if(err) {
                        return console.log(err);
                    }

                    console.log("The file was saved! (" + uuidFromUri + ")");
                });

                console.log('Status Code: ' + response.statusCode)
          }
        });
    }

    console.log('Done loading cyjs files');
}

function processCyJsToD3() {
    console.log("Processing d3 files");
    fs.readdir("./cyjs_files", (err, files) => {
        files.forEach(file => {
            if(file != ".DS_Store"){
                console.log("Reading files " + file);
                var content = fs.readFileSync("./cyjs_files/" + file);
                var d3Results = cyjs2tree(JSON.parse(content));
                var d3String = util.inspect(d3Results, {compact: false, depth: 10, maxArrayLength: null});
                fs.writeFile("./D3_files/" + file , d3String, function(err) {
                    if(err) {
                        console.log("Error");
                        return console.log(err);
                    }

                    console.log("The file was saved!");
                });
            }
        });
    });
}

if(switchParam != null){
    switch(switchParam) {
        case "1":
            processCXToCyJs();
            break;
        case "2":
            processCXToD3();
            break;
        case "3":
            processCyJsToD3();
            break;
        default:
            console.log("Please provide a valid parameter (1-3)");
    }
} else {
    console.log("Please indicate which process you want to run. (1-3)");
}
