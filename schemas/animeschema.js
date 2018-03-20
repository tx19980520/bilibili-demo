var mongoose = require('mongoose');
var Schema = mongoose.Schema;
//创建Schema
var animeSchema = new Schema({
    animePicturePath:Array,
    fans:Number,
    animeTitle:String,
    animeId:Number,
    animeFinished:Number

});
module.exports = animeSchema;