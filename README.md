# PDF Number Extractor

This Python script extracts the largest number from PDF files, considering context for scaling (e.g., millions, billions).

## Setup

1. Ensure you have a recent python version installed.
2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Place PDF files in the `input` directory.
2. Run the script:
   ```
   python main.py
   ```

## Code Explanation

The development of this script progressed through several iterations, each addressing specific challenges:

1. Initial Implementation:
   The first version focused on extracting raw text from PDF files and identifying the largest number using basic regular expressions. This approach provided a foundation but lacked contextual understanding.

2. Context-Aware Scaling:
   Recognizing the importance of contextual information, the script was enhanced to consider scaling factors. It now detects keywords like "million" or "billion" near numerical values and applies appropriate scaling. This improvement ensured accurate representation of large values mentioned in the text.

3. Tabular Data Processing + Refinement for Consistency:
   Upon discovering that the largest number in the document was in a table, which the initial implementation struggled to interpret correctly, the context window for analyzing surrounding text was expanded. This modification improved the script's ability to correctly interpret and scale numbers in both inline text and tabular formats by finding table headers with things like (dollars in millions) more readily. By employing a larger context window, the script now processes both inline and tabular numerical data more accurately, providing a reliable method for identifying the largest number in various document structures.
