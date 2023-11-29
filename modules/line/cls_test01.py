from transformers import BertJapaneseTokenizer, BertForNextSentencePrediction
import torch


class FeaturePretrainedBert:
    
    def __init__(self):
    
        super().__init__()
        self.tokenizer = BertJapaneseTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-v3") 
        self.model = BertForNextSentencePrediction.from_pretrained("cl-tohoku/bert-base-japanese-v3") 

    def get(self, primary_text: str, secondary_text: str):
    
        encoding = self.tokenizer(primary_text, secondary_text, return_tensors="pt") 
        outputs = self.model(**encoding, labels=torch.LongTensor([1])) 
        logits = outputs.logits 
        is_next = logits[0, 0] > logits[0, 1] # True : 続く, False : 続かない

        return is_next


xInstance = FeaturePretrainedBert()
x = xInstance.get("これは何ですか", "助けて")
print(x)

