# 編集済みxmlファイル対応

import os
import glob
import xml.etree.ElementTree as et

from classes import * ##



def get_comics(files):

    def get_IndexAndCoord(great_grandchild):
        
        Index = great_grandchild.attrib["index"]
        xMin = int(great_grandchild.attrib["xmin"])
        yMin = int(great_grandchild.attrib["ymin"])
        xMax = int(great_grandchild.attrib["xmax"])
        yMax = int(great_grandchild.attrib["ymax"])
        
        return Index, xMin, yMin, xMax, yMax

    comics = []

    for xpath in files:
        
        file = os.path.split(xpath)[1]
        file = os.path.splitext(file)[0]
        tree = et.ElementTree(file = xpath)
        root = tree.getroot()
        title = root.attrib["title"]
        author = root.attrib["author"]
        era = root.attrib["era"]
        publisher = root.attrib["publisher"]
        target = root.attrib["target"]
        genre = root.attrib["genre"]
        
        for child in root:

                if child.tag == "characters":
                    
                    id_name = {}
                    
                    for grandchild in child:
                        
                        character_id = grandchild.attrib["index"]
                        character_name =  grandchild.attrib["name"]
                        id_name[character_id] = character_name
                        
                if child.tag == "pages":
                    
                    episodes = []
                    
                    for grandchild in child:
                        
                        if grandchild.tag == "episode":
                            
                            episode_id = grandchild.attrib["index"]
                            
                            pages = []
                            
                            for page in grandchild:
                                
                                page_id, page_xmin, page_ymin, page_xmax, page_ymax = get_IndexAndCoord(page)
                                page_xmiddle = (page_xmin + page_xmax) / 2
                                page_ymiddle = (page_ymin + page_ymax) / 2
                                
                                arrayframes = []
                                
                                for band in page:
                                    
                                    frames = []
                                    
                                    for frame in band:
                                        
                                        frame_id, frame_xmin, frame_ymin, frame_xmax, frame_ymax = get_IndexAndCoord(frame)
                                        frame_xmiddle = (frame_xmin + frame_xmax) / 2
                                        frame_ymiddle = (frame_ymin + frame_ymax) / 2
                                        
                                        bodys = []
                                        lines = []
                                        
                                        for object in frame:
                                            
                                            if object.tag == "body":
                                                
                                                body_id, body_xmin, body_ymin, body_xmax, body_ymax = get_IndexAndCoord(object)
                                                body_xmiddle = (body_xmin + body_xmax) / 2
                                                body_ymiddle = (body_ymin + body_ymax) / 2
                                                body_character_id = object.attrib["character"]
                                                
                                                faces = []
                                                
                                                for face in object:
                                                    
                                                    face_id, face_xmin, face_ymin, face_xmax, face_ymax = get_IndexAndCoord(face)
                                                    face_xmiddle = (face_xmin + face_xmax) / 2
                                                    face_ymiddle = (face_ymin + face_ymax) / 2
                                                    face_character_id = face.attrib["character"]
                                                    face_instance = Face(face_id, face_xmin, face_ymin, face_xmax, face_ymax, face_xmiddle, face_ymiddle, face_character_id)
                                                    faces.append(face_instance)
                                            
                                                body_instance = Body(body_id, body_xmin, body_ymin, body_xmax, body_ymax, body_xmiddle, body_ymiddle, body_character_id, faces)
                                                bodys.append(body_instance)
                                            
                                            if object.tag == "text":
                                                
                                                line_id, line_xmin, line_ymin, line_xmax, line_ymax = get_IndexAndCoord(object)
                                                line_xmiddle = (line_xmin + line_xmax) / 2
                                                line_ymiddle = (line_ymin + line_ymax) / 2
                                                line_character_id = object.attrib["character"]
                                                line_text = object.text
                                                line_instance = Line(line_id, line_xmin, line_ymin, line_xmax, line_ymax, line_xmiddle, line_ymiddle, line_character_id, line_text, None, None)
                                                lines.append(line_instance)
                                                
                                        frame_instance = Frame(frame_id, frame_xmin, frame_ymin, frame_xmax, frame_ymax, frame_xmiddle, frame_ymiddle, bodys, lines)
                                        frames.append(frame_instance)
                                        
                                    arrayframes.append(frames)
                                
                                page_instance = Page(page_id, page_xmin, page_ymin, page_xmax, page_ymax, page_xmiddle, page_ymiddle, arrayframes)
                                pages.append(page_instance)
                            
                            episode_instance = Episode(episode_id, pages)
                            episodes.append(episode_instance)
                        
        comic_instance = Comic(file, title, author, era, publisher, target, genre, id_name, episodes, [])
        comics.append(comic_instance)
        
    return comics


if __name__ == "__main__":
    
    dirpath = "./datas/tests/annotations"
    files = glob.glob(os.path.join(dirpath, "*.xml"))
    
    comics = get_comics(files)
    
    episodes = comics[0].get_Episodes()
    pages = episodes[0].get_Pages()
    bands = pages[1].get_Frames()
    frames = bands[1]
    
    for frame in frames:
        
        lines = frame.get_Lines()
        
        for line in lines:
            
            text = line.get_Text()
            print(text)
    