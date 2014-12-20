var level = require('level');
var sublevel = require('level-sublevel');
var strftime = require('strftime');

var siteCrawler = require('./siteCrawler');
var testCrawler = require('./testCrawler');

var curDate = strftime('%F');

var db = sublevel(level('./testdb' + curDate));

//var curTimeDb = db.sublevel(curDate);
//
//
var testNum = 0;
var steps = [
    siteCrawler.updateMajorList,
    siteCrawler.updateMajorCourses,
    testCrawler.printMajors
    ];

function executeStepWrapper(step, arg, callback) {
    step(arg);
    callback();
}

function cleanUp() {
    console.log('Executing cleanUp');
    testNum++;
}

function executeSteps(step) { 
    if(step) {
        //console.log('Executing step: ' + step);
        executeStepWrapper(step, db, function() {
            return executeSteps(steps.shift());
        });
    } else {
        return;
    }
}

executeSteps(steps.shift());
        
//siteCrawler.updateMajorList(db);

//testCrawler.printMajors(db);

