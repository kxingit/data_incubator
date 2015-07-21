#!/usr/bin/python

import xml.etree.ElementTree as ET
import numpy

# q2.1
tree = ET.parse("Tags.xml")
root = tree.getroot()

data = []
for row in root.findall('row'):
    tag = row.get('TagName')
    count = int(row.get('Count'))
    #    print tag, count
    data.append((count,tag))
data.sort(reverse=True)
#print data
print data[:5]

count_all = 0
for row in root.findall('row'):
    tag = row.get('TagName')
    count = int(row.get('Count'))
    count_all += count
print count_all
print "fraction = ", float(data[4][0]) / count_all

# q2.2
tree = ET.parse("Posts.xml")
root = tree.getroot()

score_q = 0
n_q = 0
score_ans = 0
n_ans = 0
for row in root.findall('row'):
    type = int(row.get('PostTypeId'))
    score = int(row.get('Score'))
    #    print type
    if type == 1:
        score_q += score
        n_q += 1
    elif type == 2:
        score_ans += score
        n_ans += 1
print "ave q score = ", float(score_q) / n_q
print "ave ans score = ", float(score_ans) / n_ans
print float(score_ans) / n_ans - float(score_q) / n_q, " higher"

# q.2.3
tree = ET.parse("Users.xml")
root = tree.getroot()
tRep = {}
for row in root.findall('row'):
    userId = row.get('Id')
    reputation = int(row.get('Reputation'))
    #    print tag, count
    tRep[userId] = reputation
#print "print tRep", tRep

tree = ET.parse("Posts.xml")
root = tree.getroot()
list_score = []
list_rep = []
for row in root.findall('row'):
    score = int(row.get('Score'))
    userId = row.get('OwnerUserId')
    #print score, userId
    reputation = tRep.get(userId)
    #print reputation
    if userId != None:
        list_score.append(score)
        list_rep.append(reputation)

print numpy.ma.corrcoef(list_score,list_rep)[0,1]


