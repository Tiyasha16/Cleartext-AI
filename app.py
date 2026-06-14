from flask import Flask, render_template, request
from services.grammar_service import grammar_check
from services.rephrase_service import rephrase_text
import os
from PyPDF2 import PdfReader
# --mp--
import nltk
from services.plagiarism_service import check_plagiarism, save_to_db
from nltk.tokenize import sent_tokenize
from services.pdf_service import generate_report
from flask import send_file
from flask import session
import secrets

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = secrets.token_hex(16)
nltk.download('punkt')
nltk.download('punkt_tab')

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyse', methods=['POST'])
def analyse():
    uploaded_file = request.files.get("file")
    text_input = request.form.get("text")
    action = request.form.get("action")

    final_text = ""

    if uploaded_file and uploaded_file.filename != "":
        if not allowed_file(uploaded_file.filename):
            return "Only .txt and .pdf files are allowed."

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
        uploaded_file.save(file_path)

        extension = uploaded_file.filename.rsplit(".", 1)[1].lower()

        if extension == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                final_text = f.read()

        elif extension == "pdf":
            # reader = PdfReader(file_path)
            # for page in reader.pages:
            #     final_text += page.extract_text() or ""
            try:
                reader = PdfReader(file_path)

                for page in reader.pages:
                    try:
                        page_text = page.extract_text()

                        if page_text:
                            page_text = page_text.encode("utf-8", "ignore").decode("utf-8")
                            final_text += page_text

                    except Exception as e:
                        print("Skipping problematic page:", e)
                        continue
            except Exception as e:
                print("PDF reading error:", e)

    elif text_input and text_input.strip() != "":
        final_text = text_input

    else:
        return "No input provided!"

    if action == "grammar":
        highlighted, corrected, error_count = grammar_check(final_text)
        save_to_db(final_text)

        return render_template(
            "grammar_result.html",
            original_highlighted=highlighted,
            corrected_text=corrected,
            error_count=error_count
        )
    
    if action == "rephrase":
        variations = rephrase_text(final_text)
        save_to_db(final_text)

        return render_template(
            "rephrase_result.html",
            original_text=final_text,
            variations=variations
        )
        
    if action == "plagiarism":
        percent, plag_sentences = check_plagiarism(final_text)

        save_to_db(final_text)

        return render_template(
            "plagiarism_result.html",
            plagiarism_percent=round(percent, 2),
            plag_sentences=plag_sentences
        )
    
    if action == "all":
        import json
        import uuid
        # Grammar
        highlighted, corrected, error_count = grammar_check(final_text)

        # Plagiarism
        plagiarism_percent, plag_sentences = check_plagiarism(final_text)

        # Rephrasing
        variations = rephrase_text(final_text)

        # Save new doc
        save_to_db(final_text)

        # Scores
        words = len(final_text.split())
        sentences = len(sent_tokenize(final_text))

        grammar_score = max(0, 100 - ((error_count / words) * 100))
        originality_score = 100 - plagiarism_percent
        readability_score = max(0, 100 - (words / sentences))

        final_score = (
            0.4 * grammar_score +
            0.4 * originality_score +
            0.2 * readability_score
        )

        # session["report_data"] = {
        #     "final_score": round(final_score,2),
        #     "grammar_score": round(grammar_score,2),
        #     "originality_score": round(originality_score,2),
        #     "plagiarism_percent": round(plagiarism_percent,2),
        #     "corrected_text": corrected,
        #     "plag_sentences": plag_sentences,
        #     "variations": variations
        # }

        report_data = {
            "final_score": round(final_score,2),
            "grammar_score": round(grammar_score,2),
            "originality_score": round(originality_score,2),
            "plagiarism_percent": round(plagiarism_percent,2),
            "corrected_text": corrected,
            "plag_sentences": plag_sentences,
            "variations": variations
        }

        # generating and storing report
        report_id = str(uuid.uuid4())
        with open(f"reports/{report_id}.json", "w") as f:
            json.dump(report_data, f)
    
        return render_template(
            "analyse_result.html",
            final_score=round(final_score, 2),
            grammar_score=round(grammar_score, 2),
            originality_score=round(originality_score, 2),
            readability_score=round(readability_score, 2),
            original_highlighted=highlighted,
            corrected_text=corrected,
            plagiarism_percent=round(plagiarism_percent, 2),
            plag_sentences=plag_sentences,
            variations=variations,
            report_data=report_data,
            report_id=report_id,
        )
    
    return "Other features coming soon."

@app.route('/download_report/<report_id>')
def download_report(report_id):
    import json

    path = f"reports/{report_id}.json"
    if not os.path.exists(path):
        return "No report data found"

    with open(path, "r") as f:
        data = json.load(f)

    filename = generate_report(data)
    return send_file(filename, as_attachment=True)

    

if __name__ == '__main__':
    app.run(debug=True)