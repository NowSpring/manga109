from PIL import Image, ImageDraw

from modules.basic_research.side_frames import *
    

def check_Segment(xFile, xSideFrames):
    
    def convert_to_3_digits(binary_string):
        
        if len(binary_string) < 3:
            # 文字列の長さが3未満の場合、左に0を追加して3文字にする
            binary_string = binary_string.zfill(3)
    
        return binary_string
    
    def is_file_in_folder(file_name, folder_path):
        
        file_path = os.path.join(folder_path, file_name)
        
        return os.path.isfile(file_path)
    
    def plt_rect(xFrame, xDraw, cFlag):
        
        xxMin = xFrame.get_xMin()
        xyMin = xFrame.get_yMin()
        xxMax = xFrame.get_xMax()
        xyMax = xFrame.get_yMax()
        
        if cFlag == True:

            xDraw.rectangle([(int(xxMin), int(xyMin)), (int(xxMax), int(xyMax))], outline = (255, 0, 0), width = 4)
            
        else:
            
            xDraw.rectangle([(int(xxMin), int(xyMin)), (int(xxMax), int(xyMax))], outline = (0, 255, 0), width = 4)
    
    fFrame, bFrame = xSideFrames
    fPageIndex = fFrame.get_PageIndex()
    bPageIndex = bFrame.get_PageIndex()
    
    # print(fPageIndex, bPageIndex)
    
    # xImgInputPath = "./datas/edited_tests/images/" + xFile + "/" + fPageIndex + ".jpg"
    # xOutputFolder = "./datas/outputs/check_segment/" + xFile 
    # xOutputPath = xOutputFolder + "/" + str(fPageIndex) + ".jpg"
    
    if fPageIndex == bPageIndex:
        
        fPageIndex = convert_to_3_digits(fPageIndex)
        xImgInputPath = "./datas/edited_tests/images/" + xFile + "/" + fPageIndex + ".jpg"
        xImg = Image.open(xImgInputPath)
        xDraw = ImageDraw.Draw(xImg)
        
        plt_rect(fFrame, xDraw, True,)
        plt_rect(bFrame, xDraw, False)
            
        xOutputFolder = "./datas/outputs_tests/check_segment/" + xFile 
        
        if not os.path.exists(xOutputFolder):
            
            os.makedirs(xOutputFolder)
        
        xOutputPath = xOutputFolder + "/" + str(fPageIndex) + ".jpg"
        xImg.save(xOutputPath)
        
    else:
        
        for xFrame in (fFrame, bFrame):
            
            xPageIndex = xFrame.get_PageIndex()
            xPageIndex = convert_to_3_digits(xPageIndex)
            xImgInputPath = "./datas/edited_tests/images/" + xFile + "/" + xPageIndex + ".jpg"
            xImg = Image.open(xImgInputPath)
            xDraw = ImageDraw.Draw(xImg)
            
            if xFrame == fFrame:
    
                plt_rect(xFrame, xDraw, True)
                
            else:
                
                plt_rect(xFrame, xDraw, False)
        
            xOutputFolder = "./datas/outputs_tests/check_segment/" + xFile 
            
            if not os.path.exists(xOutputFolder):
                
                os.makedirs(xOutputFolder)
            
            xOutputPath = xOutputFolder + "/" + str(xPageIndex) + ".jpg"
            xImg.save(xOutputPath)
    
    


if __name__ == "__main__":
    
    with open("./datas/others/segment.json", "r") as file:
        SegmentJson = json.load(file)
    
    dirpath = "./datas/edited_tests/annotations"
    files = glob.glob(os.path.join(dirpath, "*.xml"))
    
    Comics = get_comics(files)
    
    for xComic in Comics:
        
        xFile = xComic.get_File()
        xSideFrames = get_SideFrame(xComic, SegmentJson)
        
        for xxSideFrames in xSideFrames:
            
            check_Segment(xFile, xxSideFrames)
            
    