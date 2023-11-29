from transformers import BertJapaneseTokenizer, BertForNextSentencePrediction
import torch

### Classify next sentence using ``bertForNextSentencePrediction``
# Going back to our initial input
tokenizer = BertJapaneseTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-v3") 
text = "[CLS] Who was Jim Henson ? [SEP] Jim Henson was a puppeteer [SEP]"
tokenized_text = tokenizer.tokenize(text)
indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
segments_ids = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
tokens_tensor = torch.tensor([indexed_tokens])
segments_tensors = torch.tensor([segments_ids])

model = BertForNextSentencePrediction.from_pretrained("cl-tohoku/bert-base-japanese-v3") 
model.eval()

tokens_tensor = tokens_tensor.to('cuda')
segments_tensors = segments_tensors.to('cuda')
model.to('cuda')

# Predict the next sentence classification logits
with torch.no_grad():
    next_sent_classif_logits = model(tokens_tensor, segments_tensors)

print(torch.softmax(next_sent_classif_logits[0], dim=1))
# tensor([[1.0000e+00, 2.8665e-06]], device='cuda:0')