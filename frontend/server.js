var express = require("express");
var app = express();
var path = require("path");
var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));
app.use("/public", express.static(__dirname + "/public"));

app.get("/", function (req, res) {
  res.sendFile(path.join(__dirname + "/index.html"));
});
app.get('/calculate', (req, res) => {
  res.sendFile(path.join(__dirname + "/calculate.html"));
  // res.render("/calculate.html");
 });
var server = app.listen(80, function () {
  console.log("Node server is running..");
});
