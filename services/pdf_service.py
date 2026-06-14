from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
import os
import uuid
import re


def clean_pdf_text(text):
    text = text.encode('utf-8', 'ignore').decode('utf-8')
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    return text

def clean_text(text):
    if not text:
        return ""

    text = str(text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = text.replace("\n", "<br/>")

    return text


def generate_report(data):

    # create reports folder
    os.makedirs("reports", exist_ok=True)

    filename = f"reports/report_{uuid.uuid4().hex}.pdf"

    styles = getSampleStyleSheet()

    normal = styles["Normal"]
    heading = styles["Heading2"]
    title = styles["Title"]

    story = []

    # Title
    story.append(Paragraph("AI Text Analyzer Report", title))
    story.append(Spacer(1, 12))

    # Scores
    story.append(Paragraph("Overall Scores", heading))
    story.append(Spacer(1, 6))

    story.append(Paragraph(f"Final Score: {data.get('final_score')}", normal))
    story.append(Paragraph(f"Grammar Score: {data.get('grammar_score')}", normal))
    story.append(Paragraph(f"Originality Score: {data.get('originality_score')}", normal))
    story.append(Paragraph(f"Plagiarism: {data.get('plagiarism_percent')}%", normal))

    story.append(Spacer(1, 20))

    # Corrected Text
    story.append(Paragraph("Corrected Text", heading))
    story.append(Spacer(1, 6))

    corrected = clean_text(data.get("corrected_text", ""))

    story.append(Paragraph(corrected, normal))
    story.append(PageBreak())

    # Plagiarism Section
    story.append(Paragraph("Plagiarism Results", heading))
    story.append(Spacer(1, 10))

    plag_sentences = data.get("plag_sentences", [])

    for sentence, score in plag_sentences:
        text = clean_text(sentence)
        story.append(
            Paragraph(
                f"{text} (Similarity: {round(score * 100, 2)}%)",
                normal
            )
        )
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Rephrased Text
    story.append(Paragraph("Rephrased Versions", heading))
    story.append(Spacer(1, 10))

    variations = data.get("variations", [])

    for i, version in enumerate(variations):
        text = clean_text(version)

        story.append(
            Paragraph(
                f"Variation {i+1}: {text}",
                normal
            )
        )

        story.append(Spacer(1, 10))

    # Create PDF
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    doc.build(story)

    return filename