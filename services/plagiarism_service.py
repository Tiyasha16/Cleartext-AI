import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize

DB_FOLDER = "plagiarism_db"

os.makedirs(DB_FOLDER, exist_ok=True)

# Load semantic model once
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')


def split_sentences(text):
    return sent_tokenize(text)


def load_db_documents():
    docs = []
    for file in os.listdir(DB_FOLDER):
        with open(os.path.join(DB_FOLDER, file), 'r', encoding='utf-8') as f:
            docs.append(f.read())
    return docs


def syntactic_similarity(input_sentences, db_sentences):
    vectorizer = TfidfVectorizer()

    all_sentences = input_sentences + db_sentences
    tfidf_matrix = vectorizer.fit_transform(all_sentences)

    input_vec = tfidf_matrix[:len(input_sentences)]
    db_vec = tfidf_matrix[len(input_sentences):]

    similarity = cosine_similarity(input_vec, db_vec)

    return similarity


def semantic_similarity(input_sentences, db_sentences):
    input_embeddings = semantic_model.encode(input_sentences)
    db_embeddings = semantic_model.encode(db_sentences)

    similarity = cosine_similarity(input_embeddings, db_embeddings)

    return similarity


def check_plagiarism(text):
    input_sentences = split_sentences(text)

    db_docs = load_db_documents()
    db_sentences = []

    for doc in db_docs:
        db_sentences.extend(split_sentences(doc))

    if not db_sentences:
        return 0, []

    syn_sim = syntactic_similarity(input_sentences, db_sentences)
    sem_sim = semantic_similarity(input_sentences, db_sentences)

    final_scores = (syn_sim + sem_sim) / 2

    plagiarised_sentences = []

    for i, row in enumerate(final_scores):
        max_score = max(row)
        if max_score > 0.65:
            plagiarised_sentences.append((input_sentences[i], max_score))

    plagiarism_percent = (len(plagiarised_sentences) / len(input_sentences)) * 100

    return plagiarism_percent, plagiarised_sentences


def save_to_db(text):
    filename = f"doc_{len(os.listdir(DB_FOLDER)) + 1}.txt"
    with open(os.path.join(DB_FOLDER, filename), 'w', encoding='utf-8') as f:
        f.write(text)