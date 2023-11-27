from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, BertJapaneseTokenizer

# 感情分析を行うモジュール
def analyze_emotion(text):
	# 1. 学習済みモデルの準備
	model = AutoModelForSequenceClassification.from_pretrained("koheiduck/bert-japanese-finetuned-sentiment")
	# 2. 日本語の単語分解
	tokenizer = BertJapaneseTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-whole-word-masking")

	# 3. 感情分析モデルの生成
	nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    
	emotion_data = nlp(text)
	return emotion_data

