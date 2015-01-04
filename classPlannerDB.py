import peewee as pw
import config 

myDB = pw.MySQLDatabase(\
            config.db['name'], \
            host = config.db['host'], \
            user = config.db['user'],\
            passwd = config.db['passwd'])

class BaseModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB

class major(BaseModel):
    id = pw.PrimaryKeyField()
    major_code = pw.CharField(max_length=255)
    major_name = pw.CharField(max_length=255)
    
class course(BaseModel):
    id = pw.PrimaryKeyField()
    major = pw.ForeignKeyField(major, related_name='courses')
    course_code = pw.CharField(max_length=255)
    course_name = pw.CharField(max_length=255)

def createTables():
    myDB.connect()
    myDB.create_tables([major, course])
    myDB.close()
