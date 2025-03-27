import os
import docx
from docx.shared import Inches
from fpdf import FPDF
import requests
import json

def generate_text(prompt):
    url = "http://localhost:11434/api/generate"  # Ollama local server
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        return response.json().get("response", "No response received")
    except requests.exceptions.RequestException as e:
        print(f"Error generating text: {e}")
        return "Error generating text"

def generate_book():
    # Create a new Word document
    doc = docx.Document()
    title = "AI in Daily Life"
    doc.add_heading(title, 0)
    
    introduction = generate_text("Write an introduction about AI in daily life.")
    doc.add_paragraph("Introduction")
    doc.add_paragraph(introduction)
    
    doc.add_heading('Table of Contents', level=1)
    doc.add_paragraph("1. Smart Homes\n2. Healthcare\n3. Finance\n4. Productivity\n5. Conclusion")
    
    sections = [
        ("Smart Homes", "How AI-powered devices such as smart assistants and IoT devices enhance daily convenience."),
        ("Healthcare", "How AI assists in diagnostics, personalized treatment, and medical research."),
        ("Finance", "How AI helps in fraud detection, automated trading, and financial planning."),
        ("Productivity", "How AI-driven tools automate tasks, enhance efficiency, and support decision-making.")
    ]
    
    for title, prompt in sections:
        doc.add_heading(title, level=1)
        content = generate_text(prompt)
        doc.add_paragraph(content)
    
    doc.add_heading("Conclusion", level=1)
    conclusion = generate_text("Write a conclusion about the impact of AI in daily life.")
    doc.add_paragraph(conclusion)
    
    # Save the Word document
    word_filename = "AI_in_Daily_Life.docx"
    doc.save(word_filename)
    
    # Convert to PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    
    for title, prompt in sections:
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt=title, ln=True)
        pdf.set_font("Arial", size=12)
        content = generate_text(prompt)
        pdf.multi_cell(0, 10, content)
        pdf.ln(5)
    
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Conclusion", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, conclusion)
    
    pdf_filename = "AI_in_Daily_Life.pdf"
    pdf.output(pdf_filename)
    
    print(f"Book saved as {word_filename} and {pdf_filename}")

if __name__ == "__main__":
    generate_book()
