var Crawler = require('crawler');
var url = require('url');
var level = require('level');
var sub = require('level-sublevel');
var mysql = require('mysql');
// DEFAULT URLS HERE
var DEFAULT_scheduleHomeURL = 'http://www.registrar.ucla.edu/schedule/schedulehome.aspx';
var DEFAULT_scheduleMajorURL = 'http://www.registrar.ucla.edu/schedule/crsredir.aspx'; //termsel=14S&subareasel=COM+SCI
// DEFAULT TAG NAMES HERE
var DEFAULT_majorListWrapperId = 'ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea';


// OTHER DEFAULT VARS HERE
var DEFAULT_academicTerm = '14S';

//TODO: integrate this wrapper, move url retrieval to the DB
function getWrapper(db, key, defaultVal, notFoundMsg) {
    var value;
    db.get(key, function(err, data) {
        if (err) {
            if(!err.notFound) {
                console.error(notFoundMsg);
                value = defaultVal;
            } else {
                console.error('ERROR: error accessing db');
                //throw err;
            }
        } else {
            value = data;
        }
    });
    return value;
}

/*
//takes in a database to store the majors
//the database will have a sublevel for storing useful url's
module.exports.loadUrls = function(db) {
    var urlDB = db.sublevel('urls');
    var urlDict = {};

    
    urlDict.scheduleHomeURL = DEFAULT_scheduleHomeURL;
    // get other needed URL's here

    return urlDict;
};

module.exports.loadTagNames = function(db) {
    var tagNamesDB = db.sublevel('tags');
    var tagDict = {};

    tagDict.majorListWrapperId = '';
    tagNamesDB.get('majorListWrapperId', function(err, data) {
};
*/



//updates db with the majors listed on the UCLA registrar page.
module.exports.updateMajorList = function(connection) {
    
    function processMajors (error, result, $) {
        $('#' + DEFAULT_majorListWrapperId)
                .children()
                .each(function(i, elem) {
                    //console.log('preparing to insert into table');
                    var majorName = $(this).text();
                    var majorCode = $(this).attr('value');
                    var insertSQL = "INSERT INTO majors (major_code, major_name) " +
                        "VALUES ('" + majorCode + "', '" + majorName + "')";
                    //console.log(insertSQL);
                    connection.query(insertSQL, 
                        function(err, results) {
                            if(err) {
                                console.log(err);
                                return;
                            }
                            //console.log(results);
                        });
                });
        
    }

    function updateDb() {
        //majorDb.batch(majorsBatch);
    }

    var c = new Crawler({
                maxConnections : 10,
                callback : processMajors,
                onDrain: updateDb
            });


    //c.queue([{
    //            /*jshint multistr: true */
    //            html:
    //            '<select size="7" name="ctl00$BodyContentPlaceHolder$SOCmain$lstSubjectArea" \
    //                id="ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea"> \
    //                <option value="AERO ST">Aerospace Studies</option> \
    //                <option value="AF AMER">African American Studies</option> \
    //                <option value="AF LANG">African Languages</option> \
    //                <option value="AFRC ST">African Studies</option> \
    //            </select>'
    //        }]);
    c.queue([{
        uri: DEFAULT_scheduleHomeURL,
        callback: processMajors}]);
};

module.exports.updateMajorCourses = function(db) {
    //var courseDb = db.sublevel('courses');

};
