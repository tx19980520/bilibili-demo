var mongoose = require('mongoose');
var Schema = mongoose.Schema;
//创建Schema
var onlineSchema = new Schema({
    year:Number,
    month:Number,
    date:Number,
    data:Array
});
module.exports = onlineSchema;