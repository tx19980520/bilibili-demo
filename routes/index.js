var express = require('express');
var api = express.Router();

var mongoose =require(".././config/mongoose.js");
var db = mongoose();
var Anime = require('.././models/Anime.js');// 引入模型
var Online = require('.././models/Online.js')
api.get('/getPage',function(req, res) {
    Anime.count({},(err,result)=>{
        if(err)return{code:201,text:"返回页数失败"};
        else{
            let num=Math.ceil(result/20);
            res.json({
                code:200,
                pages:num
            })
        }
    })
});
api.get("/getSearchPage",function(req, res) {
    if(!res.query.word)
    {

    }
    else{
        Anime.count({animeTitle:{$regex:".*"+word+".*","$options":"i"}},function(req, res) {
            if(err) res.json({code:201,text:error});
            else if(result.length === 0)
            {
                res.json({code:304})
            }
            else{
                let num = Math.ceil(result/20)
                res.json({code:200,page:num})
            }
        })
    }
});
api.get('/',function(req, res) {
    /*let anime = new Anime({
        animeTitle: "ty0207",
        fans:123214,
        animeFinished:1,
        animePicturePath:"full/sda.jpg"
    })
    anime.save()*/
})
api.get("/getOnlineData", function (req, res) {
    let date =new Date()
    let today = date.getDate()
    let nowmonth = date.getMonth()+1
    let nowYear = date.getFullYear()
    Online.find({date:today,month:nowmonth,year:nowYear},(err,result)=>{
        if(err || result.length == 0) res.json({code:201,text:err})
        else{
            let dataPoints = result[0]
            let total = {
                day:today,
                month:nowmonth,
                year:nowYear,
                code:200,
                data:dataPoints['data']
            };
            res.json(total)
        }
    })

});
api.get("/search",function(req,res){
    if(!req.query.word)
    {
        //todo
    }
    else
    {
        let word = req.query.word;
        Anime.find({animeTitle:{$regex:".*"+word+".*","$options":"i"}},(err,result)=>{
            if(err)res.json({code:201,text:err});
            else if(result.length === 1) res.json({code:200,text:"没有您需要的资料"})
            else{
                let total={
                    code:200,
                    list:result
                }
            }
        })
    }
});
api.get('/getSearchList', function (req, res) {
    //这个地方后面会做成实时的一个反馈，但是现在是整个返回
    //并且现在暂时只有一个番剧的搜索
    Anime.find({},"-_id animeTitle",(err,result)=>{
        if(err) res.json({code:201,text:err})
        else{
            let tmp = result.map((anime)=>{
                return anime.animeTitle
            });
            let nameList = Array.from(new Set(tmp))
            let re = {
                code:200,
                list:nameL8ist
            }
            res.json(re)
        }
    });
});
api.get('/getAnime', function (req, res) {
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

module.exports = api;
