import re
import PyPDF2
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract raw text from the PDF."""
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
    """Find the largest number from the extracted PDF text, considering scaling context like 'millions'."""
    if text is None:
        return None, None

    # Updated regex pattern to find all numbers (with commas, optional decimals, and optional signs)
    number_pattern = r'[-+]?\d{1,3}(?:,\d{3})*(?:\.\d+)?'
    numbers = re.findall(number_pattern, text)

    largest_number = float('-inf')
    largest_original = ""

    for number in numbers:
        clean_num = number.replace(',', '')  # Remove commas
        try:
            value = float(clean_num)  # Convert the number to a float

            # Check for scaling context (millions, billions, etc.) near the number
            context_start = max(0, text.index(number) - 100)
            context_end = min(len(text), text.index(number) + 100)
            context = text[context_start:context_end].lower()

            # Detect if scale context (millions, billions, etc.) is mentioned
            current_factor = 1  # Default scale factor
            if 'million' in context or 'millions' in context:
                current_factor = 1_000_000
            elif 'billion' in context or 'billions' in context:
                current_factor = 1_000_000_000
            elif 'thousand' in context or 'thousands' in context:
                current_factor = 1_000

            # Apply the scale factor only once
            value *= current_factor

            # Track the largest number found
            if value > largest_number:
                largest_number = value
                largest_original = number

        except ValueError:
            continue  # Skip any number we can't convert to float

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
