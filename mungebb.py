import csv
import re

def fix(s):
   while '<' in s:
      s=s[:s.index('<')]+s[s.index('>')+1:]
   s=re.sub('[^0-9]','',s)
   s=s[:4]
   return s   


fileid = open('prefs-fixed.csv', mode='rb')
reader = csv.reader(fileid)

for row in reader:
   if len(re.sub('[^0-9]','',row[0]))==8:
      c=list()
      t=0
      for i in [5,11,17,23,29]:
         n=fix(row[i])
         if n:
            t=t+int(n[0])
            c.append(n)
         else:
            c="Err"
      if len(c)==5:
         print row[0]+","+str(c[0])+","+str(c[1])+","+str(c[2])+","+str(c[3])+","+str(c[4])
