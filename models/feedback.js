var mongoose = require('mongoose');
var feedbackSchema = require('../schemas/feedbackschema.js');
//mongoose会自动改成复数，如模型名：xx―>xxes, kitten―>kittens, money还是money
var Feedback = mongoose.model('Feedback',feedbackSchema);
module.exports = Feedback;