import streamlit as st
import qrcode
import uuid
import io
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image

# Function to generate a QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    qr_img.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()

# Function to generate a barcode
def generate_barcode(data, textless=False):
    # Generate barcode using Code128
    barcode = Code128(data, writer=ImageWriter())
    img_byte_arr = io.BytesIO()

    # Options to customize barcode rendering
    options = {
        "write_text": not textless,  # Hide or show text under barcode
        "text_distance": 2,  # Adjust distance between barcode and text
        "font_size": 10,     # Set text size
    }
    barcode.write(img_byte_arr, options=options)
    return img_byte_arr.getvalue()

# Streamlit UI
st.title("Product Barcode and QR Code Generator")

# Input fields for product details
st.header("Enter Product Details")
product_name = st.text_input("Product Name")
product_id = st.text_input("Product ID")
price = st.text_input("Price")
description = st.text_area("Product Description")

# Concatenate product details into a single string for encoding
if product_name and product_id:
    product_data = f"Product: {product_name}, ID: {product_id}, Price: {price}, Description: {description}"
else:
    product_data = None

# Options to select barcode or QR code
st.header("Choose Code Type")
code_type = st.radio("Select Code Type", ["QR Code", "Barcode"])

# Option for textless barcode
textless_option = st.checkbox("Generate Textless Barcode (Hide Text Underneath)")

# Generate code on button click
if st.button("Generate Code"):
    if product_data:
        if code_type == "QR Code":
            qr_image = generate_qr_code(product_data)
            st.image(qr_image, caption="Generated QR Code", use_container_width=True)
        elif code_type == "Barcode":
            barcode_image = generate_barcode(product_id, textless=textless_option)
            st.image(barcode_image, caption="Generated Barcode", use_container_width=True)
        
        # Display the product details
        st.subheader("Product Details:")
        st.text(f"Name: {product_name}")
        st.text(f"ID: {product_id}")
        st.text(f"Price: {price}")
        st.text(f"Description: {description}")
        
        # User information
        st.markdown("### Made by:")
        st.write(
            "Name: Rigved Sarougi",
            "Email: irigved2000@gmail.com",
            "LinkedIn: [Rigved Sarougi](https://www.linkedin.com/in/rigved-sarougi/)"
        )
    else:
        st.warning("Please fill in at least Product Name and Product ID.")
