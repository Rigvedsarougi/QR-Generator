import streamlit as st
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
import io
import zipfile
import os

# Function to generate a barcode for a single product
def generate_barcode(product_id, textless=False):
    # Generate barcode using Code128 with customized options
    barcode = Code128(product_id, writer=ImageWriter())
    img_byte_arr = io.BytesIO()

    # Customize barcode options
    options = {
        "write_text": not textless,  # Show or hide text
        "text_distance": 2,  # Distance between text and barcode lines
        "font_size": 10,  # Adjust text size
        "module_height": 15,  # Adjust barcode height
        "module_width": 0.2,  # Adjust barcode width
    }

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
            # Create a temporary directory to save barcode images
            temp_dir = "barcodes"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Generate barcodes and save images
            st.write("### Generating Barcodes...")

            for index, row in df.iterrows():
                product_name = row.get("Product Name", "Unknown Product")
                product_id = str(row["Product ID"])  # Product ID is required
                price = row.get("Price", "N/A")
                description = row.get("Description", "")

                # Generate barcode
                barcode_image = generate_barcode(product_id, textless=textless_option)

                # Save barcode image to the temporary directory
                barcode_filename = f"{temp_dir}/{product_id}.png"
                with open(barcode_filename, "wb") as f:
                    f.write(barcode_image)

            # Create a ZIP file containing all the images
            zip_filename = "barcodes.zip"
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for file in os.listdir(temp_dir):
                    zipf.write(os.path.join(temp_dir, file), arcname=file)

            # Provide the ZIP file for download
            with open(zip_filename, "rb") as f:
                st.download_button(
                    label="Download Barcodes ZIP",
                    data=f,
                    file_name=zip_filename,
                    mime="application/zip"
                )

            # Clean up the temporary directory and ZIP file
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
            os.remove(zip_filename)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# User information
st.markdown("### Made by:")
st.write(
    "Name: Rigved Sarougi",
    "Email: irigved2000@gmail.com",
    "LinkedIn: [Rigved Sarougi](https://www.linkedin.com/in/rigved-sarougi/)"
)
