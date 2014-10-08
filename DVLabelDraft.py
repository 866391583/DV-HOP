#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrator
#
# Created:     05-10-2014
# Copyright:   (c) Administrator 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import numpy as np
import matplotlib.pyplot as plt
import math
D=5
S=6
S1=7
S2=8
U=9
N=0
WL=-5
INF=1000
class DVHop:
    def __init__(self):
##        self.R=20
        self.BorderLen=100
        self.NodeCount=100
        self.R=20
        self.DeployArr=np.arange(self.NodeCount)


        self.GAMtx=np.zeros((2,2))
        self.GBMtx=np.zeros(2)
        self.distMtxRef=np.zeros((self.NodeCount,self.NodeCount))
        self.distMtx=np.zeros((self.NodeCount,self.NodeCount))

        self.NodeCoordinateReference=np.zeros((2,self.NodeCount))
        self.NodeCoordinate=np.zeros((2,self.NodeCount))
        for idx in range(10):
            for inner in range(10):
                self.NodeCoordinateReference[0,idx*10+inner]=idx*10+np.random.random()*10
                self.NodeCoordinateReference[1,idx*10+inner]=inner*10+np.random.random()*10
        for idx in range(self.NodeCount):
            for inner in range(self.NodeCount):
                self.distMtxRef[idx,inner]=math.sqrt(math.pow(self.NodeCoordinateReference[0,idx]-self.NodeCoordinateReference[0,inner],2)+math.pow(self.NodeCoordinateReference[1,idx]-self.NodeCoordinateReference[1,inner],2))
                self.distMtxRef[inner,idx]=self.distMtxRef[idx,inner]
    def initScenario(self):

        self.hopMtxRef=np.ones((self.NodeCount,self.NodeCount))*(1000)
        self.hopMtx=np.ones((self.NodeCount,self.NodeCount))*(1000)






##        self.NodeCoordinate=np.zeros((2,self.NodeCount))
##        for idx in range(2):
##            for inner in range(self.NodeCount):
##                self.NodeCoordinate[idx,inner]=np.floor(np.random.random())

##        self.NodeCoordinateReference=np.random.random((2,self.NodeCount))*self.BorderLen
##        self.NodeCoordinate=np.zeros((2,self.NodeCount))


    def generateMalicious(self):
        self.MalCoordinate=np.zeros((2,2))
        self.MalCoordinate[0,0]=np.random.random()*10+20
        self.MalCoordinate[0,1]=np.random.random()*10+70
        for idx in range(2):
            self.MalCoordinate[1,idx]=np.random.random()*100

    def deployMalicious(self):
        self.DectaionList=np.zeros((2,self.NodeCount+1))
        for idx in range(self.NodeCount):
            for inner in range(2):
                if math.sqrt(math.pow(self.NodeCoordinateReference[0,idx]-self.MalCoordinate[0,inner],2)+math.pow(self.NodeCoordinateReference[1,idx]-self.MalCoordinate[1,inner],2))<self.R:
                    self.DectaionList[inner,0]+=1
                    self.DectaionList[inner,self.DectaionList[inner,0]]=idx;
        for idx in range(int(self.DectaionList[0,0])):
            for inner in range(int(self.DectaionList[1,0])):
                self.hopMtxRef[self.DectaionList[0,idx+1],self.DectaionList[1,inner+1]]=1
                self.hopMtxRef[self.DectaionList[1,inner+1],self.DectaionList[0,idx+1]]=1
    def labelAnchor(self):
        for idx in range(self.AchorCount):
            if math.pow(self.MalCoordinate[0,0]-self.NodeCoordinate[0,idx],2)+math.pow(self.MalCoordinate[1,0]-self.NodeCoordinate[1,idx],2)<math.pow(self.R,2) and math.pow(self.MalCoordinate[0,1]-self.NodeCoordinate[0,idx],2)+math.pow(self.MalCoordinate[1,1]-self.NodeCoordinate[1,idx],2)<math.pow(self.R,2):
                self.LabelArr[idx]=D
            else:
                for inner in range(self.AchorCount):
                    if self.hopMtx[idx,inner]==1:
                        if self.distMtx[idx,inner]>=self.R:
                            self.LabelArr[idx]=S
                            self.LabelMtx[idx,inner]=WL
                        if self.distMtx[idx,inner]<self.R:
                            if math.pow(self.MalCoordinate[0,0]-self.NodeCoordinate[0,idx],2)+math.pow(self.MalCoordinate[1,0]-self.NodeCoordinate[1,idx],2)<math.pow(self.R,2) and math.pow(self.MalCoordinate[0,1]-self.NodeCoordinate[0,inner],2)+math.pow(self.MalCoordinate[1,1]-self.NodeCoordinate[1,inner],2)<math.pow(self.R,2):
                                self.LabelArr[idx]=S
                                self.LabelMtx[idx,inner]=WL
                            elif math.pow(self.MalCoordinate[0,0]-self.NodeCoordinate[0,inner],2)+math.pow(self.MalCoordinate[1,0]-self.NodeCoordinate[1,inner],2)<math.pow(self.R,2) and math.pow(self.MalCoordinate[0,1]-self.NodeCoordinate[0,idx],2)+math.pow(self.MalCoordinate[1,1]-self.NodeCoordinate[1,idx],2)<math.pow(self.R,2):
                                self.LabelArr[idx]=S
                                self.LabelMtx[idx,inner]=WL
        for idx in range(self.AchorCount):
            minID=self.NodeCount
            minIdx=-1
            if self.LabelArr[idx]==S and self.DeployArr[idx]<minID:
                minID=self.DeployArr[idx]
                minIdx=idx
        for idx in range(self.AchorCount):
            if self.LabelArr[idx]==S:
                if all(self.LabelMtx[idx]==self.LabelMtx[minIdx]):
                    self.LabelArr[idx]=S1
                else:
                    self.LabelArr[idx]=S2
    def labelUnknown(self):
        for idx in range(self.AchorCount,self.NodeCount):
            if math.pow(self.MalCoordinate[0,0]-self.NodeCoordinate[0,idx],2)+math.pow(self.MalCoordinate[1,0]-self.NodeCoordinate[1,idx],2)<math.pow(self.R,2) and math.pow(self.MalCoordinate[0,1]-self.NodeCoordinate[0,idx],2)+math.pow(self.MalCoordinate[1,1]-self.NodeCoordinate[1,idx],2)<math.pow(self.R,2):
                self.LabelArr[idx]=D
            else:
                for inner in range(self.NodeCount):
                    if self.hopMtx[idx,inner]==1:
                        if self.distMtx[idx,inner]<self.R:
                            if math.pow(self.MalCoordinate[0,0]-self.NodeCoordinate[0,idx],2)+math.pow(self.MalCoordinate[1,0]-self.NodeCoordinate[1,idx],2)<math.pow(self.R,2) and math.pow(self.MalCoordinate[0,1]-self.NodeCoordinate[0,inner],2)+math.pow(self.MalCoordinate[1,1]-self.NodeCoordinate[1,inner],2)<math.pow(self.R,2):
                                self.LabelArr[idx]=S
                                if inner<self.AchorCount:
                                    if self.LabelArr[inner]==S1:
                                        self.LabelArr[idx]=S2
                                    elif self.LabelArr[inner]==S2:
                                        self.LabelArr[idx]=S1
##                                self.LabelMtx[idx,inner]=WL
                            elif math.pow(self.MalCoordinate[0,0]-self.NodeCoordinate[0,inner],2)+math.pow(self.MalCoordinate[1,0]-self.NodeCoordinate[1,inner],2)<math.pow(self.R,2) and math.pow(self.MalCoordinate[0,1]-self.NodeCoordinate[0,idx],2)+math.pow(self.MalCoordinate[1,1]-self.NodeCoordinate[1,idx],2)<math.pow(self.R,2):
                                self.LabelArr[idx]=S
                                if inner<self.AchorCount:
                                    if self.LabelArr[inner]==S1:
                                        self.LabelArr[idx]=S2
                                    elif self.LabelArr[inner]==S2:
                                        self.LabelArr[idx]=S1
##                                self.LabelMtx[idx,inner]=WL
                if self.LabelArr[idx]!=S1 and self.LabelArr[idx]!=S2:
                    tmpArr=np.arange(self.AchorCount)
                    tmpIdx=0
                    for inner in range(self.AchorCount):
                        if self.hopMtx[idx,inner]==1:
                            tmpArr[tmpIdx]=inner
                            tmpIdx+=1
                    if tmpIdx>1:
                        for idxI in range(tmpIdx-1):
                            for idxJ in range(idxI+1,tmpIdx):
                                if math.pow(self.NodeCoordinate[0,idxI]-self.NodeCoordinate[0,idxJ],2)+math.pow(self.NodeCoordinate[1,idxI]-self.NodeCoordinate[1,idxJ],2)<4*math.pow(self.R,2):
                                    self.LabelArr[idx]=S
                                    if self.LabelArr[idxI]==N:
                                        if self.LabelArr[idxJ]==S1:
                                            self.LabelArr[idx]=S2
                                        elif self.LabelArr[idxJ]==S2:
                                            self.LabelArr[idx]=S1
                                    elif self.LabelArr[idxJ]==N:
                                        if self.LabelArr[idxI]==S1:
                                            self.LabelArr[idx]=S2
                                        elif self.LabelArr[idxI]==S2:
                                            self.LabelArr[idx]=S1






    def removeWL(self):
        for idx in range(self.NodeCount):
            for inner in range(idx+1):
                if self.hopMtx[idx,inner]==1:
                    if self.LabelArr[idx]==D:
                        if self.LabelArr[inner]==D and self.distMtx[idx,inner]>self.R:
                            self.hopMtx[idx,inner]=INF
                            self.hopMtx[inner,idx]=INF
                        if (self.LabelArr[inner]==S or self.LabelArr[inner]==S1 or self.LabelArr[inner]==S2) and self.distMtx[idx,inner]>self.R:
                            self.hopMtx[idx,inner]=INF
                            self.hopMtx[inner,idx]=INF
                    elif self.LabelArr[idx]==S1:
                        if self.LabelArr[inner]==D and self.distMtx[idx,inner]>self.R:
                            self.hopMtx[idx,inner]=INF
                            self.hopMtx[inner,idx]=INF
                        elif self.LabelArr[inner]==S2 and self.distMtx[idx,inner]>self.R:
                            self.hopMtx[idx,inner]=INF
                            self.hopMtx[inner,idx]=INF
                    elif self.LabelArr[idx]==S2:
                        if self.LabelArr[inner]==D and self.distMtx[idx,inner]>self.R:
                            self.hopMtx[idx,inner]=INF
                            self.hopMtx[inner,idx]=INF
                        elif self.LabelArr[inner]==S1 and self.distMtx[idx,inner]>self.R:
                            self.hopMtx[idx,inner]=INF
                            self.hopMtx[inner,idx]=INF



    def removeMalicious(self):
        self.LabelArr=np.zeros(self.NodeCount)
        self.LabelMtx=np.zeros((self.NodeCount,self.NodeCount))
        self.labelAnchor()
        self.labelUnknown()
        self.removeWL()


##        self.NodeCoodT=self.NodeCoordinateReference.T
##        print self.NodeCoordinateReference
    def setRatio(self,ratio):
        self.Ratio=ratio
        self.R=20
        self.AchorCount=int(math.floor(self.NodeCount*self.Ratio))
        self.UnknownCount=self.NodeCount-self.AchorCount
        self.AHS=np.zeros(self.AchorCount)
        self.EstimateXYMtx=np.zeros((2,self.UnknownCount))
        self.UnknownAHS=np.zeros(self.UnknownCount)
        self.Un2AchorDistMtx=np.zeros((self.UnknownCount,self.AchorCount))
        self.CordDiff=np.zeros(self.UnknownCount)
        self.GroupCount=self.AchorCount*(self.AchorCount-1)*(self.AchorCount-2)/6
        self.GroupXYHD=np.zeros((4,self.GroupCount))
        self.BestPointXY=np.zeros((2,self.UnknownCount))

    def setR(self,r):
        self.R=r
        self.Ratio=0.2
    def broadcastOneHop(self):
        for idx in range(self.NodeCount):
            for inner in range(self.NodeCount):
                if self.distMtxRef[idx,inner]==0:
                    self.hopMtxRef[idx,inner]=0
                elif self.distMtxRef[idx,inner]<self.R:
                    self.hopMtxRef[idx,inner]=1
    def broadcastShotestPath(self):
         for idxK in range(self.NodeCount):
            for idxI in range(self.NodeCount):
                for idxJ in range(self.NodeCount):
                    if self.hopMtxRef[idxI,idxJ]>self.hopMtxRef[idxI,idxK]+self.hopMtxRef[idxK,idxJ]:
                        self.hopMtxRef[idxI,idxJ]=self.hopMtxRef[idxI,idxK]+self.hopMtxRef[idxK,idxJ]
    def broadcastShortestPathMtx(self):
         for idxK in range(self.NodeCount):
            for idxI in range(self.NodeCount):
                for idxJ in range(self.NodeCount):
                    if self.hopMtx[idxI,idxJ]>self.hopMtx[idxI,idxK]+self.hopMtx[idxK,idxJ]:
                        self.hopMtx[idxI,idxJ]=self.hopMtx[idxI,idxK]+self.hopMtx[idxK,idxJ]
    def stepBroadcast(self):
        self.broadcastOneHop()
        self.broadcastShotestPath()
##        print '*'*80
##        print self.distMtxRef
    def deployNode(self):
        np.random.shuffle(self.DeployArr)
        for idx in range(self.NodeCount):
            self.NodeCoordinate[:,idx]=self.NodeCoordinateReference[:,self.DeployArr[idx]]
        for idx in range(self.NodeCount):
            for inner in range(self.NodeCount):
                self.distMtx[idx,inner]=self.distMtxRef[self.DeployArr[idx],self.DeployArr[inner]]
                self.hopMtx[idx,inner]=self.hopMtxRef[self.DeployArr[idx],self.DeployArr[inner]]
##        np.random.shuffle(self.NodeCoodT)
##        self.NodeCoordinate=self.NodeCoodT.T
    def stepCaculateAHS(self):

        for idx in range(self.AchorCount):
            sumDist=0
            sumHop=0
            for inner in range(self.AchorCount):
                sumDist=sumDist+self.distMtx[idx,inner]
                sumHop=sumHop+self.hopMtx[idx,inner]
            self.AHS[idx]=sumDist/sumHop
        #print self.AHS
    def generateHopDistMtx(self):
        for idx in range(self.AchorCount,self.NodeCount):
            minIdx=0
            minDist=self.distMtx[idx,0]
            for inner in range(1,self.AchorCount):
                if minDist>self.distMtx[idx,inner]:
                    minIdx=inner
                    minDist=self.distMtx[idx,inner]
            self.UnknownAHS[idx-self.AchorCount]=self.AHS[minIdx]
##        print 'Unknown AHS'*20
##        print self.UnknownAHS

        for idx in range(self.AchorCount,self.NodeCount):
            for inner in range(self.AchorCount):
                self.Un2AchorDistMtx[idx-self.AchorCount,inner]=self.UnknownAHS[idx-self.AchorCount]*self.hopMtx[idx,inner]
    def stepEstimatePosition(self):
##        self.generateHopDistMtx()
        AMtx=np.zeros((self.AchorCount-1,2))
        BMtx=np.zeros(self.AchorCount-1)


        for idxUn in range(self.UnknownCount):
            for idx in range(self.AchorCount-1):
                for inner in range(2):
                    AMtx[idx,inner]=self.NodeCoordinate[inner,idx]-self.NodeCoordinate[inner,self.AchorCount-1]
            AMtx=-2*AMtx
            for idx in range(self.AchorCount-1):
                BMtx[idx]=math.pow(self.Un2AchorDistMtx[idxUn,idx],2)-math.pow(self.Un2AchorDistMtx[idxUn,self.AchorCount-1],2)-math.pow(self.NodeCoordinate[0,idx],2)-math.pow(self.NodeCoordinate[1,idx],2)+math.pow(self.NodeCoordinate[0,self.AchorCount-1],2)+math.pow(self.NodeCoordinate[1,self.AchorCount-1],2)
            tmp=np.dot(np.dot(np.linalg.inv(np.dot(AMtx.T,AMtx)),AMtx.T),BMtx)
            self.EstimateXYMtx[0,idxUn]=tmp[0]
            self.EstimateXYMtx[1,idxUn]=tmp[1]


        avgErr=0
        for idx in range(self.UnknownCount):
            avgErr=avgErr+(math.sqrt(math.pow(self.EstimateXYMtx[0,idx]-self.NodeCoordinate[0,idx+self.AchorCount],2)+math.pow(self.EstimateXYMtx[1,idx]-self.NodeCoordinate[1,idx+self.AchorCount],2))/self.R)
        avgErr=avgErr/self.UnknownCount
##        print 'avgErr',avgErr
        return avgErr
##        print '%'*80
##        print self.NodeCoordinate
##        print '$'*80
##        print self.EstimateXYMtx
##        plt.figure(2)
##        for idx in range(self.UnknownCount):
##            line=plt.plot([self.NodeCoordinate[0,idx+self.AchorCount],self.EstimateXYMtx[0,idx]],[self.NodeCoordinate[1,idx+self.AchorCount],self.EstimateXYMtx[1,idx]],'b-')
##
##        point1,=plt.plot(self.NodeCoordinate[0,0:self.AchorCount],self.NodeCoordinate[1,0:self.AchorCount],'y^')
##        point2,=plt.plot(self.NodeCoordinate[0,self.AchorCount:self.NodeCount],self.NodeCoordinate[1,self.AchorCount:self.NodeCount],'ys')
##        point3,=plt.plot(self.EstimateXYMtx[0,:],self.EstimateXYMtx[1,:],'rs')
##        plt.legend([point1,point2,point3],['Achor Node','Unknown Node','Estimated Position'])
##        plt.title('Traditional DV-HOP:Node Distribution & Estimated Podstion')
##        plt.ylim(0,125)
##        plt.xlim(0,125)
##        plt.show()
    def showNode(self,addMalNode):
        plt.figure(2)

        for idx in range(self.NodeCount):
            for inner in range(self.NodeCount):
                if self.hopMtx[idx,inner]==1:
                    plt.plot([self.NodeCoordinate[0,idx],self.NodeCoordinate[0,inner]],[self.NodeCoordinate[1,idx],self.NodeCoordinate[1,inner]],'b--')

        plt.plot(self.NodeCoordinate[0,:],self.NodeCoordinate[1,:],'ro')
        if addMalNode:
            plt.plot(self.MalCoordinate[0,:],self.MalCoordinate[1,:],'k^-',linewidth=5.0)
        plt.title('Uniform-Random Deployment:Node Distribution')

##        plt.plot(self.EstimateXYMtx[0,:],self.EstimateXYMtx[1,:],'g*')
        plt.show()

def SimulateScenario(dvh,repeatCount,addMalNode,removeMalNode):
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    avgDistErr=np.zeros(6)
    dvDistErr=np.zeros(6)
    dvh.initScenario()
    dvh.broadcastOneHop()
    if addMalNode:
        dvh.deployMalicious()
##    dvh.broadcastShotestPath()
    for outer in np.arange(0.05,0.35,0.05):
        dvh.setRatio(outer)
        for idx in range(repeatCount):
            dvh.deployNode()
            if addMalNode:
                if removeMalNode:
                    dvh.removeMalicious()
            dvh.broadcastShortestPathMtx()
##            dvh.test()
##            dvh.stepBroadcast()
            dvh.stepCaculateAHS()
            dvh.generateHopDistMtx()
##            dvh.stepEstimatePosition()
            avgDistErr[int(outer*20)-1]=avgDistErr[int(outer*20)-1]+dvh.stepEstimatePosition()
##            avgDistErr[int(outer*20)-1]=avgDistErr[int(outer*20)-1]+dvh.stepSelect3Achor()
            dvDistErr[int(outer*20)-1]+=dvh.stepEstimatePosition()
##            print 'repeat',outer,' ',idx
        avgDistErr[int(outer*20)-1]=avgDistErr[int(outer*20)-1]/repeatCount
        dvDistErr[int(outer*20)-1]/=repeatCount
        print outer
    result=np.zeros((2,6))
    result[0,:]=dvDistErr[:]
    result[1,:]=avgDistErr[:]
    return result



    #dvh.showNode()
def tstfun():
    repeatCount=10
    dvh=DVHop()
    dvh.generateMalicious()
    sce0=np.zeros((2,6))
    sce0=SimulateScenario(dvh,repeatCount,False,False)
    dvh.showNode(False)
    sce1=SimulateScenario(dvh,repeatCount,True,False)
    dvh.showNode(True)
    sce2=SimulateScenario(dvh,repeatCount,True,True)
    dvh.showNode(True)

    print '$'*40
    print sce0
    arrX=np.arange(0.05,0.35,0.05)
    plt.figure(1)
    dvLine,=plt.plot(arrX,sce0[0,:],'b--')
##    sel3Line,=plt.plot(arrX,sce0[1,:],'r-')

    dvMalLine,=plt.plot(arrX,sce1[0,:],'r--')
##    sel3MalLine,=plt.plot(arrX,sce1[1,:],'r-.')

    dvRmLine,=plt.plot(arrX,sce2[0,:],'r-')
##    sel3RmLine,=plt.plot(arrX,sce2[1,:],'r--')

    plt.legend([dvLine,dvMalLine,dvRmLine],['DV-HOP','DV-HOP+Wormhole Attack','DV-HOP-Wormhole Attack'])
    plt.xlabel('Achor Ratio')
    plt.ylabel('Localization Error')
    plt.title('Uniform-Random Deployment:Achor Ratio vs Localization Error')
    plt.show()
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #dvh.showNode()



def main():
    pass
    tstfun()



if __name__ == '__main__':
    main()
