var mongoose = require('mongoose');
var Schema = mongoose.Schema;
//创建Schema
var animeSpecificSchema = new Schema({
    __v:{type:Number,default:0},
    _id: Number,
    actor:{type:Array,default:[]},
    evaluate:String,
    coins: Number,
    episodes:Array,
    rating:Array,
    tags:Array,
    animeId:Number

});
module.exports = animeSpecificSchema;