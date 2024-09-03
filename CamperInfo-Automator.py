import pdfplumber
import pandas as pd
from collections import defaultdict

# Path to your PDF file
pdf_path = "C:FileName.pdf"  # Update with PDF file name

def extract_info_from_pdf(pdf_path):
    data = {
        "Name": [],
        "Activity Restrictions": [],
        "Other Medical Issues": [],
        "EpiPen": [],
        "Allergies": [],
        "Other": [],
        " ":[]
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')

            i = 0
            while i < len(lines):
                if "Parent/Guardian 1:" in lines[i]:
                    # Extract Name from the line before "Parent/Guardian 1:"
                    name = lines[i-1].strip() if i > 0 else "Unknown"
                    data["Name"].append(name)

                    # Initialize placeholders for medical information
                    activity_restrictions = ""
                    other_medical_issues = ""
                    epipen = ""
                    allergies = ""
                    other_info = ""

                    j = i
                    while j < len(lines):
                        if "Parent/Guardian 1:" in lines[j] and j != i:
                            break  # Exit loop if we find a new "Parent/Guardian 1:"

                        # Extract Activity Restrictions, Other Medical Issues, EpiPen, Allergies, and Other
                        if "Activity Restrictions:" in lines[j]:
                            activity_restrictions = lines[j].split(":")[1].strip() if ':' in lines[j] else ""
                        elif "Other Medical Issues:" in lines[j]:
                            other_medical_issues = lines[j].split(":")[1].strip() if ':' in lines[j] else ""
                        elif "EpiPen?" in lines[j]:
                            epipen = lines[j].split(":")[1].strip() if ':' in lines[j] else ""
                        elif "Allergies" in lines[j]:
                            allergy_lines = []
                            k = j + 1
                            while k < len(lines) and not any(header in lines[k] for header in ["Parent/Guardian 1:", "Parent/Guardian 2:", "MEDICAL INFORMATION", "Activity Restrictions:", "Other Medical Issues:", "EpiPen?", "Allergies", "Other"]):
                                allergy_lines.append(lines[k].strip())
                                k += 1
                            allergies = ' '.join(allergy_lines).strip()
                        elif "Other" in lines[j]:
                            other_lines = []
                            k = j + 1
                            while k < len(lines) and not any(header in lines[k] for header in ["Parent/Guardian 1:", "Parent/Guardian 2:", "MEDICAL INFORMATION", "Activity Restrictions:", "Other Medical Issues:", "EpiPen?", "Allergies", "Other"]):
                                other_lines.append(lines[k].strip())
                                k += 1
                            other_info = ' '.join(other_lines).strip()
                        j += 1

                    data["Activity Restrictions"].append(activity_restrictions)
                    data["Other Medical Issues"].append(other_medical_issues)
                    data["EpiPen"].append(epipen)
                    data["Allergies"].append(allergies)
                    data["Other"].append(other_info)
                
                i += 1

    # Make sure all lists have the same length
    max_length = max(len(data[key]) for key in data)
    for key in data:
        while len(data[key]) < max_length:
            data[key].append("")

    return data

# Extract information
extracted_data = extract_info_from_pdf(pdf_path)

# Print extracted data
for key, value in extracted_data.items():
    print(f"{key}: {value}")

# Convert to DataFrame for further processing
df = pd.DataFrame(extracted_data)
print(df)

# Export to Excel
df.to_excel("FileName-info.xlsx", index=False)
