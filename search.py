import json,requests
import sys
import numpy as np

from req import Req
from map import Map
from house import House

class Search():

    g = ""
    ranking = []
    paramlist = []

    def __init__(self):
        pass

    #params is a list of addresses
    #params in order: Work, Edu, Other1, Other2, Other3
    def search(self,city,params,low,high):
        reqo=Req()
        mapo=Map()

        self.g = reqo.initialSearch(city,low,high)

        nHouses = json.loads(self.g.text)['total_records']
        temp = [House(0,0,0) for i in range(nHouses)]

        nParams = len(params)

        paramlist = [x for x in params if x is not None]

        nParams = len(paramlist)

        for i in range(0,nHouses):
            lat=json.loads(self.g.text)['results'][i]['lat']
            lng=json.loads(self.g.text)['results'][i]['long']
            mlsid=json.loads(self.g.text)['results'][i]['mls_id']

            temp[i]=House(mlsid,lat,lng)

            if(nParams>=1):
                temp[i].setWTime(mapo.getDistanceTime((lat,lng),mapo.getGeoCode(paramlist[0])))
            if(nParams>=2):
                temp[i].setETime(mapo.getDistanceTime((lat,lng),mapo.getGeoCode(paramlist[1])))
            if(nParams>=3):
                temp[i].set1Time(mapo.getDistanceTime((lat,lng),mapo.getGeoCode(paramlist[2])))
            if(nParams>=4):
                temp[i].set2Time(mapo.getDistanceTime((lat,lng),mapo.getGeoCode(paramlist[3])))
            if(nParams>=5):
                temp[i].set3Time(mapo.getDistanceTime((lat,lng),mapo.getGeoCode(paramlist[4])))
        print("\n")

        return temp

    def bestHouseCandidate(self,list):
        lowaff=sys.maxsize
        mlsid = 0
        for i in list:
            if(self.ranking[1]!=None):
                i.setAffinity((5-float(self.ranking[0]))*(i.getWTime()/60)+(5-float(self.ranking[1]))*(i.getETime()/60))
            else:
                i.setAffinity((5-float(self.ranking[0]))*(i.getWTime()/60))
            if(i.getAffinity()<lowaff):
                lowaff=i.getAffinity()
                mlsid = i.getID()
        return mlsid
       
    def findHouseFromID(self,id):
        data=''
        for i in range(0,json.loads(self.g.text)['total_records']):
            if(json.loads(self.g.text)['results'][i]['mls_id']==id):
                data=json.loads(self.g.text)['results'][i]
        print(data)
        return data

    def setRanking(self,Ranking):
        self.ranking=Ranking

    def getRanking(self):
        return self.ranking


#d = Search()
#params=['Mount Carmel West','Dodge Rec Center']
#templist = d.search('Columbus',params,0,100000)



#for i in templist:
#    print(i)
