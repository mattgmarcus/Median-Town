var express = require("express");
var fs = require("fs");
var cookieParser = require('cookie-parser');
var htmlfile = "index.html";
var sitemapfile = "sitemap.xml";

var app = express();
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use('/data', express.static(__dirname + '/data'));

app.get("/sitemap.xml", function(req, res) {
    var html = fs.readFileSync(sitemapfile).toString();
    res.send(html);
});

app.get("/*", function(req, res) {
    var html = fs.readFileSync(htmlfile).toString();
    res.send(html);
});

var port = process.env.PORT || 8080;
app.listen(port, function() {
    console.log("Listening on " + port);
});
