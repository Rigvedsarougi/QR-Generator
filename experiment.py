import streamlit as st
import pandas as pd
import zipfile
import io
from barcode import Code128
from barcode.writer import ImageWriter

# Function to generate a barcode for a product ID
def generate_barcode(product_id, textless=False):
    barcode = Code128(product_id, writer=ImageWriter())
    img_byte_arr = io.BytesIO()
    options = {"write_text": not textless}  # Hide text if textless=True
    barcode.write(img_byte_arr, options=options)
    return img_byte_arr.getvalue()

# Function to generate barcodes for multiple products and create a ZIP file
def generate_barcodes_zip(dataframe, textless=False):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for index, row in dataframe.iterrows():
            product_id = str(row["Product ID"])
            product_name = row["Product Name"]
            barcode_image = generate_barcode(product_id, textless)
            
            # Generate a file name for the barcode
            filename = f"{product_name}_{product_id}.png"
            zipf.writestr(filename, barcode_image)
    return zip_buffer

# Streamlit UI
st.title("Bulk Product Barcode Generator")

# Instructions for the user
st.write("""
### Instructions:
1. Upload an **Excel file** with the following columns:
   - `Product Name`
   - `Product ID` (unique identifier)
   - `Price` (optional)
   - `Description` (optional)
2. Ensure the column names are correct.
3. Click the **Generate Barcodes** button to download a ZIP file containing all product barcodes.
""")

# Example Excel template for download
example_data = {
    "Product Name": ["Product A", "Product B", "Product C"],
    "Product ID": ["12345", "67890", "11223"],
    "Price": ["100", "150", "200"],
    "Description": ["Sample Product A", "Sample Product B", "Sample Product C"]
}
example_df = pd.DataFrame(example_data)
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    example_df.to_excel(writer, index=False, sheet_name="Products")
st.download_button(
    label="Download Excel Template",
    data=excel_buffer.getvalue(),
    file_name="product_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# File upload section
uploaded_file = st.file_uploader("Upload your Excel file here", type=["xlsx"])

# Option for textless barcodes
textless_option = st.checkbox("Generate Textless Barcodes (Hide Text Underneath)")

# Generate and download barcodes
if st.button("Generate Barcodes"):
    if uploaded_file:
        # Load Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)
        
        # Validate required columns
        required_columns = ["Product Name", "Product ID"]
        if all(column in df.columns for column in required_columns):
            # Generate ZIP file with barcodes
            zip_buffer = generate_barcodes_zip(df, textless_option)
            
            # Provide ZIP file download
            st.success("Barcodes generated successfully!")
            st.download_button(
                label="Download All Barcodes (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="product_barcodes.zip",
                mime="application/zip"
            )
        else:
            st.error(f"Your Excel file must contain the following columns: {', '.join(required_columns)}")
    else:
        st.warning("Please upload a valid Excel file.")
