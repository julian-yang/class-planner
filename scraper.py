from lxml import html
import requests
import classPlannerDB as db
import re 
import logUtility

MAJOR_LIST_URL = 'http://www.registrar.ucla.edu/schedule/schedulehome.aspx'
COURSE_LIST_URL = 'http://www.registrar.ucla.edu/schedule/crsredir.aspx?termsel='+CUR_TERM+'&subareasel=' # COM+SCI
# DEFAULT TAG NAMES HERE
MAJOR_LIST_WRAPPER_ID = 'ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea'
CLASS_LIST_WRAPPER_ID = 'ctl00_BodyContentPlaceHolder_crsredir1_lstCourseNormal'
# XPATHS HERE
MAJOR_XPATH = '//select[@id="' + MAJOR_LIST_WRAPPER_ID + '"]/*'
COURSE_XPATH = '//select[@id="' + CLASS_LIST_WRAPPER_ID + '"]/*'
# OTHER VARS HERE
CUR_TERM = '15W'



#test = majors.select()

#for major in test:
#    print major.major_code, major.major_name


def getPageTree(url):
    page = requests.get(url)
    page.raise_for_status() # raises an exception if status_code is not 200
    return html.fromstring(page.text)

def clearTables():
    logUtility.title('Deleting current entries')
    print 'Deleted', db.course.delete().execute(), 'course(s)'
    print 'Deleted', db.major.delete().execute(), 'major(s)'
    print '...done\n'

def insertMajors():
    if(db.major.select().count() != 0):
        error = 'Tried to call insertMajors() with non-empty majors table'
        error += '\n--> Hint: call clearTables() first'
        logUtility.error(error)
        return

    logUtility.title('Inserting Majors in Database')
    tree = getPageTree(MAJOR_LIST_URL)    
    majorCodes = tree.xpath(MAJOR_XPATH + '/@value')
    majorNames = tree.xpath(MAJOR_XPATH + '/text()')
    majorList = map((lambda (a,b): (a.strip(), b.strip())), zip(majorCodes,\
        majorNames))
    
    row_dict = [{ \
        'major_code': code, \
        'major_name': name \
        } for (code,name) in majorList]
    db.myDB.connect()
    insertQuery = db.major.insert_many(row_dict)
    print 'Inserting', len(row_dict), 'majors'
    print 'First primary key inserted:', insertQuery.execute()
    
    db.myDB.close()
    print '...done'

def insertCourses():
    if(db.course.select().count() != 0):
        error = 'Tried to call insertCourses() with non-empty table "course"'
        error += '\n--> Hint: call clearTables() first'
        logUtility.error(error)
        return

    if(db.major.select().count() == 0):
        warning = 'Calling insertCourses() with empty table "major"'
        logUtility.warning(warning)

    logUtility.title('Inserting Courses in Database')

    majors = db.major.select()
    db.myDB.connect()
    
    numCourses = 0
    courselessMajors = []
    for curMajor in majors:
        print '>>> Processing', curMajor.major_code, 'courses'
        curMajorCode = re.sub(' ', '+', curMajor.major_code)
        curMajorCode = re.sub('&', '%26', curMajorCode)
        tree = getPageTree(COURSE_LIST_URL + curMajorCode)
        courseCodes = tree.xpath(COURSE_XPATH + '/@value')
        courseNames = tree.xpath(COURSE_XPATH + '/text()')
        courseList = map((lambda (a,b): (a.strip(), b.strip())),\
                zip(courseCodes, courseNames))
        courseListLen = len(courseList)
        
        if(courseListLen == 0):
            print 'No courses this quarter, moving on to next major\n'
            courselessMajors.append(curMajor.major_name)
            continue

        row_dict = [{ \
            'major': curMajor, \
            'course_code': code, \
            'course_name': name, \
            } for (code,name) in courseList]
        insertQuery = db.course.insert_many(row_dict)
        print 'Inserting', courseListLen, 'courses' 
        print 'Insert new classes: first primary key inserted =', insertQuery.execute()
        print ''
        numCourses += courseListLen
    # end for
    db.myDB.close()
    print 'Added', numCourses, 'courses'
    print 'The following majors have no courses this quarter:'
    for major in courselessMajors:
        print '-', major

    print '...done\n'


