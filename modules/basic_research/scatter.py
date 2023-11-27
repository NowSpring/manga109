from modules.basic_research.side_frames import *
from modules.basic_research.range import get_ObjectRange

if __name__ == "__main__":
    
    with open("./datas/others/segment.json", "r") as file:
        SegmentJson = json.load(file)
    
    dirpath = "./datas/edited_tests/annotations"
    files = glob.glob(os.path.join(dirpath, "*.xml"))
    
    Comics = get_comics(files)
    
    for xComic in Comics:
        
        xEpisodes = xComic.get_Episodes()
        
        for yEpisode in xEpisodes:
            
            yPages = yEpisode.get_Pages()
            
            for zPage in yPages:
                
                zBands = zPage.get_Frames()
                
                for vBand in zBands:
                    
                    for wFrame in vBand:
                        
                        