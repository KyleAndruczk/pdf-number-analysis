import re
import PyPDF2
import os
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file) 
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {str(e)}")
        return None

def find_largest_number(text):
    if text is None:
        return None, None
    
    # regex to find all numbers in the text, including those with commas and decimal points
    number_pattern = r'[-+]?[,.\d]+(?:[eE][-+]?\d+)?'
    numbers = re.findall(number_pattern, text)
    largest_number = float('-inf')
    largest_original = ""
    for number in numbers:
        # rm the commas and convert to float
        clean_num = number.replace(',', '')
        try: 
            value = float(clean_num)
            # check context of nearby words with scale
            context = text[max(0, text.index(number) - 50):min(len(text), text.index(number) + 50)]
            if 'million' in context.lower() or 'millions' in context.lower():
                value *= 1_000_000
            elif 'billion' in context.lower() or 'billions' in context.lower():
                value *= 1_000_000_000
            elif 'thousand' in context.lower() or 'thousands' in context.lower():
                value *= 1_000


            if value > largest_number:
                largest_number = value
                largest_original = number
        except ValueError:
            # skip if can't convert to float
            continue
    
    return (largest_number, largest_original) if largest_number != float('-inf') else (None, None)

def main():
    input_dir = Path("input")
    pdf_paths = [f for f in input_dir.iterdir() if f.suffix.lower() == '.pdf']
    
    if not pdf_paths:
        print("No PDF files found in the 'input' directory.")
        return
    
    for pdf_path in pdf_paths:
        print(f"Processing: {pdf_path.name}")
        text = extract_text_from_pdf(pdf_path)
        largest_number, largest_original = find_largest_number(text)
        
        if largest_number is not None:
            print(f'The largest number in the PDF {pdf_path.name} is {largest_original} which is {largest_number:,.2f}')
        else:
            print(f'No valid numbers found in {pdf_path.name}')
        print()

if __name__ == "__main__":
    main()