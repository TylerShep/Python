import torch
from transformers import BertTokenizer, BertModel
from pytube import YouTube
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from collections import defaultdict
from string import punctuation
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def get_video_transcript(url):
    yt = YouTube(url)
    caption = yt.captions.get_by_language_code('en')
    if caption is None:
        return None
    else:
        return caption.generate_srt_captions()

def clean_transcript(transcript):
    transcript = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', transcript)
    transcript = re.sub(r'\n', ' ', transcript)
    return transcript

def summarize_text(text, num_sentences):
    stop_words = set(stopwords.words('english') + list(punctuation))
    words = word_tokenize(text.lower())
    freq = FreqDist(words)
    rank = defaultdict(int)
    for i, sentence in enumerate(sent_tokenize(text)):
        for word in word_tokenize(sentence.lower()):
            if word in freq:
                rank[i] += freq[word]
    ranked_sentences = sorted(((rank[i], s) for i, s in enumerate(sent_tokenize(text))), reverse=True)
    summary = ' '.join([s for _, s in ranked_sentences[:num_sentences]])
    return summary

def get_bert_embedding(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].detach().numpy()

def main():
    model = BertModel.from_pretrained('bert-base-uncased')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    url = input('Enter YouTube video URL: ')
    transcript = get_video_transcript(url)
    if transcript is None:
        print('No English captions available for this video.')
    else:
        transcript = clean_transcript(transcript)
        summary = summarize_text(transcript, 3)
        print('Summary:', summary)
        embedding = get_bert_embedding(summary, model, tokenizer)
        print('BERT Embedding:', embedding)

if __name__ == '__main__':
    main()
