var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var Anime = require('.././models/Anime.js');// 引入模型
//创建Schema
var userSchema = new Schema({
    _id: Number,
    uid:String,
    vip:Array,
    likevideo:[{ type: String, ref: 'anime' }]

});
module.exports = userSchema;