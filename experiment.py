import streamlit as st
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
import io
from PIL import Image

# Function to generate a barcode for a single product
def generate_barcode(product_id, textless=False):
    # Generate barcode using Code128
    barcode = Code128(product_id, writer=ImageWriter())
    img_byte_arr = io.BytesIO()
    options = {"write_text": not textless}  # Hide text if textless=True
    barcode.write(img_byte_arr, options=options)
    return img_byte_arr.getvalue()

# Streamlit UI
st.title("Bulk Product Barcode Generator")

# Instructions
st.markdown("""
### Instructions:
1. Prepare a CSV file with the following columns:
   - `Product Name`
   - `Product ID` (required)
   - `Price`
   - `Description`
2. Upload the file, and select options below to generate barcodes.
""")

# File upload
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

# Checkbox for textless barcode option
textless_option = st.checkbox("Generate Textless Barcodes (Hide Text Underneath)")

# Process file and generate barcodes
if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)
        st.write("### Uploaded Product Data")
        st.dataframe(df)  # Display uploaded data

        # Check for required column
        if 'Product ID' not in df.columns:
            st.error("The CSV file must include a 'Product ID' column.")
        else:
            # Generate barcodes
            st.write("### Generated Barcodes")
            for index, row in df.iterrows():
                product_name = row.get("Product Name", "Unknown Product")
                product_id = str(row["Product ID"])  # Product ID is required
                price = row.get("Price", "N/A")
                description = row.get("Description", "")

                # Generate barcode
                barcode_image = generate_barcode(product_id, textless=textless_option)
                
                # Display barcode and product details
                st.image(barcode_image, caption=f"Barcode for {product_name} (ID: {product_id})", use_column_width=True)
                st.text(f"Product Name: {product_name}")
                st.text(f"Product ID: {product_id}")
                st.text(f"Price: {price}")
                st.text(f"Description: {description}")
                st.markdown("---")  # Separator between products

    except Exception as e:
        st.error(f"An error occurred: {e}")

# User information
st.markdown("### Made by:")
st.write(
    "Name: Rigved Sarougi",
    "Email: irigved2000@gmail.com",
    "LinkedIn: [Rigved Sarougi](https://www.linkedin.com/in/rigved-sarougi/)"
)
