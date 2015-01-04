def title(title):
    border = '+'
    for i in range(0, len(title) + 2):
        border += '-'
    border += '+'
    print border
    print '|', title, '|'
    print border

def error(error):
    print 'ERROR:', error

def warning(warning):
    print 'WARNING:', warning
