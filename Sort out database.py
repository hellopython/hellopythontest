#!/usr/bin/env python
import sys
import re
if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + "table" 
    print "eg: " + sys.argv[0] + "csdn"
    sys.exit() 
table = sys.argv[1]

sqlfile = open('sql.txt','r')
sql_result = open('sql_result.txt','a')

print 'read data now,please wait.....'
count = len(open('sql.txt','rU').readlines())
print count
for x in range(count):
        sql=sqlfile.readline()
        result=re.split('#',sql)
        result[2]=result[2].rstrip('\n')
        sql_change="INSERT INTO `%s` (`username`, `password`, `email`) VALUES ('%s', '%s', '%s');\n"%(table,result[0],result[1],result[2])
        sql_result.write(sql_change)
sqlfile.close()
sql_result.close()