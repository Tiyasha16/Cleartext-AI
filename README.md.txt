# AI Text Analyzer 🚀

An AI-powered Flask web application for Grammar Checking, Rephrasing, and Hybrid Plagiarism Detection with PDF report generation.

---

## 📌 Overview

AI Text Analyzer is a modular NLP-based system that performs:

- ✅ Grammar Detection & Correction (LanguageTool)
- ✅ AI-based Rephrasing (T5 Transformer)
- ✅ Hybrid Plagiarism Detection (TF-IDF + Sentence Embeddings)
- ✅ Multi-factor AI Scoring
- ✅ Professional PDF Report Generation

The system supports both direct text input and file uploads (.txt, .pdf).

---

## 🏗 Tech Stack

**Frontend**
- HTML
- Tailwind CSS
- JavaScript

**Backend**
- Python Flask

**AI & NLP**
- LanguageTool (Rule-based grammar engine)
- T5 Transformer (Rephrasing)
- Sentence-Transformers MiniLM (Semantic similarity)
- TF-IDF + Cosine Similarity (Syntactic plagiarism detection)

**Reporting**
- ReportLab (PDF generation)

---

## 🧠 Features

### 1️⃣ Grammar Checker
- Detects grammar, punctuation, and spelling errors
- Highlights mistakes
- Provides corrected text

### 2️⃣ Rephrasing Engine
- Transformer-based paraphrasing
- Generates multiple variations
- Preserves original meaning

### 3️⃣ Plagiarism Detection
Hybrid approach:
- Syntactic similarity (TF-IDF)
- Semantic similarity (MiniLM embeddings)
- Combined similarity score

### 4️⃣ Analyse All
- Runs all modules together
- Generates:
  - Grammar Score
  - Originality Score
  - Readability Score
  - Final AI Score
- Downloadable detailed PDF report

---

## 📊 Scoring Formula

Final AI Score:

Final Score =
(0.4 × Grammar Score) +
(0.4 × Originality Score) +
(0.2 × Readability Score)

---

## 📂 Project Structure
