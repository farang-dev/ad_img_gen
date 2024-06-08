import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.title("Product Image Variation Generator")

# Function to generate image variations using DALL-E 2 API
def generate_variations(image, api_key):
    url = "https://api.openai.com/v1/images/variations"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    # Convert image to bytes using BytesIO
    with BytesIO() as buffer:
        # Convert the image to PNG mode
        image = image.convert('RGB')  # Convert to RGB first
        image.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()

    # Create multipart/form-data
    files = {'image': ('image.png', image_bytes, 'image/png')}
    data = {
        "n": 3,  # Number of variations to generate
        "size": "1024x1024"  # Output image size
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        st.error(f"Error generating variations: {response.status_code}")
        st.write(f"Response Text: {response.text}")
        return None

# Get OpenAI API key from user input
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Image upload
uploaded_image = st.file_uploader("Upload your product image", type=["png"])

if uploaded_image is not None and api_key:
    image = Image.open(uploaded_image)

    # Display original image
    st.image(image, caption="Original Image")

    # Generate variations and display them
    variations = generate_variations(image, api_key)
    if variations:
        st.subheader("Generated Variations:")
        for variation in variations:
            image_url = variation["url"]
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Variation")

elif uploaded_image is not None:
    st.warning("Please enter your OpenAI API key.")
elif api_key:
    st.warning("Please upload a product image.")
else:
    st.info("Please upload a product image and enter your OpenAI API key.")
