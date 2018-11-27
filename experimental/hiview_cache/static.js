var express = require('express');
var app = express();
var path = require('path');
var request = require('request');
var http = require('http');
var proxy = require('express-http-proxy');
var compression = require('compression')
var fs = require('fs');
var cors = require('cors')

var masterList = [];
var geoList = [];

app.use(cors());
app.use(compression());

app.use(express.static(__dirname + '/',{ maxAge: 1000 }));

var bodyParser = require('body-parser');

app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({
  limit: '50mb',
    extended: true
}));

app.get('/cache/getcyjs/:uuid', function(req, res) {

  var uuid = req.params.uuid;
  var filePath = path.join(__dirname, "cyjs_files", uuid + ".json");
  fs.exists(filePath, function(exists){
      if (exists) {
        res.writeHead(200, {
          "Content-Type": "application/json",
          "Content-Disposition": "attachment; filename=" + uuid + ".json"
        });
        fs.createReadStream(filePath).pipe(res);
      } else {
        res.writeHead(400, {"Content-Type": "text/plain"});
        res.end("ERROR File does not exist");
      }
    });
  });


app.get('/cache/getd3/:uuid', function(req, res) {

  // Check if file specified by the filePath exists
  var uuid = req.params.uuid;
  var filePath = path.join(__dirname, "D3_files", uuid + ".json");
  fs.exists(filePath, function(exists){
      if (exists) {
        // Content-type is very interesting part that guarantee that
        // Web browser will handle response in an appropriate manner.
        res.writeHead(200, {
          "Content-Type": "application/json",
          "Content-Disposition": "attachment; filename=" + uuid + ".json"
        });
        fs.createReadStream(filePath).pipe(res);
      } else {
        res.writeHead(400, {"Content-Type": "text/plain"});
        res.end("ERROR File does not exist");
      }
    });
  });


console.log("Ready...");


app.listen(3001);