import pytesseract
from PIL import Image
import os

# Set path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path as per your system

# Function to extract text from image
def extract_text_from_image(image_path):
    # Open image using Pillow
    img = Image.open(image_path)
    
    # Extract text from image using pytesseract
    extracted_text = pytesseract.image_to_string(img)

    # Return the extracted text
    return extracted_text

# Function to format extracted text to LaTeX
def format_to_latex(text):
    # Initial formatting for LaTeX output
    latex_code = "\\begin{align}\n"

    # Split text into lines and format for LaTeX
    lines = text.split('\n')
    for line in lines:
        # Avoid empty lines
        if line.strip():
            latex_code += f"{line.strip()} \\\\\n"

    latex_code += "\\end{align}"
    
    return latex_code

# Function to save LaTeX to file
def save_latex_to_file(latex_code, output_file):
    with open(output_file, 'w') as f:
        f.write(latex_code)
    print(f"Latex code saved to {output_file}")

if __name__ == "__main__":
    # Set the image path directly
    image_path = 'x.jpg'
    
    if os.path.exists(image_path):
        # Extract text from image
        extracted_text = extract_text_from_image(image_path)
        
        # Format the text to LaTeX
        latex_code = format_to_latex(extracted_text)
        
        # Output LaTeX code to a file
        output_file = 'output_latex.tex'
        save_latex_to_file(latex_code, output_file)

        print("Extracted Text: \n", extracted_text)
        print("Generated LaTeX Code: \n", latex_code)
    else:
        print(f"Image path '{image_path}' does not exist. Please provide a valid path.")
