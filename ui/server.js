var app = require('express')();
var proxy = require('express-http-proxy');
var serveStatic = require('serve-static');

var request = require('request');

app.use('/api', function(req, res) {
    var url = 'http://localhost:5000/api' + req.url;
    req.pipe(request(url)).pipe(res);
});

app.use('/', serveStatic("./static"));

app.listen(8080, function(){
    console.log('Server running on 8080.');
});

