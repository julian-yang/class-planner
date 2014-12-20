var level = require('level');
var sublevel = require('level-sublevel');
var strftime = require('strftime');

var siteCrawler = require('./siteCrawler');
var testCrawler = require('./testCrawler');

var curDate = strftime('%F');

var db = sublevel(level('./testdb' + curDate));

//var curTimeDb = db.sublevel(curDate);
//

siteCrawler.updateMajorList(db);

//testCrawler.printMajors(db);

