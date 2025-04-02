# Data was of NPTEL certificates
import pdfplumber
import re
import pandas as pd

# Function to extract data from PDF
def extract_data(pdf_path, csv_output):
    extracted_text = []
    
    # Open PDF and extract text from each page
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text.append(page.extract_text())
    
    full_text = "\n".join(extracted_text)
    
    # Regex pattern to extract required details
    pattern_with_roll = re.compile(
        r"([A-Z ]+)\n"  # Name
        r"([A-Za-z ]+)\n"  # Course Name
        r"(\d+)\n"  # Candidate Score
        r"([\d.]+)/25 ([\d.]+)/75\n"  # Online Assignments / Proctored Exam
        r"\d+\n.+?\n.+?\nRoll No: (\S+)"  # Roll No.
    )
    
    # Find all matches
    matches = pattern_with_roll.findall(full_text)
    
    # Store extracted data
    data = []
    for match in matches:
        name, course, score, assignments, exam, roll_no = match
        data.append([name.strip(), course.strip(), int(score), float(assignments), float(exam), roll_no])
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data, columns=["Name", "Course Name", "Consolidated Score", "Online Assignments", "Proctored Exam", "Roll No"])
    df.to_csv(csv_output, index=False)
    
    print(f"Data extracted and saved to {csv_output}")

# Example usage
pdf_path = '''<File Path>'''# Change this to your actual file path
csv_output = '''<Output File Path>'''# Change this to your actual file path
extract_data(pdf_path, csv_output)
