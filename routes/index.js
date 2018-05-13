var express = require('express');
var api = express.Router();
var mongoose =require("../config/mongoose.js");
var db = mongoose();
var Anime = require('../models/Anime.js');// 引入模型
var Online = require('../models/Online.js');
var request = require('request');
var AnimeSpecific = require('../models/animeSpecific.js');
var FeedBack = require("../models/FeedBack.js");
	api.all('*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Content-Type");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By",' 3.2.1')
    res.header("Content-Type", "application/json;charset=utf-8");
    if (req.method == 'OPTIONS') {
    res.sendStatus(200); // 让options请求快速返回
  }
  else {
    next();
  }
});
async function handlResult(arr)
{
	return arr.map( item => {
		return `${item._id}`;
	})
}
async function handleCallback(arr)
{
	return JSON.parse(arr)
}
	api.get("api/getExtensionData", function(req,res){
		FeedBack.Find({merge:false},(err, result) => {
			if(!err)res.json({code:200, FeedBackData:result})
		})
	})
	api.post("api/merge", function(req, res){
		/* check the password and merge some data */
		
	})
	
	api.post("/api/postFeedBack", function(req,res){
		let body = req.body
		let doc = {body..., date:new Date(), merge:false}
		FeedBack.create(doc, function(err, docs){
			if(err) console.log(err);
		console.log('保存成功：' + docs);
		});
	})
	
	api.post("/api/postRecommend", function(req,res){
		let animelist = req.body.animelist;
		Anime.find({"animeTitle":{"$in":animelist}},"_id", (err, result) => {
			handlResult(result).then( arr => {
				console.log(arr)
				let url = "http://localhost:8000/postRecommend"
				request({
					url: url,
					method: "POST",
					json: true,
					headers: {
						"content-type": "application/json",
						"Accept":"application/json"
					},
					body: JSON.stringify(arr)
				}, function(error, response, body) {
					if (!error && response.statusCode == 200) {
						handleCallback(body).then(recommends =>{
							Anime.find({_id:{"$in":recommends}}, (err,result) => {
								if (err){res.json({code:201,text:err});}
								else{
									res.json({code:200,animelist:result})
								}
							})
						})
					}
				});
			})
		}) 
		
		/*
		let options = {
			mode: 'cors',
			body:JSON.stringify({'animelist':animelist}),
			headers:{
                'Accept':"application/json",
                'Content-Type': 'application/json;charset=utf-8',
            }
		}
		fetch(`http://localhost:8000/api/pythonRecommend`,options).then(response => {
			JSON.parse(response)
		}).then(rjs => {res.json({code:200,text:rjs});})
		*/
	});
    api.get("/api/AnimeSpecific/:animeId",function(req,res){
        let animeId = req.params.animeId;
        Anime.findOne({_id:animeId}).populate('animeSpecific').exec(function (err, anime) {
            if (err) console.log(err);
            else {
                res.json({"cover":anime.animePicturePath[0],"animeTitle":anime.animeTitle,"specific":anime.animeSpecific});
            }
        });
        });
    api.get('/api/getPage',function(req, res) {
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
    api.get("/api/getSearchPage",function(req, res) {
        if(!req.query.word)
        {
            //todo 返回一个所谓的推荐队列
        }
        else{
            let word = req.query.word;
            Anime.count({animeTitle:{$regex:".*"+word+".*","$options":"i"}},function(err, result) {
                if(err) res.json({code:201,text:error});
                else if(result.length === 0)
                {
                    res.json({code:304})
                }
                else{
                    let num = Math.ceil(result/20);
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
    });
    api.get("/api/getOnlineData", function (req, res) {
        let date =new Date();
        let today = date.getDate();
        let nowmonth = date.getMonth()+1;
        let nowYear = date.getFullYear();
        Online.find({date:today,month:nowmonth,year:nowYear},(err,result)=>{
            if(err || result.length === 0) res.json({code:201,text:err})
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
    api.get("/api/search",function(req,res){
        if(!req.query.word)
        {
            //todo
        }
        else
        {
            let word = req.query.word;
            Anime.find({animeTitle:{$regex:".*"+word+".*","$options":"i"}},(err,result)=>{
                if(err){res.json({code:201,text:err});}
                else if(result.length === 0) {res.json({code:202,text:"没有您需要的资料"});}
                else{
                    let total={
                        code:200,
                        list:result
                    };
                    res.json(total);
                }
            })
        }
    });
    api.get('/api/getSearchList', function (req, res) {
        //这个地方后面会做成实时的一个反馈，但是现在是整个返回
        //并且现在暂时只有一个番剧的搜索
        if(!req.query.word)
        {
            Anime.find({},(err,result)=>{
                if(err) res.json({code:201,text:err})
                else{
                    let tmp = result.map((anime)=>{
                        return anime.animeTitle
                    });
                    let nameList = Array.from(new Set(tmp))
                    let re = {
                        code:200,
                        searchlist:nameList,
                    }
                    res.json(re)
                }
            });
        }
		else if(!req.query.page){
			let word = req.query.word;
            Anime.find({animeTitle:{$regex:".*"+word+".*","$options":"i"}},(err,result)=>{
                if(err) res.json({code:201,text:err})
                else{
                    let tmp = result.map((anime)=>{
                        return anime.animeTitle
                    });
					console.log(tmp)
                    let nameList = Array.from(new Set(tmp))
                    let re = {
                        code:200,
                        searchlist:nameList
						}
                    res.json(re)
                }
            });
		}
			
        else{
            let word = req.query.word;
			let page = req.query.page;
            Anime.find({animeTitle:{$regex:".*"+word+".*","$options":"i"}},(err,result)=>{
                if(err) res.json({code:201,text:err})
                else{
                    let tmp = result.map((anime)=>{
                        return anime.animeTitle
                    });
                    let nameList = Array.from(new Set(tmp))
                    let re = {
                        code:200,
                        searchList:nameList.slice((page-1)*20,page*20),
						animeList:result.slice((page-1)*20,page*20),
						totalPage:Math.ceil(nameList.length/20)
						}
                    res.json(re)
                }
            });
        }
    });
    api.get('/api/getAnime', function (req, res) {
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
                    };
                    res.json(total);
                }
            })
        }
    });


module.exports = api;
