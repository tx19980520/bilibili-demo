var mongoose = require('mongoose');
var Schema = mongoose.Schema;
//创建Schema
var feedbackSchema = new Schema({
	_id: Number,
    date: Date,
	origin: [{type:Number, ref:"Anime"}],
	recommend: [{type:Number, ref:"Anime"}],
	score: {type:Array,default:[]},
	merge: {type:Boolean,default:false}
});
module.exports = feedbackSchema;