# セグメントの隣接ゴマの特徴調査
# コマ範囲に対する体描写範囲、コマ範囲に対する顔描写範囲、コマ範囲に対するセリフ描写範囲、セリフテキスト
# {title:[(FrontFramInstance, BackFrameInstance), (FrontFramInstance, BackFrameInstance), ...], ...}


import json

from main import *
from range import get_ObjectRange

class SideFrame(Core):
    
    def __init__(self, Index, xMin, yMin, xMax, yMax, PageIndex, BandIndex, FrameIndex, BodyRate, FaceRate, LineRate, Text):
        
        super().__init__(Index, xMin, yMin, xMax, yMax)
        self.PageIndex = PageIndex
        self.BandIndex = BandIndex
        self.FrameIndex = FrameIndex
        self.BodyRate = BodyRate
        self.FaceRate = FaceRate
        self.LineRate = LineRate
        self.Text = Text
        
    
    def get_PageIndex(self):
        
        return self.PageIndex
    
    def get_BandIndex(self):
        
        return self.BandIndex
    
    def get_FrameIndex(self):
        
        return self.FrameIndex

    def get_BodyRate(self):
        
        return self.BodyRate
    
    def get_FaceRate(self):
        
        return self.FaceRate
    
    def get_LineRate(self):
        
        return self.LineRate
    
    def get_Text(self):
        
        return self.Text
    
    
def get_FrameFeature(xFrame, xCharacterIndexs):
    
    xFrameUniqueIndex = xFrame.get_Index()
    sumBodyRate = 0
    sumFaceRate = 0
    sumLineRate = 0
    Texts = []
    
    xFrameRange = get_ObjectRange(xFrame)
    
    xBodys = xFrame.get_Bodys()
    
    if xBodys != []:
        
        for xBody in xBodys:
            
            xCharacterIndex = xBody.get_CharacterIndex()
            
            if xCharacterIndex in xCharacterIndexs: # モブは弾く
                
                xBodyRange = get_ObjectRange(xBody)
                xBodyRate = xBodyRange / xFrameRange
                sumBodyRate += xBodyRate
                
                xFaces = xBody.get_Faces()
                    
                if xFaces != []:
                    
                    for xFace in xFaces:
                        
                        xFaceRange = get_ObjectRange(xFace)
                        xFaceRate = xFaceRange / xFrameRange
                        sumFaceRate += xFaceRate
                    
    xLines = xFrame.get_Lines()
    
    if xLines != []:
        
        for xLine in xLines:
            
            xLineRange = get_ObjectRange(xLine)
            xLineRate = xLineRange / xFrameRange
            sumLineRate += xLineRate
            
            xText = xLine.get_Text()
            Texts.append(xText)
    
    return xFrameUniqueIndex, sumBodyRate, sumFaceRate, sumLineRate, Texts


def get_SideFrame(xComicInstance, SegmentJson):    
    
    SideFrameInstances = []
    
    xFile = xComicInstance.get_File()
    EpisodeIndex_Segments = SegmentJson[xFile]
    
    xCharacterIndex_CharancterName = xComicInstance.get_CharacterIndex_CharacterName()
    xCharacterIndexs = list(xCharacterIndex_CharancterName.keys())
    
    xEpisodes = xComicInstance.get_Episodes()
    
    for xEpisode in xEpisodes:
        
        xEpisodeIndex = xEpisode.get_Index()
        xSegments = EpisodeIndex_Segments[xEpisodeIndex]
        
        ChangePageIndex = 0
        ChangeSegmentIndex = 0
        aSegment = xSegments[ChangeSegmentIndex]
        bPageIndex = aSegment[0]
        bBandIndex = aSegment[1]
        bFrameIndex = aSegment[2]
        
        xPages = xEpisode.get_Pages()
        
        while True:
            
            xPage = xPages[ChangePageIndex]
            xPageIndex = xPage.get_Index()
            
            if xPageIndex == bPageIndex:
                
                bBands = xPage.get_Frames()
                bFrames = bBands[int(bBandIndex) - 1]
                bFrame = bFrames[int(bFrameIndex) - 1]
                
                if bFrameIndex == "1":
                                
                    if bBandIndex == "1":
                        
                        BackPageCount = 1
                        
                        while True:
                            
                            fPage = xPages[xPages.index(xPage) - BackPageCount]
                            fPageIndex = str(int(bPageIndex) - BackPageCount)
                        
                            fBands = fPage.get_Frames()
                        
                            if len(fBands) == 0:
                                
                                BackPageCount += 1
                                
                                continue
                            
                            else:
                                
                                break
                        
                        fBandIndex = str(len(fBands))
                        
                    else:
                        
                        fPageIndex = bPageIndex
                        
                        fBands = bBands
                        fBandIndex = str(int(bBandIndex) - 1)

                    # print(len(fBands), fBandIndex)
                    fFrames = fBands[int(fBandIndex) - 1]
                    fFrameIndex = str(len(fFrames))
                    
                else:
                    
                    fPageIndex = bPageIndex
                    fBandIndex = bBandIndex
                    
                    fFrames = bFrames
                    fFrameIndex = str(int(bFrameIndex) - 1)
                
                fFrame = fFrames[int(fFrameIndex) - 1]
            
                fFramexMin = fFrame.get_xMin()
                fFrameyMin = fFrame.get_yMin()
                fFramexMax = fFrame.get_xMax()
                fFrameyMax = fFrame.get_yMax()
                fFrameUniqueIndex, fBodyRate, fFaceRate, fLineRate, fText = get_FrameFeature(fFrame, xCharacterIndexs)
                fFrameInstance = SideFrame(fFrameUniqueIndex, fFramexMin, fFrameyMin, fFramexMax, fFrameyMax, fPageIndex, fBandIndex, fFrameIndex, fBodyRate, fFaceRate, fLineRate, fText)
                
                bFramexMin = bFrame.get_xMin()
                bFrameyMin = bFrame.get_yMin()
                bFramexMax = bFrame.get_xMax()
                bFrameyMax = bFrame.get_yMax()
                bFrameUniqueIndex, bBodyRate, bFaceRate, bLineRate, bText = get_FrameFeature(bFrame, xCharacterIndexs)
                bFrameInstance = SideFrame(bFrameUniqueIndex, bFramexMin, bFrameyMin, bFramexMax, bFrameyMax, bPageIndex, bBandIndex, bFrameIndex, bBodyRate, bFaceRate, bLineRate, bText)

                SideFrameInstances.append((fFrameInstance, bFrameInstance))
                
                ChangeSegmentIndex += 1
                
                if ChangeSegmentIndex == len(xSegments):
                    
                    break
                
                else:
                    
                    aSegment = xSegments[ChangeSegmentIndex]
                    bPageIndex = aSegment[0]
                    bBandIndex = aSegment[1]
                    bFrameIndex = aSegment[2]
    
            else:
                
                ChangePageIndex += 1
    
    
    return SideFrameInstances


                
                           
                                    
                            
    
    

if __name__ == "__main__":
    
    with open("./datas/others/segment.json", "r") as file:
        
        SegmentJson = json.load(file)
    
    dirpath = "./datas/edited_tests/annotations"
    files = glob.glob(os.path.join(dirpath, "*.xml"))
    
    Comics = get_comics(files)
    
    for xComic in Comics:
        
        SideFrameInstances = get_SideFrame(xComic, SegmentJson)
        
        for xSideFrames in SideFrameInstances:
            
            fFrameIndex = xSideFrames[0].get_Index()
            bFrameIndex = xSideFrames[1].get_Index()
            #print(fFrameIndex,bFrameIndex)
        
        