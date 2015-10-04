#!/usr/bin/python

import csv
from random import sample, shuffle

Project = {}
Lecturer = {}
Student = {}
M=[]

def csvInit(filename):
   Project.clear()
   Lecturer.clear()
   Student.clear()

   fileid = open(filename, mode='r')
   reader = csv.reader(fileid)

   ProjectsSource = {}
   for row in reader:
      if row[0]=='Project Definitions':
         reader.next() #Skip Headers
      elif row[0]=='':
         break 
      else:
         sourceid = row[0]
         limit = int(row[1])
         title = row[2]
         ProjectsSource[sourceid]={'limit':limit,'title':title}

   destid=0
   for row in reader:
      if row[0]=='Lecturer Preferences':
         reader.next() #Skip Headers
      elif row[0]=='':
         break
      else:
         projects = []
         for sourceid in row[2:]:
            if sourceid!='':
               p=ProjectsSource[sourceid]
               Project[destid]=p
               projects.append(destid)
               destid+=1
         Lecturer[row[0]]={'limit':int(row[1]), 'projects':projects}

   for row in reader:
      if row[0]=='Student Preferences':
         reader.next() #Skip Headers
      elif row[0]=='':
         break
      else:
         destids = []
         for sourceid in row[1:]:
            if sourceid!='':
               p=ProjectsSource[sourceid]
               pidlist=[]
               for pid in Project:
                  px=Project[pid]
                  if p['title']==px['title']:
                     pidlist.append(pid)
               shuffle(pidlist) #Shuffle to random pid order for a student (fairer)
               destids.extend(pidlist)
         Student[row[0]]={'projects':destids}

   fileid.close()

def isStudentAssigned(s):
   for m in M:
      if m['student'] == s:
         return True
   return False

def getSomeUnassignedStudentWithNonEmptyList():
   for s in sample(Student,len(Student)):
      w = Student[s]
      if not isStudentAssigned(s) and len(w['projects'])>0:
         return s

def getLecturerOffering(p):
   for l in Lecturer:
      w = Lecturer[l]
      if p in w['projects']:
         return l
   print("Err: No supervisors for this project")

def isProjectFull(p):
   c=0
   for m in M:
      if m['projectid']==p:
         c+=1
   return c==Project[p]['limit']

def isLecturerFull(l):
   c=0
   for m in M:
      if m['lecturer']==l:
         c+=1
   return c==Lecturer[l]['limit']

def isLecturerOversubscribed(l):
   c=0
   for m in M:
      if m['lecturer']==l:
         c+=1
   return c>Lecturer[l]['limit']

def isProjectAllocated(p):
   for m in M:
      if m['projectid']==p:
         return True
   return False

def getSomeStudentDoing(p):
   for m in sample(M,len(M)):
      if m['projectid']==p:
         return m['student']
   print("Err: No students doing this project")

def getWorstNonEmptyProject(l):
   for p in reversed(Lecturer[l]['projects']):
      if isProjectAllocated(p):
         return p
   print("Err: No allocations for this lecturer")

def AddToM(s,l,p):
   r = {
      'student': s,
      'lecturer': l,
      'projectid': p
   }
   M.append(r)

def RemoveFromM(s,l,p):
   for m in M:
      if m['student']==s and m['lecturer']==l and m['projectid']==p:
         M.remove(m)
         return

def SPA():
   global M
   M=[]

   si=getSomeUnassignedStudentWithNonEmptyList()
   while(si!=None):
      pj=Student[si]['projects'][0]             #first project of si's list
      lk=getLecturerOffering(pj)                #lecturer who offers pj
      if isProjectFull(pj):
         Student[si]['projects'].remove(pj)     #delete pj from si's list
      else:
         AddToM(si,lk,pj)
         if isLecturerOversubscribed(lk):
            pz = getWorstNonEmptyProject(lk)    #lk's worst non-empty project
            sr = getSomeStudentDoing(pz)
            RemoveFromM(sr,lk,pz)
            Student[si]['projects'].remove(pj)  #delete pz from sr's list
         if isLecturerFull(lk):
            pz = getWorstNonEmptyProject(lk)    #lk's worst non-empty project
            successor = False
            for p in Lecturer[lk]['projects']:
               if successor:
                  for s in Student:
                     w=Student[s]
                     if p in w['projects']:
                        w['projects'].remove(p)
               if p==pz:
                  successor=True
      si=getSomeUnassignedStudentWithNonEmptyList()

#Main

print("MComp")
csvInit("Double_Projects.csv")
SPA()
MCompWorkload={}
for m in M:
   s = m['student']
   l = m['lecturer']
   MCompWorkload[l]=MCompWorkload.get(l,0)+1
   id = m['projectid']
   p = Project[id]['title']
   print(s+","+l+","+p)

print
print("Unassigned Students")
for s in sample(Student,len(Student)):
   if not isStudentAssigned(s):
      print s

print
print("BSc")
csvInit("Single_Projects.csv")
for l in MCompWorkload:
   limit=Lecturer[l]['limit'] - (MCompWorkload[l]*2)
   if limit<=0:
      del Lecturer[l]
   else:
      Lecturer[l]['limit']=limit
SPA()
for m in M:
   s = m['student']
   l = m['lecturer']
   Lecturer[l]['limit'] = Lecturer[l]['limit'] - 1
   id = m['projectid']
   p = Project[id]['title']
   print(s+","+l+","+p)

print
print("Unassigned Students")
for s in sample(Student,len(Student)):
   if not isStudentAssigned(s):
      print s

print
print("Remaining Capacity")
for l in Lecturer:
   limit=Lecturer[l]['limit']
   if(limit>0):
      print(l+" has "+str(limit)+" supervisions free")
