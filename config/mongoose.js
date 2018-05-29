const mongoose = require('mongoose');
const config = require('./config');
const fs = require('fs');
const readline = require('readline');
var User = require('../models/User.js');
var Anime = require("../models/Anime.js");
var AnimeSpecific = require('../models/animeSpecific.js');
module.exports = ()=>{
    //  mongoose.Promise = global.Promise;//如果有promise的问题，可以用这个试试
    mongoose.connect(config.mongodb);//连接mongodb数据库
    // 实例化连接对象
    let db = mongoose.connection;
    db.on('error', console.error.bind(console, '连接错误：'));
    db.once('open', (callback) => {
     /*   console.log('MongoDB连接成功！！');
        //开始设计导入之前的数据

        let fRead = fs.createReadStream("./scrapy_crawl/bilibili/bilibili/data/bilibili2.json");
        const rl = readline.createInterface({
            input: fRead
        });
        rl.on('line', (line) => {
            //我们在这里进行文件
            let data = JSON.parse(line);
            data['_id'] = parseInt(data['animeId']);
            data['animeSpecific'] = data['_id'];
            let spec = new Anime(data);
            spec.save();
        });
        rl.on('close', () => {
            console.log("番剧数据导入完成");
        });
        let fReadspec = fs.createReadStream("./scrapy_crawl/bilibili/bilibili/data/specific2.json");
        const rlspec = readline.createInterface({
            input: fReadspec
        });
        rlspec.on('line', (line) => {
            //我们在这里进行文件
            let data = JSON.parse(line);
            data['_id'] = parseInt(data['animeId']);
            let spec = new AnimeSpecific(data);
            spec.save();
        });
        rlspec.on('close', () => {
            console.log("番剧番剧详情数据导入完成");
        });*/
        //上述测试是成功的，下面代码的逻辑是没错的，错的是我们的主键的设定

        //下述代码没有问题
        /*User.findOne({uid: "10935167"}).populate('likevideo').exec(function (err, user) {
            if (err) console.log(err);
            console.log('The author is %s', user.likevideo[0]);
        });*/
        return db;
    });
};