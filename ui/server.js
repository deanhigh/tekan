var app = require('express')();
var proxy = require('express-http-proxy');
var serveStatic = require('serve-static');

app.use('/api', proxy('http://localhost:5000/api/'));

app.use('/', serveStatic("./static"));

app.listen(8080, function(){
    console.log('Server running on 8080.');
});

