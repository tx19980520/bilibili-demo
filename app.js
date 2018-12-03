var express = require('express');
var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var api = require('./routes/index');
var users = require('./routes/users');
var fs = require('fs');


var app = express();


var https = require('https');

var privateKey  = fs.readFileSync("/etc/nginx/cqdulux.key", 'utf8');
var certificate = fs.readFileSync("/etc/nginx/libilibi.cqdulux.cn_chain.crt", 'utf8');
var credentials = {key: privateKey, cert: certificate};

var httpsServer = https.createServer(credentials, app);

// view engine setup
//app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', api);
app.use('/users', users);

// catch 404 and forward to error handler
app.use(function(req, res, next) { 
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});
var debug = require('debug')('my-application'); // debug模块
//app.listen(8080, function() {
//    console.log('HTTPS Server is running on: https://localhost:%s', 8080);
//});
var server = app.listen(8080, function () {
    var host = server.address().address;
    var port = server.address().port;
	debug('Express server listening on port ' + port);
    console.log('Example app listening at http://%s:%s', host, port);
});

module.exports = app;
