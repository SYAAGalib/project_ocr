import streamlit as st
from PIL import Image
import image_processor  # Import the image processing module

def main():
    st.title("Text Recognition and Rewriting with Ollama Model")

    # Step 1: Upload the image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

        # Save the image to a temporary location
        image_path = "temp_image.jpg"
        image.save(image_path)

        # Step 2: Process the image (extract text and send it to the model)
        if st.button("Recognize and Rewrite Text"):
            st.write("Extracting text from image...")
            extracted_text = image_processor.extract_text_from_image(image_path)

            st.write("Sending text to Ollama model for rewriting...")
            rewritten_text = image_processor.send_text_to_ollama(extracted_text)

            # Step 3: Display the result
            st.write("Rewritten Text:")
            st.text_area("Output", rewritten_text)

if __name__ == "__main__":
    main()
