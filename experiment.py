import streamlit as st
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
import io
from fpdf import FPDF
import zipfile
import base64

# Function to generate a barcode for a single product
def generate_barcode(product_id, textless=False):
    barcode = Code128(product_id, writer=ImageWriter())
    img_byte_arr = io.BytesIO()
    options = {"write_text": not textless}
    barcode.write(img_byte_arr, options=options)
    return img_byte_arr.getvalue()

# Function to create a PDF with barcodes
def generate_pdf(barcode_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for product in barcode_data:
        product_name, product_id, barcode_img = product
        # Add product details to the PDF
        pdf.cell(200, 10, txt=f"Product: {product_name}, ID: {product_id}", ln=True)
        pdf.ln(2)
        
        # Add barcode image
        img_path = f"barcode_{product_id}.png"
        with open(img_path, "wb") as f:
            f.write(barcode_img)
        pdf.image(img_path, x=10, y=pdf.get_y(), w=80, h=20)
        pdf.ln(25)  # Space after each barcode

    # Save PDF to bytes
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()

# Function to create a ZIP file of barcode images
def generate_zip(barcode_data):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for product in barcode_data:
            product_name, product_id, barcode_img = product
            img_filename = f"{product_name}_{product_id}.png"
            zip_file.writestr(img_filename, barcode_img)
    return zip_buffer.getvalue()

# Streamlit UI
st.title("Bulk Product Barcode Generator with PDF/CSV Download")

# File upload
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

# Checkbox for textless barcode option
textless_option = st.checkbox("Generate Textless Barcodes (Hide Text Underneath)")

# Option for output format
output_format = st.radio("Select Output Format", ["PDF", "ZIP"])

# Generate barcodes on button click
if uploaded_file is not None:
    try:
        # Read uploaded CSV
        df = pd.read_csv(uploaded_file)
        st.write("### Uploaded Product Data")
        st.dataframe(df)

        # Check for required 'Product ID' column
        if 'Product ID' not in df.columns:
            st.error("The CSV file must include a 'Product ID' column.")
        else:
            barcode_data = []

            # Generate barcodes and collect details
            for _, row in df.iterrows():
                product_name = row.get("Product Name", "Unknown Product")
                product_id = str(row["Product ID"])
                barcode_img = generate_barcode(product_id, textless=textless_option)
                barcode_data.append((product_name, product_id, barcode_img))

            # Output: PDF or ZIP
            if output_format == "PDF":
                st.success("Generating PDF...")
                pdf_file = generate_pdf(barcode_data)
                st.download_button(
                    label="Download Barcodes as PDF",
                    data=pdf_file,
                    file_name="barcodes.pdf",
                    mime="application/pdf"
                )
            elif output_format == "ZIP":
                st.success("Generating ZIP File...")
                zip_file = generate_zip(barcode_data)
                st.download_button(
                    label="Download Barcodes as ZIP",
                    data=zip_file,
                    file_name="barcodes.zip",
                    mime="application/zip"
                )

    except Exception as e:
        st.error(f"An error occurred: {e}")

# User information
st.markdown("### Made by:")
st.write(
    "Name: Rigved Sarougi",
    "Email: irigved2000@gmail.com",
    "LinkedIn: [Rigved Sarougi](https://www.linkedin.com/in/rigved-sarougi/)"
)
