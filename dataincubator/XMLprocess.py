#!/usr/bin/python
'''
Created on Jul 15, 2015

@author: gogqou
'''

import sys
import xml.etree.ElementTree as ET
import xml
import glob
import os
import collections
import numpy as np
from scipy.stats.stats import pearsonr
########################################################
                                                     ###
def tagSorting(xmlTree):
    root = xmlTree.getroot()
    tags_counts = []
    i = 5 #  return the ith most popular tag
    for row in root.findall('row'):
        
        count = int(row.get('Count'))
        tag = row.get('TagName')
        tags_counts.append((tag, count))
    tags_counts = sorted(tags_counts, key = lambda tag:tag[1], reverse= True)
    return tags_counts[i-1]
                                                    ###
#######################################################

#######################################################
                                                     ##
def postsCount(xmlTree):
    root = xmlTree.getroot()
    postCount = 0
    for row in root.findall('row'):
        if 'Tags' in row.attrib:
            #print row.attrib 
            postCount = postCount + 1
    
    return postCount
#######################################################
def scoring(xmlTree):
    root = xmlTree.getroot()
    post_total_score = 0
    answer_total_score = 0
    postCount = 0
    answerCount = 0
    for row in root.findall('row'):
        #PostTypeId = 1 means it's a question
        if row.attrib['PostTypeId']=='1':
            post_total_score = float(row.attrib['Score'])+post_total_score
            postCount = postCount +1
        elif row.attrib['PostTypeId']==2:
            answer_total_score = float(row.attrib['Score'])+answer_total_score
            answerCount = answerCount +1
    post_average_score = float(post_total_score)/postCount
    
    answer_average_score = float(answer_total_score)/answerCount
    return post_average_score, answer_average_score
                                                    ###
#######################################################
                                                    ###
def userRep(userxmlTree, postxmlTree):
    userRoot = userxmlTree.getroot()
    postRoot = postxmlTree.getroot()
    userDict = collections.defaultdict(list)
    for child in userRoot:
        userDict[child.attrib['Id']].append(float(child.attrib['Reputation']))
        userDict[child.attrib['Id']].append(0)
    for child in postRoot:
        if 'OwnerUserId' in child.attrib.keys():
            if child.attrib['OwnerUserId'] in userDict:
                #print userDict[child.attrib['OwnerUserId']]
                #print child.attrib['OwnerUserId'], userDict[child.attrib['OwnerUserId']]
                userDict[child.attrib['OwnerUserId']][1] = userDict[child.attrib['OwnerUserId']][1] + float(child.attrib['Score'])
    full_array = np.empty([len(userDict), 2])
    i = 0
    for value in userDict.itervalues():
        full_array[i]=value
        i=i+1
    print full_array    
    PearsonCorrelation = pearsonr(full_array[:,0], full_array[:,1])    
    return PearsonCorrelation
                                                    ###
#######################################################
def upVotes(postxmlTree, votesxmlTree):
    postsRoot = postxmlTree.getroot()
    votesRoot = votesxmlTree.getroot()
    voteDict = collections.defaultdict(list)
    
    for row in votesRoot.findall('row'):
        if row.attrib['VoteTypeId']=='2':
            print row.attrib['PostId']
            voteDict[row.attrib['PostId']] = voteDict[row.attrib['PostId']].append(1)
    print voteDict.keys()
    
    #for child in votesRoot:
     #   print(child.tag, child.attrib)
    return 1
######################################################
                                                    ##
                                                    ##                                                        
def parseXML():
    homePath = sys.argv[1]
    files = os.listdir(homePath)
    for file in files:
        if '.gz' not in file:
            filename, ext = os.path.splitext(file)
            path = homePath + file
    
    #Question 1        
#     Tagsfile = homePath +'Tags.xml'
#     tagsTree = ET.parse(Tagsfile)
    Postsfile = homePath + 'Posts.xml'
    postsTree = ET.parse(Postsfile)
#     ithTag= tagSorting(tagsTree)
#     ithTagCount = float(ithTag[1])
    #postCount = postsCount(postsTree)
    
#     print 'Fraction of posts with fifth most popular tag = ', ithTagCount/postCount

    #Question 2
       
    #postAvgScore, answerAvgScore= scoring(postsTree)
    #print 'Post Avg Score = ', postAvgScore, 'Answer Avg Score = ', answerAvgScore
    
    #Question 3
    #Usersfile = homePath + 'Users.xml'
    #userTree = ET.parse(Usersfile)
    #correlationP = userRep(userTree, postsTree)
    #print 'Correlation coefficient and two-tailed pvalue= ', correlationP
    #for child in root:
        #print(child.tag, child.attrib)
    
    
    #Question 4
    Votesfile = homePath + 'Votes.xml'
    votesTree = ET.parse(Votesfile)
    upVotes(postsTree, votesTree)
    
    return 1
                                                    ##
######################################################
if __name__ == '__main__':
    parseXML()
