import PyPDF2
import docx
import re


# Function to extract text from PDF
def extract_text_from_pdf(file_path):

    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None


# Function to extract text from DOCX
def extract_text_from_docx(file_path):

    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return None


# Function to handle both file types
def parse_resume(file_path):

    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        print("Unsupported file format. Please provide either a PDF or DOCX file.")
        return None


def keyword_match(resume_text, job_keywords):

    keyword_freq = {}
    for keyword in job_keywords:
        matches = re.findall(keyword.lower(), resume_text.lower())
        keyword_freq[keyword] = len(matches)
    return keyword_freq


if __name__ == "__main__":

    resume_path = "CVDanVelea.pdf"  # Replace with your actual file path

    resume_text = parse_resume(resume_path)

    if resume_text:
        print("\nExtracted Resume Text:\n")
        print(resume_text)

        #Provide job keywords to match. Change with what you want.
        job_keywords = ["python", "automation","linux", "AI", "SQL"]

        # keyword matching
        matches = keyword_match(resume_text, job_keywords)

        # Display the results
        print("\nKeyword Matches:")
        for keyword, freq in matches.items():
            print(f"{keyword}: {freq}")
    else:
        print("Failed to extract resume text.")