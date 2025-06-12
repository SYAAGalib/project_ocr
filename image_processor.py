from langchain.llms import Ollama  # Correct import
from PIL import Image
import pytesseract

# Initialize the Ollama model
ollama = Ollama(model="qwen2:1.5b")

def extract_text_from_image(image_path):
    """
    Extract text from image using OCR (pytesseract).
    """
    img = Image.open(image_path)  # Load the image
    text = pytesseract.image_to_string(img)  # Extract text using pytesseract
    return text

def send_text_to_ollama(text):
    """
    Send extracted text to the Ollama model for rewriting.
    """
    prompt = f"Rewrite the following text exactly as written: {text}"
    response = ollama(prompt)
    return response

if __name__ == "__main__":
    # Assuming the image is named 'x.jpg' and is in the same directory
    image_path = "x.jpg"
    
    # Step 1: Extract text from the image
    extracted_text = extract_text_from_image(image_path)
    print(f"Extracted Text: {extracted_text}")
    
    # Step 2: Send the text to the Ollama model
    rewritten_text = send_text_to_ollama(extracted_text)
    print(f"Rewritten Text: {rewritten_text}")
