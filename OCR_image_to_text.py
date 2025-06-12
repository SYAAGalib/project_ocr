import pytesseract
from PIL import Image
import os

# Function to perform OCR on an image and convert text to LaTeX
def ocr_image_to_latex(image_path, output_path):
    # Open the image file
    img = Image.open(image_path)
    
    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(img, lang='eng')
    
    # Convert the text to LaTeX format
    latex_text = "\\begin{document}\n" + text + "\n\\end{document}"
    
    # Write the LaTeX text to a file
    with open(output_path, 'w') as file:
        file.write(latex_text)

# Example usage
image_path = 'C:/Users/Admin/AI/ai/ai.jpg'  # Update this path to a valid image file
script_dir = os.path.dirname(__file__)
output_path = os.path.join(script_dir, 'output.txt')
ocr_image_to_latex(image_path, output_path)
print(f"LaTeX output written to {output_path}")