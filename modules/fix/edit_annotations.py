import json
from modules.fix.sub import *


def shift_xCoord(xObject, xShift):
    
    xMin = xObject.get_xMin()
    xMax = xObject.get_xMax()
    xMiddle = xObject.get_xMiddle()
    
    xObject.set_xMin(str(int(xMin) - xShift))
    xObject.set_xMax(str(int(xMax) - xShift))
    xObject.set_xMiddle(str(int(xMiddle) - xShift))
    
    

def edit_xml(xComicInstance):
    
    def indent(elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    xFile = xComicInstance.get_File()
    xTitle = xComicInstance.get_Title()
    xAuthor = xComicInstance.get_Author()
    xEra = xComicInstance.get_Era()
    xPublisher = xComicInstance.get_Publisher()
    xTarget = xComicInstance.get_Target()
    xGenre = xComicInstance.get_Genre()
        
    book = et.Element('book',  {'title':xTitle, "author":xAuthor, "era":xEra, "publisher":xPublisher, "target":xTarget, "genre":xGenre})
    
    xCharacterIndex_CharacterName = xComicInstance.get_CharacterIndex_CharacterName()
    characters = et.SubElement(book, 'characters')
    
    for yCharacterIndex in xCharacterIndex_CharacterName:
    
        character = et.SubElement(characters, 'character', {"index":yCharacterIndex, "name":xCharacterIndex_CharacterName[yCharacterIndex]})

    xPage = xComicInstance.get_Pages()
    pages = et.SubElement(book, 'pages')
    
    with open("./datas/others/episode.json", "r") as file:
        
        EpisodeJson = json.load(file)
        
    EpisodeFrag = False
    EpisodeIndex_PageIndexs = EpisodeJson[xFile]
    EpisodeIndex = list(EpisodeIndex_PageIndexs.keys())[0]
    EpisodeFirstPageIndex = EpisodeIndex_PageIndexs[EpisodeIndex][0]
    EpisodeLastPageIndex = EpisodeIndex_PageIndexs[EpisodeIndex][1]
    
    for yPage in xPage:
        
        yPageIndex = str(yPage.get_Index())
        yPagexMin = str(yPage.get_xMin())
        yPageyMin = str(yPage.get_yMin())
        yPagexMax = str(yPage.get_xMax())
        yPageyMax = str(yPage.get_yMax())
        
        if EpisodeFrag == False:
            
            if yPageIndex != EpisodeFirstPageIndex:
        
                page = et.SubElement(pages, 'page', {"index":yPageIndex, "xmin":yPagexMin, "ymin":yPageyMin, "xmax":yPagexMax, "ymax":yPageyMax})
            
            else:
                
                EpisodeFrag = True
                episode = et.SubElement(pages, "episode", {"index" : EpisodeIndex})
                page = et.SubElement(episode, 'page', {"index":yPageIndex, "xmin":yPagexMin, "ymin":yPageyMin, "xmax":yPagexMax, "ymax":yPageyMax})
                
        else:
            
            if yPageIndex != EpisodeLastPageIndex:
                
                page = et.SubElement(episode, 'page', {"index":yPageIndex, "xmin":yPagexMin, "ymin":yPageyMin, "xmax":yPagexMax, "ymax":yPageyMax})
                
            else:
                
                EpisodeFrag = False
                page = et.SubElement(episode, 'page', {"index":yPageIndex, "xmin":yPagexMin, "ymin":yPageyMin, "xmax":yPagexMax, "ymax":yPageyMax})
                
                if str(int(EpisodeIndex) + 1) in EpisodeIndex_PageIndexs:
                        
                    EpisodeIndex = str(int(EpisodeIndex) + 1)
                    EpisodeFirstPageIndex = EpisodeIndex_PageIndexs[EpisodeIndex][0]
                    EpisodeLastPageIndex = EpisodeIndex_PageIndexs[EpisodeIndex][1]
        
        yBands = yPage.get_Frames()
        
        if yBands != []:
            
            for zBand in yBands:
                
                band = et.SubElement(page, 'band')
                
                for zFrame in zBand:
                    
                    zFrameIndex = str(zFrame.get_Index())
                    zFramexMin = str(zFrame.get_xMin())
                    zFrameyMin = str(zFrame.get_yMin())
                    zFramexMax = str(zFrame.get_xMax())
                    zFrameyMax = str(zFrame.get_yMax())
                    frame = et.SubElement(band, 'frame', {"index":zFrameIndex, "xmin":zFramexMin, "ymin":zFrameyMin, "xmax":zFramexMax, "ymax":zFrameyMax})
                    
                    zBodys = zFrame.get_Bodys()
                    
                    if zBodys != []:
                    
                        for wBody in zBodys:
                    
                            wBodyIndex = str(wBody.get_Index())
                            wBodyxMin = str(wBody.get_xMin())
                            wBodyyMin = str(wBody.get_yMin())
                            wBodyxMax = str(wBody.get_xMax())
                            wBodyyMax = str(wBody.get_yMax())
                            wBodyNI = str(wBody.get_CharacterIndex())
                            body = et.SubElement(frame, 'body', {"index":wBodyIndex, "xmin":wBodyxMin, "ymin":wBodyyMin, "xmax":wBodyxMax, "ymax":wBodyyMax, "character":wBodyNI})
                    
                            wFaces = wBody.get_Faces()
                    
                            if wFaces != []:
                    
                                for vFace in wFaces:
                    
                                    vFaceIndex = str(vFace.get_Index())
                                    vFacexMin = str(vFace.get_xMin())
                                    vFaceyMin = str(vFace.get_yMin())
                                    vFacexMax = str(vFace.get_xMax())
                                    vFaceyMax = str(vFace.get_yMax())
                                    vFaceNI = str(vFace.get_CharacterIndex())
                                    face = et.SubElement(body, 'face', {"index":vFaceIndex, "xmin":vFacexMin, "ymin":vFaceyMin, "xmax":vFacexMax, "ymax":vFaceyMax, "character":vFaceNI})
                    
                    zLines = zFrame.get_Lines()
                    
                    if zLines != []:
                    
                        for wLine in zLines:
                    
                            wLineIndex = str(wLine.get_Index())
                            wLinexMin = str(wLine.get_xMin())
                            wLineyMin = str(wLine.get_yMin())
                            wLinexMax = str(wLine.get_xMax())
                            wLineyMax = str(wLine.get_yMax())
                            wLineText = str(wLine.get_Text())
                            wLineNI = str(wLine.get_CharacterIndex())
                            line = et.SubElement(frame, 'text', {"index":wLineIndex, "xmin":wLinexMin, "ymin":wLineyMin, "xmax":wLinexMax, "ymax":wLineyMax, "character":wLineNI})
                            line.text = wLineText
                
    indent(book)
    tree = et.ElementTree(book)
    tree.write('./datas/raw/tests/annotations/' + xFile + ".xml", xml_declaration=True, encoding='utf-8')

    
    

if __name__ == "__main__":
    
    dirpath = "./datas/raw/annotations"
    files = glob.glob(os.path.join(dirpath, "*.xml"))
    
    comics = get_ComicInstances(files)
    
    # episodes = comics[0].get_Episodes()
    # pages = episodes[0].get_Pages()
    
    
    for xComic in comics:
        
        xPages = xComic.get_Pages()
        
        for aPage in xPages:
            
            aPagexMin = aPage.get_xMin()
            
            if aPagexMin != "0":
                
                shift_xCoord(aPage, int(aPagexMin))
                
                aBands = aPage.get_Frames()
                
                for aFrames in aBands:
                
                    for bFrame in aFrames:
                        
                        shift_xCoord(bFrame, int(aPagexMin))
                        
                        bBodys = bFrame.get_Bodys()
                        
                        for cBody in bBodys:
                            
                            shift_xCoord(cBody, int(aPagexMin))
                            
                            cFaces = cBody.get_Faces()
                            
                            for dFace in cFaces:
                                
                                shift_xCoord(dFace, int(aPagexMin))
                        
                        bLines = bFrame.get_Lines()
                        
                        for cLine in bLines:
                            
                            shift_xCoord(cLine, int(aPagexMin))
        
        edit_xml(xComic)
    
    