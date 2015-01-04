from lxml import html
import requests
import peewee as pw
import config

DEFAULT_scheduleHomeURL = 'http://www.registrar.ucla.edu/schedule/schedulehome.aspx'
DEFAULT_scheduleMajorURL = 'http://www.registrar.ucla.edu/schedule/crsredir.aspx' #termsel=14S&subareasel=COM+SCI
# DEFAULT TAG NAMES HERE
DEFAULT_majorListWrapperId = 'ctl00_BodyContentPlaceHolder_SOCmain_lstSubjectArea'

# XPATHS HERE
MAJOR_XPATH = '//select[@id="' + DEFAULT_majorListWrapperId + '"]/*'

myDB = pw.MySQLDatabase(\
            config.db['name'], \
            host = config.db['host'], \
            user = config.db['user'],\
            passwd = config.db['passwd'])

class BaseModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB

class majors(BaseModel):
    id = pw.PrimaryKeyField()
    major_code = pw.CharField(max_length=255)
    major_name = pw.CharField(max_length=255)

myDB.connect()

#test = majors.select()

#for major in test:
#    print major.major_code, major.major_name

def updateMajors():
    page = requests.get(DEFAULT_scheduleHomeURL)
    tree = html.fromstring(page.text)
    

    majorNames = tree.xpath(MAJOR_XPATH + '/text()')
    majorCodes = tree.xpath(MAJOR_XPATH + '/@value')
    #print 'MajorNames: ', majorNames
    #print 'MajorCodes: ', majorCodes

    majorList = zip(majorCodes, majorNames)
    
    # erase the old majors
    myDB.execute_sql('TRUNCATE TABLE majors')
    # insert the new majors
    majors \
        .insert_many([{'major_code': code, 'major_name': name} \
            for (code,name) in majorList]) \
        .execute()

