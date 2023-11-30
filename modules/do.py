import os
import glob
from operator import attrgetter
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import japanize_matplotlib

from main import get_comics
from line.bert import analyze_emotion

def is_all_zero(lst):
    
    for item in lst:
    
        if item != 0:
    
            return False
    
    return True

if __name__ == "__main__":
    
    dirpath = "./datas/tests/annotations"
    files = glob.glob(os.path.join(dirpath, "*.xml"))
    
    positive_lines = []
    negative_lines = []
    
    comics = get_comics(files)
    file = comics[0].get_File()
    id_name = comics[0].get_CharacterIndex_CharacterName()
    episodes = comics[0].get_Episodes()
    
    i = 2
    pages = episodes[i - 1].get_Pages()
        
    for page in pages:
        
        frames = page.get_Frames()
        
        for frame in frames:
            
            lines = frame.get_Lines()
            
            for line in lines:
                
                text = line.get_Text()
                emorion_data = analyze_emotion(text)
                label = emorion_data[0]["label"]
                score = emorion_data[0]["score"]
                line.set_Label(label)
                line.set_Score(score)
                
                if label == "POSITIVE":
            
                    positive_lines.append(line)
                    
                elif label == "NEGATIVE":
                    
                    negative_lines.append(line)
    
    positive_lines.sort(key = attrgetter('Score'), reverse=True)
    negative_lines.sort(key = attrgetter('Score'), reverse=True)
    
    for line in positive_lines[:10]:
        
        text = line.get_Text()
        score = line.get_Score()
        print(text, ":", score)
        
    print("")
    
    for line in negative_lines[:10]:
        
        text = line.get_Text()
        score = line.get_Score()
        print(text, ":", score)
        
        
    # ----
    
    
    id_name = comics[0].get_CharacterIndex_CharacterName()
    name_emotion = {}
    max_score = 0
    
    for id in id_name:
    
        sum_positive_scores = []
        sum_negative_scores = []
        
        for page in pages:
            
            sum_positive_score = 0
            sum_negative_score = 0

            frames = page.get_Frames()
            
            for frame in frames:
                
                lines = frame.get_Lines()
                
                for line in lines:
                    
                    character_id = line.get_CharacterIndex()
                    
                    if character_id == id:
                        
                        label = line.get_Label()
                        score = line.get_Score()
                    
                        if label == "POSITIVE":
                            
                            sum_positive_score += score
                        
                        elif label == "NEGATIVE":
                            
                            sum_negative_score += score
                        
            sum_positive_scores.append(sum_positive_score)
            sum_negative_scores.append(sum_negative_score)
            
            max_positive_score = max(sum_positive_scores)
            max_negative_score = max(sum_negative_scores)
            
            if max(max_positive_score, max_negative_score) > max_score:
                max_score = max(max_positive_score, max_negative_score)
        
        if not ((is_all_zero(sum_positive_scores) == True) and 
                (is_all_zero(sum_negative_scores) == True)):
            
            name = id_name[id]
            name_emotion[name] = {"POSITIVE":sum_positive_scores, "NEGATIVE":sum_negative_scores}
            
    
    # ----
    
    
    folder_path = "datas/output/posi_nega_series/" + file + "/episode_" + str(i)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    
    # ----

    
    for name in name_emotion:
        
        plt.figure(figsize = (10,5))
        
        label_scores = name_emotion[name]
        sum_positive_scores = label_scores["POSITIVE"]
        sum_negative_scores = label_scores["NEGATIVE"]
        
        plt.plot(sum_positive_scores, linewidth = 2, color = "red", label = "POSITIVE")
        plt.plot(sum_negative_scores, linewidth = 2, color = "blue", label = "NEGATIVE")
        
        plt.ylim(-0.01, max_score + 0.01)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=13)
        plt.tick_params(labelsize=18)
        plt.tight_layout()
        
        image_path = os.path.join(folder_path, name)
        plt.savefig(image_path, dpi=300)
        
    
    # ----
    
    
    Colors = mcolors.TABLEAU_COLORS
    Colors = list(Colors.keys())
    
    for emotion in ["POSITIVE", "NEGATIVE"]:
        
        CI = 0
        plt.figure(figsize = (10,5))
        
        for id in id_name:
            
            name  = id_name[id]
            
            if name in name_emotion:
            
                label_scores = name_emotion[name]
                sum_emotion_scores = label_scores[emotion]
                plt.plot(sum_emotion_scores, linewidth = 2, color = Colors[CI], label = name)
                
            CI += 1
            
        plt.ylim(-0.01, max_score + 0.01)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5, fontsize=13)
        plt.tick_params(labelsize=18)
        plt.tight_layout()
        
        image_path = os.path.join(folder_path, emotion)
        plt.savefig(image_path, dpi=300)
        
                    
    # ----
    ######
    
    
    
    
    
    
    