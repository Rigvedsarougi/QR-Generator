import streamlit as st
import qrcode
import uuid
import io

def generate_unique_qr(data, is_url=False):
    # If the data is a URL, don't add a unique ID
    if is_url:
        data_with_id = data
    else:
        # Generate a unique ID and concatenate
        unique_id = str(uuid.uuid4())
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
    
    return img_byte_arr, data_with_id

# Streamlit UI
st.title("QR Code Generator")

# Input field for user to enter data
data = st.text_input("Enter data to encode in QR code (e.g., URL or text)")

# Checkbox to indicate if the data is a URL
is_url = st.checkbox("Is this a URL?")

# Button to generate QR code
if st.button("Generate QR Code"):
    if data:
        qr_img_bytes, generated_data = generate_unique_qr(data, is_url=is_url)
        st.image(qr_img_bytes, caption=f"QR Code for: {generated_data}", use_container_width=True)
        
        # If the data is a URL, provide a clickable link
        if is_url:
            st.markdown(f"[Click here to open the link]({generated_data})")
        
        # Display user information
        st.markdown("### Made by:")
        st.write(
            "Name: Rigved Sarougi",
            "Email: rigvedsarougi@gmail.com",
            "LinkedIn: [Rigved Sarougi](https://www.linkedin.com/in/rigved-sarougi/)"
        )

        # Add download button for QR code image
        st.download_button(
            label="Download QR Code",
            data=qr_img_bytes,
            file_name="generated_qr_code.png",
            mime="image/png"
        )
    else:
        st.warning("Please enter some data to generate a QR code.")
