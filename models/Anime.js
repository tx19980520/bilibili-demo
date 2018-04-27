var mongoose = require('mongoose');
var animeSchema = require('../schemas/animeschema.js');
//创建model，这个地方的ch_user对应mongodb数据库中ch_users的conllection。
//mongoose会自动改成复数，如模型名：xx―>xxes, kitten―>kittens, money还是money
var Anime = mongoose.model('Anime',animeSchema);
module.exports = Anime;