import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import warnings
warnings.filterwarnings("ignore")

model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

dataset_path = '/kaggle/working/sample_lyrics_with_emotions.csv'
df = pd.read_csv(dataset_path)

def generate_lyrics_t5(emotion: str, seed_text: str, min_words: int = 75):
    try:
        emotion_lyrics = df[df['emotion'] == emotion]['processed_lyrics'].sample(1).values[0]
    except ValueError:
        emotion_lyrics = ""
    
    prompt = (
        f"{emotion}, "
        f"{seed_text}.{emotion_lyrics}. "
    )
    
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    with torch.no_grad():
        output = model.generate(input_ids,max_new_tokens=200,num_beams=5,no_repeat_ngram_size=2,temperature=0.7,length_penalty=1.2,early_stopping=True)

    generated_lyrics = tokenizer.decode(output[0], skip_special_tokens=True)
    
    word_count = len(generated_lyrics.split())
    if word_count < min_words:
        while word_count < min_words:
            prompt = generated_lyrics
            input_ids = tokenizer.encode(prompt, return_tensors='pt')
            output = model.generate(input_ids,max_new_tokens=150,num_beams=5,no_repeat_ngram_size=2,temperature=0.7,length_penalty=1.2,early_stopping=True)
            generated_lyrics += " " + tokenizer.decode(output[0], skip_special_tokens=True)
            word_count = len(generated_lyrics.split())
    
    formatted_lyrics = ", ".join(generated_lyrics.split(". "))
    return formatted_lyrics

if __name__ == "__main__":
    emotion = input("Enter the emotion: ").strip().lower()
    
    seed_text = input("Enter a seed text: ").strip()
    
    if emotion not in df['emotion'].unique():
        print(f"Emotion '{emotion}' not found in the dataset. Enter valid emotion.")
    else:
        generated_lyrics = generate_lyrics_t5(emotion, seed_text)
        print(f"Generated Lyrics for emotion '{emotion}' with seed text '{seed_text}':\n {seed_text} {generated_lyrics}")
