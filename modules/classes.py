
class Comic:
    def __init__(self, File, Title, Author, Era, Publisher, Target, Genre, CharacterIndex_CharacterName, Episodes, Pages):
        self.File = File
        self.Title = Title
        self.Author = Author
        self.Era = Era
        self.Publisher = Publisher
        self.Target = Target
        self.Genre = Genre
        self.CharacterIndex_CharacterName = CharacterIndex_CharacterName
        self.Episodes = Episodes
        self.Pages = Pages

    def get_File(self):
        return self.File

    def get_Title(self):
        return self.Title

    def get_Author(self):
        return self.Author
    
    def get_Era(self):
        return self.Era

    def get_Publisher(self):
        return self.Publisher
    
    def get_Target(self):
        return self.Target

    def get_Genre(self):
        return self.Genre
    
    def get_CharacterIndex_CharacterName(self):
        return self.CharacterIndex_CharacterName
   
    def get_Episodes(self):
        return self.Episodes
    
    def get_Pages(self):
        return self.Pages
    

class Episode:
    def __init__(self, Index, Pages):
        self.Index = Index
        self.Pages = Pages
        
    def get_Index(self):
        return self.Index
    

    def get_Pages(self):
        return self.Pages
    

class Core:
    def __init__(self, Index, xMin, yMin, xMax, yMax):
        self.Index = Index
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax
        self.yMax = yMax
        
    def get_Index(self):
        return self.Index

    def get_xMin(self):
        return self.xMin
    
    def get_yMin(self):
        return self.yMin
    
    def get_xMax(self):
        return self.xMax
    
    def get_yMax(self):
        return self.yMax
    
    def set_xMin(self, xMin):
        self.xMin = xMin
        
    def set_yMin(self, yMin):
        self.yMin = yMin
        
    def set_xMax(self, xMax):
        self.xMax = xMax
        
    def set_yMax(self, yMax):
        self.yMax = yMax


class Object(Core):
    def __init__(self, Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle):
        super().__init__(Index, xMin, yMin, xMax, yMax)
        self.xMiddle = xMiddle
        self.yMiddle = yMiddle
    
    def get_xMiddle(self):
        return self.xMiddle
    
    def get_yMiddle(self):
        return self.yMiddle
    
    def set_xMiddle(self, xMiddle):
        self.xMiddle = xMiddle
        
    def set_yMiddle(self, yMiddle):
        self.yMiddle = yMiddle
    
    def get_Width(self):
        return (self.xMax - self.xMin)
    
    def get_Height(self):
        return (self.yMax - self.yMin)
    
    
class Page(Object):
    def __init__(self, Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle, Frames):
        super().__init__(Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle)
        self.Frames = Frames

    def get_Frames(self):
        return self.Frames
    

class Frame(Object):
    def __init__(self, Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle, Bodys, Lines):
        super().__init__(Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle)
        self.Bodys = Bodys
        self.Lines = Lines
    
    def get_Bodys(self):
        return self.Bodys
    
    def get_Lines(self):
        return self.Lines
    
    def set_Bodys(self, Bodys):
        self.Bodys = Bodys
    
    def set_Lines(self, Lines):
        self.Lines = Lines
        

class Character(Object):
    def __init__(self, Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle, CharacterIndex):
        super().__init__(Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle)
        self.CharacterIndex = CharacterIndex
        
    def get_CharacterIndex(self):
        return self.CharacterIndex


class Face(Character):
    def __init__(self, Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle, CharacterIndex):
        super().__init__(Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle, CharacterIndex)


class Body(Character):
    def __init__(self, Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle, CharacterIndex, Faces):
        super().__init__(Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle, CharacterIndex)
        self.Faces = Faces

    def get_Faces(self):
        return self.Faces
    
    def set_Faces(self, Faces):
        self.Faces = Faces


class Line(Character):
    def __init__(self, Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle, CharacterIndex, Text, Label, Score):
        super().__init__(Index, xMin, yMin, xMax, yMax, xMiddle, yMiddle, CharacterIndex)
        self.Text = Text
        self.Label = Label
        self.Score = Score

    def get_Text(self):
        return self.Text
    
    def get_Label(self):
        return self.Label

    def get_Score(self):
        return self.Score
    
    def set_Text(self, Text):
        self.Text = Text

    def set_Label(self, Label):
        self.Label = Label
        
    def set_Score(self, Score):
        self.Score = Score
    