var level = require('level');
var strftime = require('strftime');

var siteCrawler = require('./siteCrawler');
var testCrawler = require('./testCrawler');

// setup dB
var mysql = require('mysql');
var pool = mysql.createPool({
        connectionLimit : 10,
        host        : 'localhost',
        user        : 'classplanner',
        password    : 'stackedqueue',
        database    : 'class_planner'
});
/*
connection.connect(function(err) {
    if(err) {
        console.error('error connecting: ' + err.stack);
        return;
    }

    console.log('connected as id ' + connection.threadId);
});
*/
/*
var sql = 'SELECT * FROM majors';
connection.query("INSERT INTO majors (major_code, major_name) VALUES ('code', 'name')");
connection.query(sql, function(err, results) {
    if(err)
        console.log(err);
    else
        console.log(results);
});


*/

var curDate = strftime('%F');
var count = 0;
//var db = sublevel(level('./testdb' + curDate));

//var curTimeDb = db.sublevel(curDate);
//
//
var testNum = 0;
var steps = [
    connectionWrapper(siteCrawler.updateMajorList),
    connectionWrapper(siteCrawler.updateMajorCourses),
    connectionWrapper(testCrawler.printMajors),
    cleanUp
    ];

function connectionWrapper(fun) {
    return function() {
        pool.getConnection(function(err, connection) {
                if(err) {
                    console.log(err);
                    return;
                }
                console.log('got connection!');
                fun(connection);
                console.log('releasing connection!');
                connection.release();
            });

    };
}

function executeStepWrapper(step, callback) {
    step();
    callback();
}

function cleanUp() {
    console.log('Executing cleanUp');
}

function executeSteps(step) { 
    console.log(count);
    count++;
    if(step) {
        //console.log('Executing step: ' + step);
        executeStepWrapper(step, function() {
            return executeSteps(steps.shift());
        });
    } else {
    }
}

executeSteps(steps.shift());
        
//siteCrawler.updateMajorList(db);

//testCrawler.printMajors(db);
//connection.end();


