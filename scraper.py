from lxml import html
import requests
import classPlannerDB as db
import re 

MAJOR_LIST_URL = 'http://www.registrar.ucla.edu/schedule/schedulehome.aspx'
COURSE_LIST_URL = 'http://www.registrar.ucla.edu/schedule/crsredir.aspx?termsel=14S&subareasel=' # COM+SCI
# DEFAULT TAG NAMES HERE
MAJOR_LIST_WRAPPER_ID = 'ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea'
CLASS_LIST_WRAPPER_ID = 'ctl00_BodyContentPlaceHolder_crsredir1_lstCourseNormal'
# XPATHS HERE
MAJOR_XPATH = '//select[@id="' + MAJOR_LIST_WRAPPER_ID + '"]/*'
COURSE_XPATH = '//select[@id="' + CLASS_LIST_WRAPPER_ID + '"]/*'
# OTHER VARS HERE
CUR_TERM = '14S'



#test = majors.select()

#for major in test:
#    print major.major_code, major.major_name
def printTitle(title):
    border = '+'
    for i in range(0, len(title) + 2):
        border += '-'
    border += '+'
    print border
    print '|', title, '|'
    print border

def printError(error):
    print 'ERROR:', error

def printWarning(warning):
    print 'WARNING:', warning

def getPageTree(url):
    page = requests.get(url)
    page.raise_for_status() # raises an exception if status_code is not 200
    return html.fromstring(page.text)

def clearTables():
    printTitle('Deleting current entries')
    print 'Deleted', db.course.delete().execute(), 'major(s)'
    print 'Deleted', db.major.delete().execute(), 'course(s)'
    print '...done\n'

def insertMajors():
    if(db.major.select().count() != 0):
        error = 'Tried to call insertMajors() with non-empty majors table'
        error += '\n--> Hint: call clearTables() first'
        printError(error)
        return

    printTitle('Inserting Majors in Database')
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
        printError(error)
        return

    if(db.major.select().count() == 0):
        warning = 'Calling insertCourses() with empty table "major"'
        printWarning(warning)

    printTitle('Inserting Courses in Database')

    majors = db.major.select()
    db.myDB.connect()

    for curMajor in majors:
        print '>>> Processing', curMajor.major_code, 'courses'
        tree = getPageTree(COURSE_LIST_URL + 'COM+SCI')
        courseCodes = tree.xpath(COURSE_XPATH + '/@value')
        courseNames = tree.xpath(COURSE_XPATH + '/text()')
        courseList = map((lambda (a,b): (a.strip(), b.strip())),\
                zip(courseCodes, courseNames))
        
        row_dict = [{ \
            'major': curMajor, \
            'course_code': code, \
            'course_name': name, \
            } for (code,name) in courseList]
        insertQuery = db.course.insert_many(row_dict)
            
        print 'Insert new classes: first primary key inserted =', insertQuery.execute()
        print ''
    # end for
    db.myDB.close()
    print '...done\n'


