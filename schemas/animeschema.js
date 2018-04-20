var mongoose = require('mongoose');
var Schema = mongoose.Schema;
//创建Schema
var animeSchema = new Schema({
    _id:Number,
    animePicturePath:Array,
    fans:Number,
    animeTitle:String,
    animeId:Number,
    animeFinished:Number,
    animeSpecific:{type:Number,ref:"animeSpecific"}

});
module.exports = animeSchema;