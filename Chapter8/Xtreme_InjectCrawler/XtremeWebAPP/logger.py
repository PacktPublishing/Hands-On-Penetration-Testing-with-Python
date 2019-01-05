"""Logger module for XTreme Project"""

import time

class Logger(object):
    """Logger class for logging every important event in the discovery process"""

    def __init__(self, write_to_file = False):
        self.file_write = write_to_file


    def log(self, string, Type, REPORT_FILE=None):
        if not Type:
            Type = 'INFO'
        #print "[%s] - %s: %s" % (time.ctime(), Type.upper(), string)
        print "[%s] - %s: %s" % (time.ctime(), Type, string.encode('utf-8'))
        #write to pdf file
        if REPORT_FILE and Type.find("VULNERABILITY FOUND")!=-1:
                with open(REPORT_FILE, 'a') as f:
                    f.writelines("%s \n %s \n %s \n \n" % (time.ctime(), Type, string))



if __name__ == "__main__":
    logger = Logger()
    logger.log('checking!', 'warning')
    logger.log('abcd')
