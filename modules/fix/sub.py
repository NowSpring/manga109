import os
import glob
import pandas as pd
from operator import attrgetter
import xml.etree.ElementTree as et

from classes import * ##


def get_IndexAndCoord(great_grandchild):
    
    Index = great_grandchild.attrib["id"]
    xMin = int(great_grandchild.attrib["xmin"])
    yMin = int(great_grandchild.attrib["ymin"])
    xMax = int(great_grandchild.attrib["xmax"])
    yMax = int(great_grandchild.attrib["ymax"])
    
    return Index, xMin, yMin, xMax, yMax


def get_aMiddle(aMin, aMax):
    
    return aMin + ((aMax - aMin) / 2)


def judge_Storage(aStorages, oObject):
    
    def rectangles_overlap_area(rect1, rect2):
    
        x1_min, y1_min, x1_max, y1_max = rect1
        x2_min, y2_min, x2_max, y2_max = rect2
        overlap_width = min(x1_max, x2_max) - max(x1_min, x2_min)
        overlap_height = min(y1_max, y2_max) - max(y1_min, y2_min)

        if overlap_width < 0 or overlap_height < 0:
            # 矩形が重なっていない場合、面積は0
            return 0

        overlap_area = overlap_width * overlap_height
        
        return overlap_area

    max_overlap_area = 0
    max_overlap_rectangle = None
    
    oObjectCoord = (oObject.get_xMin(), oObject.get_yMin(), oObject.get_xMax(), oObject.get_yMax())
    
    for oStorage in aStorages:
        
        oStorageCoord = (oStorage.get_xMin(), oStorage.get_yMin(), oStorage.get_xMax(), oStorage.get_yMax())
        overlap_area = rectangles_overlap_area(oObjectCoord, oStorageCoord)
        
        if overlap_area > max_overlap_area:
        
            max_overlap_area = overlap_area
            max_overlap_rectangle = oStorage

    return max_overlap_rectangle


def sort_Frames(bFrames):
    
    def get_RowBands(dFrames, CoreFrame):
        
        iFrames = dFrames.copy()
        
        if CoreFrame == None:
        
            RowBands = []
            CoreFrames = []
        
        else:
        
            RowBands = [[CoreFrame]]
            CoreFrames = [CoreFrame]  
            iFrames.remove(CoreFrame)
        
        while iFrames != []:
        
            MaxHeight = 0
            MaxHeightFrame = None
            
            for eFrame in dFrames:
        
                if eFrame in iFrames:
        
                    if eFrame.get_Height() > MaxHeight:
                    
                        MaxHeight = eFrame.get_Height()
                        MaxHeightFrame = eFrame
            
            RowBand = [MaxHeightFrame]
            
            for jFrame in iFrames:
        
                if jFrame != MaxHeightFrame:
                    
                    jFrameyMiddle = jFrame.get_yMiddle()
        
                    if MaxHeightFrame.get_yMin() < jFrameyMiddle < MaxHeightFrame.get_yMax():
                    
                        RowBand.append(jFrame)
            
            RowBand.sort(key = attrgetter('yMiddle'))
            RowBands.append(RowBand)
            CoreFrames.append(MaxHeightFrame)
            
            hFrames = list(eFrame for eFrame in iFrames if eFrame not in RowBand)
            iFrames = hFrames
        
        NewRowBands = []
        CoreFrames.sort(key = attrgetter('yMiddle'))
        
        for hFrame in CoreFrames:
        
            for xRowBand in RowBands:
        
                if hFrame in xRowBand:
                    
                    NewRowBands.append(xRowBand)
            
        return NewRowBands, CoreFrames
    
    def get_ColBands(dFrames, CoreFrame):
        
        iFrames = dFrames.copy()
        
        if CoreFrame == None:
            
            ColBands = []
            CoreFrames = []
        
        else:
        
            ColBands = [[CoreFrame]]
            CoreFrames = [CoreFrame]
            iFrames.remove(CoreFrame)
        
        while iFrames != []:
            
            MaxWidth = 0
            MaxWidthFrame = None
            
            for eFrame in dFrames:
                
                if eFrame in iFrames:
                
                    if eFrame.get_Width() > MaxWidth:
                        
                        MaxWidth = eFrame.get_Width()
                        MaxWidthFrame = eFrame
            
            ColBand = [MaxWidthFrame]
            
            for jFrame in iFrames:
                
                if jFrame != MaxWidthFrame:
                    
                    jFramexMiddle = jFrame.get_xMiddle()
                
                    if MaxWidthFrame.get_xMin() < jFramexMiddle < MaxWidthFrame.get_xMax():
                        
                        ColBand.append(jFrame)
            
            ColBand.sort(key = attrgetter('xMiddle'), reverse = True)
            ColBands.append(ColBand)
            CoreFrames.append(MaxWidthFrame)
            
            hFrames = list(eFrame for eFrame in iFrames if eFrame not in ColBand)
            iFrames = hFrames
        
        NewColBands = []
        CoreFrames.sort(key = attrgetter('xMiddle'), reverse = True)
        
        for hFrame in CoreFrames:
            
            for xColBand in ColBands:
            
                if hFrame in xColBand:
                    
                    NewColBands.append(xColBand)    
            
        return NewColBands, CoreFrames
    
    def judge_Flag(xNum):
        
        if xNum % 2 == 1:  # 奇数の場合
        
            xFlag = True
        
        else:  # 偶数の場合
        
            xFlag = False
        
        return xFlag
    
    def get_NewBands(xNum, xBandFrames, xCoreFrame):
        
        xFlag = judge_Flag(xNum)
        
        if xFlag == True:
            
            NewBands, NewCoreFrames = get_RowBands(xBandFrames, xCoreFrame)
            
        elif xFlag == False:
            
            NewBands, NewCoreFrames = get_ColBands(xBandFrames, xCoreFrame)
            
        return NewBands, NewCoreFrames
    
    def get_AlignedBands(NewBands, FixIndex, ChangeIndex, FlagNum, xBands, xCoreFrames):
        
        FlagNum += 1
        
        if len(xBands[ChangeIndex]) > 1:
            
            SubBands, SubCoreFrames = get_NewBands(FlagNum, xBands[ChangeIndex], xCoreFrames[ChangeIndex])
            
            for j in range(len(SubBands)):
                
                get_AlignedBands(NewBands, FixIndex, j, FlagNum, SubBands, SubCoreFrames)
            
            FlagNum -= 1
            
        else:
            
            NewBands[FixIndex].append(xBands[ChangeIndex][0])
            FlagNum -= 1
    
    FlagNum = 1
    FirstBands, FirstCoreFrames = get_RowBands(bFrames, None)

    if (len(FirstBands) == 1) and (len(FirstCoreFrames) == 1):
        
        FlagNum = 2
        FirstBands, FirstCoreFrames = get_ColBands(bFrames, None)
            
    NewBands = [[] for _ in range(len(FirstBands))]
            
    for i in range(len(FirstBands)):
       
       get_AlignedBands(NewBands, i, i, FlagNum, FirstBands, FirstCoreFrames)
    
    return NewBands, FirstCoreFrames


def sort_Lines(xLines):
    
    pass

def get_ComicInstances(PATHS): # PAHTS : 'Annotations/*.xml'
    
    ComicInstances = [] 
    
    for xPath in PATHS:
        
        xFile = os.path.split(xPath)[1]
        xFile = os.path.splitext(xFile)[0]
        tree = et.ElementTree(file = xPath)
        root = tree.getroot()
        xTitle = root.attrib["title"]
        xAuthor = root.attrib["author"]
        xEra = root.attrib["era"]
        xPublisher = root.attrib["publisher"]
        xTarget = root.attrib["target"]
        xGenre = root.attrib["genre"]
        
        xDF = pd.read_csv("./datas/others/annotation.csv")
        xDFrows = xDF[xDF['title'] == xFile]
        
        for child in root:

            if child.tag == "characters":
                
                xCharacterIndex_CharacterName = {}
                
                for grandchild in child:
                
                    yCharacterIndex = grandchild.attrib["id"]
                    yCharacterName =  grandchild.attrib["name"]
                    xCharacterIndex_CharacterName[yCharacterIndex] = yCharacterName
            
            if child.tag == "pages":
                
                xPages = []
                PageIndex = 0
                
                for grandchild in child:
                
                    aPageWidth = int(grandchild.attrib["width"])
                    aPageHeight = int(grandchild.attrib["height"])
                    aPagexMiddle = int(aPageWidth / 2)
                    
                    aFrames = []
                    aFaces = []
                    aBodys = []
                    aLines = []
                    
                    # ページ内のFrameInstance, FaceInstance, LineInstanceを全て、読み順関係なく抽出
                    for great_grandchild in grandchild:
                        
                        if great_grandchild.tag == "frame":
                
                            oFrameIndex, oFramexMin, oFrameyMin, oFramexMax, oFrameyMax = get_IndexAndCoord(great_grandchild)
                            
                            if (oFramexMin < aPagexMiddle) and (aPagexMiddle < oFramexMax):
                
                                aFrames.append(Frame(oFrameIndex, oFramexMin, oFrameyMin, aPagexMiddle, oFrameyMax, int(get_aMiddle(oFramexMin, aPagexMiddle)), int(get_aMiddle(oFrameyMin, oFrameyMax)), [], []))
                                aFrames.append(Frame(oFrameIndex, aPagexMiddle, oFrameyMin, oFramexMax, oFrameyMax, int(get_aMiddle(aPagexMiddle, oFramexMax)), int(get_aMiddle(oFrameyMin, oFrameyMax)), [], []))
                            
                            else:
                
                                aFrames.append(Frame(oFrameIndex, oFramexMin, oFrameyMin, oFramexMax, oFrameyMax, int(get_aMiddle(oFramexMin, oFramexMax)), int(get_aMiddle(oFrameyMin, oFrameyMax)), [], []))
                        
                        elif (great_grandchild.tag == "face") or (great_grandchild.tag == "body"):
                
                            oFBIndex, oFBxMin, oFByMin, oFBxMax, oFByMax = get_IndexAndCoord(great_grandchild)
                            
                            if oFBxMin < aPagexMiddle < oFBxMax:
                                
                                if great_grandchild.tag == "face":
                
                                    aFaces.append(Face(oFBIndex, oFBxMin, oFByMin, aPagexMiddle, oFByMax, int(get_aMiddle(oFBxMin, aPagexMiddle)), int(get_aMiddle(oFByMin, oFByMax)), great_grandchild.attrib["character"]))
                                    aFaces.append(Face(oFBIndex, aPagexMiddle, oFByMin, oFBxMax, oFByMax, int(get_aMiddle(aPagexMiddle, oFBxMax)), int(get_aMiddle(oFByMin, oFByMax)), great_grandchild.attrib["character"]))
                                
                                elif great_grandchild.tag == "body":
                
                                    aBodys.append(Body(oFBIndex, oFBxMin, oFByMin, aPagexMiddle, oFByMax, int(oFBxMin + ((aPagexMiddle - oFBxMin) / 2)), int(oFByMin + ((oFByMax - oFByMin) / 2)), great_grandchild.attrib["character"], []))
                                    aBodys.append(Body(oFBIndex, aPagexMiddle, oFByMin, oFBxMax, oFByMax, int(aPagexMiddle + ((oFBxMax - aPagexMiddle) / 2)), int(oFByMin + ((oFByMax - oFByMin) / 2)), great_grandchild.attrib["character"], []))
                            
                            else:
                                
                                if great_grandchild.tag == "face":
                
                                    aFaces.append(Face(oFBIndex, oFBxMin, oFByMin, oFBxMax, oFByMax, int(oFBxMin + ((oFBxMax - oFBxMin) / 2)), int(oFByMin + ((oFByMax - oFByMin) / 2)), great_grandchild.attrib["character"]))
                                
                                elif great_grandchild.tag == "body":
                
                                    aBodys.append(Body(oFBIndex, oFBxMin, oFByMin, oFBxMax, oFByMax, int(oFBxMin + ((oFBxMax - oFBxMin) / 2)), int(oFByMin + ((oFByMax - oFByMin) / 2)), great_grandchild.attrib["character"], []))
                                
                        elif great_grandchild.tag == "text":
                
                            oTextIndex, oTextxMin, oTextyMin, oTextxMax, oTextyMax = get_IndexAndCoord(great_grandchild)
                            oCharacterId = xDFrows[xDFrows['text_id'] == oTextIndex]['character_id'].values[0]
                            
                            if oTextxMin < aPagexMiddle < oTextxMax:
                            
                                if (aPagexMiddle - oTextxMin) > (oTextxMax - aPagexMiddle):
                
                                    aLines.append(Line(oTextIndex, oTextxMin, oTextyMin, aPagexMiddle, oTextyMax, int(oTextxMin + ((aPagexMiddle - oTextxMin) / 2)), int(oTextyMin + ((oTextyMax - oTextyMin) / 2)), oCharacterId, great_grandchild.text, None, None))
                                    aLines.append(Line(oTextIndex, aPagexMiddle, oTextyMin, oTextxMax, oTextyMax, int(aPagexMiddle + ((oTextxMax - aPagexMiddle) / 2)), int(oTextyMin + ((oTextyMax - oTextyMin) / 2)), oCharacterId, None, None, None))
                            
                                else:
                
                                    aLines.append(Line(oTextIndex, oTextxMin, oTextyMin, aPagexMiddle, oTextyMax, int(oTextxMin + ((aPagexMiddle - oTextxMin) / 2)), int(oTextyMin + ((oTextyMax - oTextyMin) / 2)), oCharacterId, None, None, None))
                                    aLines.append(Line(oTextIndex, aPagexMiddle, oTextyMin, oTextxMax, oTextyMax, int(aPagexMiddle + ((oTextxMax - aPagexMiddle) / 2)), int(oTextyMin + ((oTextyMax - oTextyMin) / 2)), oCharacterId, great_grandchild.text, None, None))         
                            
                            else:
                
                                aLines.append(Line(oTextIndex, oTextxMin, oTextyMin, oTextxMax, oTextyMax, int(oTextxMin + ((oTextxMax - oTextxMin) / 2)), int(oTextyMin + ((oTextyMax - oTextyMin) / 2)), oCharacterId, great_grandchild.text, None, None))                    
                                
                    # BodyInstanceにFaceInstanceを格納
                    # FrameInstanceにBodyInstanceとLineInstanceを格納
                    for oFace in aFaces:
                        
                        sBody = judge_Storage(aBodys, oFace)
                        
                        if sBody != None:
                        
                            soFaces = sBody.get_Faces()
                            soFaces.append(oFace)
                            sBody.set_Faces(soFaces)
                    
                    for oBody in aBodys:
                        
                        sFrame = judge_Storage(aFrames, oBody)
                        
                        if sFrame != None:
                            
                            soBodys = sFrame.get_Bodys()
                            soBodys.append(oBody)
                            sFrame.set_Bodys(soBodys)
                        
                    for oLine in aLines:
                        
                        sFrame = judge_Storage(aFrames, oLine)
                        
                        if sFrame != None:
                        
                            soLines = sFrame.get_Lines()
                            soLines.append(oLine)
                            soLines.sort(key = attrgetter('xMin'), reverse = True)
                            sFrame.set_Lines(soLines)
                    
                    bFrames = []
                    cFrames = []
                    
                    for oFrame in aFrames:
                        
                        if aPagexMiddle < oFrame.get_xMiddle() <= aPageWidth:
                            
                            bFrames.append(oFrame)
                            
                        elif 0 <= oFrame.get_xMiddle() <= aPagexMiddle:
                            
                            cFrames.append(oFrame)  
                            
                    bFrames, bCoreFrames = sort_Frames(bFrames)
                    cFrames, cCoreFrames = sort_Frames(cFrames)
                    
                    xPages.append(Page(PageIndex, aPagexMiddle, 0, aPageWidth, aPageHeight, int((aPageWidth - aPagexMiddle) / 2), int(aPageHeight / 2), bFrames))
                    xPages.append(Page(PageIndex + 1, 0, 0, aPagexMiddle, aPageHeight, int(aPagexMiddle / 2), int(aPageHeight / 2), cFrames))          
                    
                    PageIndex += 2
        
        ComicInstances.append(Comic(xFile, xTitle, xAuthor, xEra, xPublisher, xTarget, xGenre, xCharacterIndex_CharacterName, [], xPages))
    
    return ComicInstances



        
        
        


if __name__ == "__main__":
    
    dirpath = "./datas/tests/raw/annotations"
    files = glob.glob(os.path.join(dirpath, "*.xml"))
    
    comics = get_ComicInstances(files)
    
    # episodes = comics[0].get_Episodes()
    # pages = episodes[0].get_Pages()
    
    pages = comics[0].get_Pages()
    id_name = comics[0].get_CharacterIndex_CharacterName()
    
    
    # for page in pages:
        
        # print(page.get_xMin(), type(page.get_xMin()))
        
        # bands = page.get_Frames()
        
        # for frames in bands:
            
        #     for frame in frames:
                
        #         lines = frame.get_Lines()
                
        #         for line in lines:
                    
        #             text = line.get_Text()
        #             id = line.get_CharacterIndex()
                    
        #             if id in id_name:

        #                 name = id_name[id]
                    
        #             else:
                        
        #                 name = "モブ"
                    
        #             print(text, ":", name)
                    
        #     print()
            
        # print("---------------------")
    
            
    

    