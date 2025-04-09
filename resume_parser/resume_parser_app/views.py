# Create your views here.
import re
from django.shortcuts import render
from .forms import ResumeUploadForm
import PyPDF2
import docx


def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None


def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error processing DOCX: {e}")
        return None


def parse_resume(file):
    file_path = file.name.lower()
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file)
    else:
        print("Unsupported file format.")
        return None


def keyword_match(resume_text, job_keywords):
    keyword_freq = {}
    for keyword in job_keywords:
        matches = re.findall(keyword.lower(), resume_text.lower())
        keyword_freq[keyword] = len(matches)
    return keyword_freq


def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            # Parse the resume
            resume_text = parse_resume(resume.file)
            if resume_text:
                # Save extracted text
                resume.extracted_text = resume_text
                # Match keywords
                keywords = ["python", "machine learning", "Selenium", "SQL", "Linux","automation"]
                keyword_freq = keyword_match(resume_text, keywords)
                resume.keyword_matches = keyword_freq
                resume.save()
                return render(request, 'resume_parser_app/results.html', {'resume': resume, 'matches': keyword_freq})
            else:
                resume.delete()
                return render(request, 'resume_parser_app/error.html', {'message': 'Error processing the file.'})
    else:
        form = ResumeUploadForm()
    return render(request, 'resume_parser_app/upload.html', {'form': form})

# View for the results page
def results(request):
    return render(request, 'resume_parser_app/results.html')