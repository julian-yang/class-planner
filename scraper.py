from lxml import html
import requests
import classPlannerDB as db

DEFAULT_scheduleHomeURL = 'http://www.registrar.ucla.edu/schedule/schedulehome.aspx'
DEFAULT_scheduleMajorURL = 'http://www.registrar.ucla.edu/schedule/crsredir.aspx' #termsel=14S&subareasel=COM+SCI
# DEFAULT TAG NAMES HERE
DEFAULT_majorListWrapperId = 'ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea'

# XPATHS HERE
MAJOR_XPATH = '//select[@id="' + DEFAULT_majorListWrapperId + '"]/*'




#test = majors.select()

#for major in test:
#    print major.major_code, major.major_name

def updateMajors():
    page = requests.get(DEFAULT_scheduleHomeURL)
    tree = html.fromstring(page.text)
    
    majorNames = tree.xpath(MAJOR_XPATH + '/text()')
    majorCodes = tree.xpath(MAJOR_XPATH + '/@value')
    majorList = zip(majorCodes, majorNames)
    
    db.myDB.connect()
    # erase the old majors
    db.myDB.execute_sql('TRUNCATE TABLE majors')
    db.majors \
        .insert_many([{'major_code': code, 'major_name': name} \
            for (code,name) in majorList]) \
        .execute()

    db.myDB.close()

    



