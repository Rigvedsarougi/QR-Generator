import streamlit as st
import qrcode
import uuid
import io

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
    
    # Convert PIL image to bytes
    img_byte_arr = io.BytesIO()
    qr_img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr, unique_id

# Streamlit UI
st.title("QR Code Generator")

# Input field for user to enter data
data = st.text_input("Enter data to encode in QR code")

# Button to generate QR code
if st.button("Generate QR Code"):
    if data:
        qr_img_bytes, unique_id = generate_unique_qr(data)
        st.image(qr_img_bytes, caption=f"QR code with unique ID: {unique_id}", use_column_width=True)
        
        # Display user information
        st.markdown("### Made by:")
        st.write("Name: Rigved Sarougi", "Email: irigved2000@gmail.com", "LinkedIn: [Rigved Sarougi](https://www.linkedin.com/in/rigved-sarougi/)")

        
    else:
        st.warning("Please enter some data to generate QR code.")
