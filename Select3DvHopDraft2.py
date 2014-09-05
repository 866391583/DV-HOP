#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrator
#
# Created:     03-09-2014
# Copyright:   (c) Administrator 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import numpy as np
import matplotlib.pyplot as plt
import math
class DVHop:
    def __init__(self):
##        self.R=20
        self.BorderLen=100
        self.NodeCount=100
        self.DeployArr=np.arange(self.NodeCount)
        self.distMtxRef=np.zeros((self.NodeCount,self.NodeCount))
        self.distMtx=np.zeros((self.NodeCount,self.NodeCount))
        self.hopMtxRef=np.ones((self.NodeCount,self.NodeCount))*(1000)
        self.hopMtx=np.ones((self.NodeCount,self.NodeCount))*(1000)
        self.GAMtx=np.zeros((2,2))
        self.GBMtx=np.zeros(2)





##        self.Ratio=ratio
##        self.NodeCoordinate=np.zeros((2,self.NodeCount))
##        for idx in range(2):
##            for inner in range(self.NodeCount):
##                self.NodeCoordinate[idx,inner]=np.floor(np.random.random())
##        self.NodeCoordinateReference=np.random.random((2,self.NodeCount))*self.BorderLen
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

    def stepBroadcast(self):



        for idx in range(self.NodeCount):
            for inner in range(self.NodeCount):
                if self.distMtxRef[idx,inner]==0:
                    self.hopMtxRef[idx,inner]=0
                elif self.distMtxRef[idx,inner]<self.R:
                    self.hopMtxRef[idx,inner]=1
        for idxK in range(self.NodeCount):
            for idxI in range(self.NodeCount):
                for idxJ in range(self.NodeCount):
                    if self.hopMtxRef[idxI,idxJ]>self.hopMtxRef[idxI,idxK]+self.hopMtxRef[idxK,idxJ]:
                        self.hopMtxRef[idxI,idxJ]=self.hopMtxRef[idxI,idxK]+self.hopMtxRef[idxK,idxJ]
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
    def stepEstimatePosition(self):
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
    def stepSelect3Achor(self):
        for idx in range(self.AchorCount,self.NodeCount):
            groupIdx=0

            for idxI in np.arange(0,self.AchorCount-2):
                for idxJ in np.arange(idxI+1,self.AchorCount-1):
                    for idxK in np.arange(idxJ+1,self.AchorCount):

                        self.GAMtx[0,0]=self.NodeCoordinate[0,idxI]-self.NodeCoordinate[0,idxK]
                        self.GAMtx[0,1]=self.NodeCoordinate[1,idxI]-self.NodeCoordinate[1,idxK]
                        self.GAMtx[1,0]=self.NodeCoordinate[0,idxJ]-self.NodeCoordinate[0,idxK]
                        self.GAMtx[1,1]=self.NodeCoordinate[1,idxJ]-self.NodeCoordinate[1,idxK]
                        self.GAMtx=-2*self.GAMtx
                        self.GBMtx[0]=math.pow(self.distMtx[idx,idxI],2)-math.pow(self.distMtx[idx,idxK],2)-math.pow(self.NodeCoordinate[0,idxI],2)-math.pow(self.NodeCoordinate[1,idxI],2)+math.pow(self.NodeCoordinate[0,idxK],2)+math.pow(self.NodeCoordinate[1,idxK],2)
                        self.GBMtx[1]=math.pow(self.distMtx[idx,idxJ],2)-math.pow(self.distMtx[idx,idxK],2)-math.pow(self.NodeCoordinate[0,idxJ],2)-math.pow(self.NodeCoordinate[1,idxJ],2)+math.pow(self.NodeCoordinate[0,idxK],2)+math.pow(self.NodeCoordinate[1,idxK],2)
                        tmp=np.dot(np.linalg.inv(self.GAMtx),self.GBMtx)
                        self.GroupXYHD[0,groupIdx]=tmp[0]
                        self.GroupXYHD[1,groupIdx]=tmp[1]
                        groupIdx+=1
            tmpIdx=-1
            tmpMin=1000
            for idxG in range(self.GroupCount):
                tmpDff=0
                for idxN in range(self.AchorCount):
                    tmpDff+=(math.fabs(self.hopMtx[idx,idxN]-math.sqrt(math.pow(self.GroupXYHD[0,idxG]-self.NodeCoordinate[0,idxN],2)+math.pow(self.GroupXYHD[1,idxG]-self.NodeCoordinate[1,idxN],2))/self.AHS[idxN]))
                if tmpMin>tmpDff:
                    tmpIdx=idxG
                    tmpMin=tmpDff
            self.BestPointXY[0,idx-self.AchorCount]=self.GroupXYHD[0,tmpIdx]
            self.BestPointXY[1,idx-self.AchorCount]=self.GroupXYHD[1,tmpIdx]
        avgErr=0
        for idx in range(self.AchorCount,self.NodeCount):
            avgErr+=(math.sqrt(math.pow(self.BestPointXY[0,idx-self.AchorCount]-self.NodeCoordinate[0,idx],2)+math.pow(self.BestPointXY[1,idx-self.AchorCount]-self.NodeCoordinate[1,idx],2))/self.R)
        avgErr=avgErr/self.UnknownCount
        return avgErr


    def stepFilter(self):
        self.Est2AchorDistMtx=np.zeros((self.UnknownCount,self.AchorCount))
        self.EnableEstimate=np.zeros(self.UnknownCount)
        for idx in range(self.UnknownCount):
            for inner in range(self.AchorCount):
                self.Est2AchorDistMtx[idx,inner]=math.sqrt(math.pow(self.EstimateXYMtx[0,idx]-self.NodeCoordinate[0,inner],2)+math.pow(self.EstimateXYMtx[1,idx]-self.NodeCoordinate[1,inner],2))
        for idx in range(self.UnknownCount):
            sumDist=0
            for inner in range(self.AchorCount):
                sumDist=sumDist+math.fabs(self.Est2AchorDistMtx[idx,inner]-self.Un2AchorDistMtx[idx,inner])
            if sumDist/self.AchorCount>self.R*0.3:
                self.EnableEstimate[idx]=0
            else:
                self.EnableEstimate[idx]=1
            print '*'*20
            print sumDist/self.AchorCount
##        plt.figure(3)
##        for idx in range(self.UnknownCount):
##            if self.EnableEstimate[idx]==1:
##                plt.plot([self.EstimateXYMtx[0,idx],self.NodeCoordinate[0,idx+self.AchorCount]],[self.EstimateXYMtx[1,idx],self.NodeCoordinate[1,idx+self.AchorCount]],'b-')
##        point1,=plt.plot(self.NodeCoordinate[0,0:self.AchorCount],self.NodeCoordinate[1,0:self.AchorCount],'r^')
##        point2,=plt.plot(self.NodeCoordinate[0,self.AchorCount:self.NodeCount],self.NodeCoordinate[1,self.AchorCount:self.NodeCount],'rs')
##        point3,=plt.plot(self.EstimateXYMtx[0,self.EnableEstimate==True],self.EstimateXYMtx[1,self.EnableEstimate==True],'bs')
##        plt.legend([point1,point2,point3],['Achor Node','Unknown Node','Estimated Position'])
##        plt.title('Traditional DV-HOP:Node Distribution & Estimation Position')
##        plt.xlim(0,125)
##        plt.ylim(0,125)
##        print self.EnableEstimate
##        plt.show()
        self.CordDiff=np.zeros(self.UnknownCount)
        avgErr=0
        for idx in range(self.UnknownCount):
            avgErr=avgErr+(math.sqrt(math.pow(self.EstimateXYMtx[0,idx]-self.NodeCoordinate[0,idx+self.AchorCount],2)+math.pow(self.EstimateXYMtx[1,idx]-self.NodeCoordinate[1,idx+self.AchorCount],2))/self.R)
        avgErr=avgErr/self.UnknownCount
##        print 'avgErr',avgErr
        return avgErr
    def showNode(self):
        plt.figure(2)
        plt.plot(self.NodeCoordinate[0,:],self.NodeCoordinate[1,:],'ro')
        for idx in range(self.NodeCount):
            for inner in range(self.NodeCount):
                if self.hopMtx[idx,inner]==1:
                    plt.plot([self.NodeCoordinate[0,idx],self.NodeCoordinate[0,inner]],[self.NodeCoordinate[1,idx],self.NodeCoordinate[1,inner]],'b--')
        plt.title('Uniform-Random Deployment:Node Distribution')

##        plt.plot(self.EstimateXYMtx[0,:],self.EstimateXYMtx[1,:],'g*')
        plt.show()
    def test(self):
        print self.NodeCoordinate
def tstfun():
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    repeatCount=10
    avgDistErr=np.zeros(10)
    dvh=DVHop()

    for outer in np.arange(0.05,0.25,0.05):
        dvh.setRatio(outer)
        dvh.stepBroadcast()
        for idx in range(repeatCount):
            dvh.deployNode()
##            dvh.test()
##            dvh.stepBroadcast()
            dvh.stepCaculateAHS()
##            dvh.stepEstimatePosition()
            #avgDistErr[int(outer*20)-1]=avgDistErr[int(outer*20)-1]+dvh.stepEstimatePosition()
            avgDistErr[int(outer*20)-1]=avgDistErr[int(outer*20)-1]+dvh.stepSelect3Achor()
            print 'repeat',outer,' ',idx
        avgDistErr[int(outer*20)-1]=avgDistErr[int(outer*20)-1]/repeatCount
    print '$'*40
    print avgDistErr
    arrX=np.arange(0.05,0.55,0.05)
    plt.figure(1)
    plt.plot(arrX,avgDistErr)
    plt.xlabel('Achor Ratio')
    plt.ylabel('Localization Error')
    plt.title('Uniform-Random Deployment:Achor Ratio vs Localization Error')
    plt.show()
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    dvh.showNode()


    #dvh.showNode()

def main():
    pass
    tstfun()



if __name__ == '__main__':
    main()
