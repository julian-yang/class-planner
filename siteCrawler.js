var Crawler = require('crawler');
var url = require('url');
var level = require('level');

// DEFAULT URLS HERE
var DEFAULT_scheduleHomeURL = 'http://www.registrar.ucla.edu/schedule/schedulehome.aspx';

// DEFAULT TAG NAMES HERE
var DEFAULT_majorListWrapperId = 'ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea';
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

module.exports.updateMajorList = function(db) {
    var c = new Crawler({
            maxConnections : 10,
            callback : function (error, result, $) {
                var majors = $('#' + DEFAULT_majorListWrapperId).children();
                console.log(majors);
            }
    });
    c.queue([{
                /*jshint multistr: true */
                html:
                '<select size="7" name="ctl00$BodyContentPlaceHolder$SOCmain$lstSubjectArea" \
                    id="ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea"> \
                    <option value="AERO ST">Aerospace Studies</option> \
                    <option value="AF AMER">African American Studies</option> \
                    <option value="AF LANG">African Languages</option> \
                    <option value="AFRC ST">African Studies</option> \
                </select>'
            }]);
    //c.queue(DEFAULT_scheduleHomeURL);
};
