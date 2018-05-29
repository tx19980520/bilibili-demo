var mongoose = require('mongoose');
var Schema = mongoose.Schema;
//创建Schema
var feedbackSchema = new Schema({
	_id: Number,
    date: Date,
	animeList: Array,
    recommendList: Array,
	merge: {type:Boolean,default:false},
});
module.exports = feedbackSchema;