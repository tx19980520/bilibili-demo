var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var index = require('./routes/index');
var users = require('./routes/users');

var app = express();

var mongoose =require("./config/mongoose.js");
var db = mongoose();
var Anime = require('./models/Anime.js');// 引入模型
var Online = require('./models/Online.js')
app.get('/getPage',function(req, res) {
    Anime.count({},(err,result)=>{
    if(err)return{code:201,text:"返回页数失败"}
    else{
        let num=Math.ceil(result/20)
        res.json({
            code:200,
            pages:num
        })
    }
    })
});
app.get('/',function(req, res) {
    /*let anime = new Anime({
        animeTitle: "ty0207",
        fans:123214,
        animeFinished:1,
        animePicturePath:"full/sda.jpg"
    })
    anime.save()*/
})
app.get("/getOnlineData", function (req, res) {
    let date =new Date()
    let today = date.getDate()
    let nowmonth = date.getMonth()+1
    let nowYear = date.getFullYear()
    Online.find({date:today,month:nowmonth,year:nowYear},(err,result)=>{
        if(err) res.json({code:201,text:err})
        else{
            let dataPoints = result[0]
            let total = {
                day:today,
                month:nowmonth,
                year:nowYear,
                code:200,
                data:dataPoints['data']
            }
            res.json(total)
        }
    })

})
app.get('/getAnime', function (req, res) {
    if(!req.query.page){
        Anime.find({},(err,result)=>{
            if(err)  res.json({code:201,text:err});
            else{
                let total = {
                    code:200,
                    list:result.slice(0,20)
                };
                res.json(total);
            }
    })
    }
    else{//代表有页数
            page = req.query.page;
            Anime.find({},(error,result)=>{
                if(error)
                {
                    res.json({code:201,text:"无法查找数据"})
                }
                else{
                    let total = {
                        code:200,
                        list:result.slice((page-1)*20,page*20)
                    }
                    res.json(total);
                }
            })
        }
});

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

app.use('/', index);
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

var server = app.listen(3000, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Example app listening at http://%s:%s', host, port);
});

module.exports = app;
