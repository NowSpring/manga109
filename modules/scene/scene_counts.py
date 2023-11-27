# シーンとして成り立つページ数、帯数、コマ数の調査

import os
import glob
import json
import xml.etree.ElementTree as et


def get_SceneCounts(xPath):
    
    xFile = os.path.split(xPath)[1]
    xFile = os.path.splitext(xFile)[0]
    tree = et.ElementTree(file = xPath)
    root = tree.getroot()
    
    with open("./datas/others/segment.json", "r") as file:
        SegmentJson = json.load(file)
        
    EpisodeIndex_arraySegments = SegmentJson[xFile]
    
    EpisodeIndex_arraySceneCounts = {}
    
    for child in root:
            
        if child.tag == "pages":

            for grandchild in child:
                
                if grandchild.tag == "episode":
                    
                    PageCount = 0
                    BandCount = 0
                    FrameCount = 0
                    arraySceneCounts = []

                    ChangeIndex = 0
                    EpisodeIndex = grandchild.attrib["index"]
                    arraySeguments = EpisodeIndex_arraySegments[EpisodeIndex]
                    
                    for Page in grandchild:
                        
                        PageIndex = Page.attrib["index"]
                        BandIndex = 0
                        
                        for Band in Page:
                            
                            BandIndex += 1
                            FrameIndex = 0
                            
                            for Frame in Band:
                                
                                FrameIndex += 1
                                
                                if ChangeIndex != len(arraySeguments):
                                
                                    if [str(PageIndex), str(BandIndex), str(FrameIndex)] == arraySeguments[ChangeIndex]:
                                        
                                        if PageCount == -1:
                                            
                                            if BandCount == -1:
                                            
                                                arraySceneCounts.append(["0", "0", str(FrameCount)])
                                        
                                            else:
                                            
                                                arraySceneCounts.append(["0", str(BandCount), str(FrameCount)])
                                            
                                        else:
                                            
                                            arraySceneCounts.append([str(PageCount), str(BandCount), str(FrameCount)])
                                            
                                        if str(FrameIndex) == "1":
                                            
                                            BandCount = 0
                                            
                                            if str(BandIndex) == "1":
                                            
                                                PageCount = 0
                                                
                                            else:
                                                                                            
                                                PageCount = -1
                                        
                                        else:
                                            
                                            BandCount = -1
                                            PageCount = -1
                                        
                                        FrameCount = 0
                                        
                                        ChangeIndex += 1
                                        
                                FrameCount += 1
                                
                            BandCount += 1
                            
                        PageCount += 1
                        
                    arraySceneCounts.append([str(PageCount), str(BandCount), str(FrameCount)])
                    EpisodeIndex_arraySceneCounts[EpisodeIndex] = arraySceneCounts
    
    # 出力：{episode_id : [[ページ数、帯数、コマ数]] }
    return EpisodeIndex_arraySceneCounts
    

if __name__ == "__main__":
    
    dirpath = "./datas/tests/annotations"
    Paths = glob.glob(os.path.join(dirpath, "*.xml"))
    
    
    for xPath in Paths:
        EpisodeIndex_arraySceneCounts = get_SceneCounts(xPath)
        print(EpisodeIndex_arraySceneCounts)
        
        