from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re

MODEL_NAME = "Vamsi/T5_Paraphrase_Paws"

# Load model once
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def split_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences


def paraphrase_sentence(sentence, num_return_sequences=3):
    text = "paraphrase: " + sentence + " </s>"

    encoding = tokenizer._encode_plus(
        text,
        padding=True,
        return_tensors="pt"
    )

    input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]

    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_masks,
        max_length=256,
        num_beams=10,
        num_return_sequences=num_return_sequences,
        temperature=1.5
    )

    paraphrases = set()

    for output in outputs:
        decoded = tokenizer.decode(output, skip_special_tokens=True)
        paraphrases.add(decoded)

    return list(paraphrases)


def rephrase_text(text):
    sentences = split_sentences(text)

    all_variations = []

    for sentence in sentences:
        if sentence.strip():
            variations = paraphrase_sentence(sentence)
            all_variations.append(variations)

    # Combine sentence variations into full paragraph variations
    combined_results = []

    for i in range(3):
        paragraph = []
        for sentence_group in all_variations:
            if i < len(sentence_group):
                paragraph.append(sentence_group[i])
        combined_results.append(" ".join(paragraph))

    return combined_results