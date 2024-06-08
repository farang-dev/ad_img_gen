import streamlit as st
from PIL import Image
from io import BytesIO
import requests

st.title("Product Image Background Changer")

# Function to generate a background image using DALL-E 2 API
def generate_background(prompt):
    api_key = ""  # Replace with your actual DALL-E 2 API key
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "n": 1,  # Generate only one background
        "size": "1024x1024"  # Output image size
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["data"][0]["url"]  # Get the URL of the generated image
    else:
        st.error(f"Error generating background: {response.status_code}")
        st.write(f"Response Text: {response.text}")
        return None

# Image upload
uploaded_image = st.file_uploader("Upload your product image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    product_image = Image.open(uploaded_image)

    # Display the original product image
    st.image(product_image, caption="Original Product Image")

    # Text input for background description
    background_prompt = st.text_input("Describe the background you want (e.g., 'a white studio background', 'a beach at sunset')")

    # Generate background image
    background_url = generate_background(background_prompt)

    if background_url:
        # Fetch and display the generated background
        response = requests.get(background_url)
        background_image = Image.open(BytesIO(response.content))
        st.image(background_image, caption="Generated Background")

        # Check dimensions and resize if necessary
        if product_image.size != background_image.size:
            product_image = product_image.resize(background_image.size)

        # Combine product image and background (but don't display it yet)
        product_image = product_image.convert('RGBA')  # Make sure product image has alpha channel
        background_image = background_image.convert('RGBA')
        combined_image = Image.alpha_composite(background_image, product_image)

        # Display the product image with the changed background
        st.image(combined_image, caption="Product Image with Changed Background")

# Handle errors related to API call or image loading
else:
    st.info("Please upload a product image.")
