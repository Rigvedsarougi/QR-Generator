import streamlit as st
import qrcode
import uuid

def generate_unique_qr(data):
    # Generate a unique ID
    unique_id = str(uuid.uuid4())
    
    # Concatenate the data with the unique ID
    data_with_id = f"{data}-{unique_id}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_with_id)
    qr.make(fit=True)
    
    # Create an image from the QR code
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    return qr_img, unique_id

# Streamlit UI
st.title("Unique QR Code Generator")

# Input field for user to enter data
data = st.text_input("Enter data to encode in QR code")

# Button to generate QR code
if st.button("Generate QR Code"):
    if data:
        qr_img, unique_id = generate_unique_qr(data)
        st.image(qr_img, caption=f"QR code with unique ID: {unique_id}", use_column_width=True)
    else:
        st.warning("Please enter some data to generate QR code.")
