
from modules.basic_research.side_frames import *



if __name__ == "__main__":
    
    with open("./datas/others/segment.json", "r") as file:
        
        SegmentJson = json.load(file)
    
    dirpath = "./datas/tests/annotations"
    files = glob.glob(os.path.join(dirpath, "*.xml"))
    
    Comics = get_comics(files)
    
    for xComic in Comics:
        
        SideFrameInstances = get_SideFrame(xComic, SegmentJson)
        
        for xSideFrames in SideFrameInstances:
            
            fFrameIndex = xSideFrames[0].get_BodyRate()
            bFrameIndex = xSideFrames[1].get_BodyRate()
            print(fFrameIndex,bFrameIndex)