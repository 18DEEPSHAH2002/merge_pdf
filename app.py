# app.py
# Universal File Converter & PDF Toolkit (Single File)

import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
from PIL import Image
import tempfile
import os
import zipfile

# Optional tools (install if needed)
# pip install pdf2image pytesseract python-docx openpyxl
try:
    from pdf2image import convert_from_bytes
except:
    convert_from_bytes = None

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Universal File Converter",
    page_icon="📁",
    layout="wide"
)

st.title("📁 Universal File Converter & PDF Toolkit")
st.caption("All-in-one PDF, Word, Excel, CSV & Image tools")

# ---------------------------------------------------
# TOOL SELECTOR
# ---------------------------------------------------
tool = st.selectbox(
    "Select Function",
    [
        "Merge PDFs",
        "Split PDF",
        "Compress PDF",
        "Image → PDF",
        "PDF → Image",
        "CSV → Excel",
        "Excel → CSV",
        "JPG → PNG",
        "PNG → JPG"
    ]
)

st.divider()

# ---------------------------------------------------
# MERGE PDFs
# ---------------------------------------------------
if tool == "Merge PDFs":
    st.subheader("🔗 Merge PDFs")

    files = st.file_uploader(
        "Upload PDF files (max 20)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if files and st.button("Merge PDFs"):
        writer = PdfWriter()
        temp_dir = tempfile.mkdtemp()

        for file in files:
            path = os.path.join(temp_dir, file.name)
            with open(path, "wb") as f:
                f.write(file.read())

            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)

        output = os.path.join(temp_dir, "merged.pdf")
        with open(output, "wb") as f:
            writer.write(f)

        with open(output, "rb") as f:
            st.download_button(
                "⬇ Download Merged PDF",
                f,
                file_name="merged.pdf",
                mime="application/pdf"
            )

# ---------------------------------------------------
# SPLIT PDF
# ---------------------------------------------------
elif tool == "Split PDF":
    st.subheader("✂ Split PDF")

    pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if pdf and st.button("Split"):
        reader = PdfReader(pdf)
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "split_pages.zip")

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)

                page_path = os.path.join(temp_dir, f"page_{i+1}.pdf")
                with open(page_path, "wb") as f:
                    writer.write(f)

                zipf.write(page_path, arcname=f"page_{i+1}.pdf")

        with open(zip_path, "rb") as f:
            st.download_button(
                "⬇ Download ZIP",
                f,
                file_name="split_pages.zip"
            )

# ---------------------------------------------------
# COMPRESS PDF (basic)
# ---------------------------------------------------
elif tool == "Compress PDF":
    st.subheader("📉 Compress PDF")

    pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if pdf and st.button("Compress"):
        reader = PdfReader(pdf)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        with open(temp_path, "wb") as f:
            writer.write(f)

        with open(temp_path, "rb") as f:
            st.download_button(
                "⬇ Download Compressed PDF",
                f,
                file_name="compressed.pdf"
            )

# ---------------------------------------------------
# IMAGE → PDF
# ---------------------------------------------------
elif tool == "Image → PDF":
    st.subheader("🖼 Image to PDF")

    images = st.file_uploader(
        "Upload Images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if images and st.button("Convert"):
        img_list = [Image.open(img).convert("RGB") for img in images]

        output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        img_list[0].save(output, save_all=True, append_images=img_list[1:])

        with open(output, "rb") as f:
            st.download_button(
                "⬇ Download PDF",
                f,
                file_name="images.pdf"
            )

# ---------------------------------------------------
# PDF → IMAGE
# ---------------------------------------------------
elif tool == "PDF → Image":
    st.subheader("📄 PDF to Images")

    if convert_from_bytes is None:
        st.error("pdf2image not installed")
    else:
        pdf = st.file_uploader("Upload PDF", type=["pdf"])

        if pdf and st.button("Convert"):
            images = convert_from_bytes(pdf.read())
            temp_dir = tempfile.mkdtemp()

            zip_path = os.path.join(temp_dir, "images.zip")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for i, img in enumerate(images):
                    img_path = os.path.join(temp_dir, f"page_{i+1}.png")
                    img.save(img_path)
                    zipf.write(img_path, arcname=f"page_{i+1}.png")

            with open(zip_path, "rb") as f:
                st.download_button(
                    "⬇ Download Images ZIP",
                    f,
                    file_name="pdf_images.zip"
                )

# ---------------------------------------------------
# CSV → EXCEL
# ---------------------------------------------------
elif tool == "CSV → Excel":
    st.subheader("📊 CSV to Excel")

    csv = st.file_uploader("Upload CSV", type=["csv"])

    if csv and st.button("Convert"):
        df = pd.read_csv(csv)
        path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
        df.to_excel(path, index=False)

        with open(path, "rb") as f:
            st.download_button(
                "⬇ Download Excel",
                f,
                file_name="converted.xlsx"
            )

# ---------------------------------------------------
# EXCEL → CSV
# ---------------------------------------------------
elif tool == "Excel → CSV":
    st.subheader("📊 Excel to CSV")

    excel = st.file_uploader("Upload Excel", type=["xlsx"])

    if excel and st.button("Convert"):
        df = pd.read_excel(excel)
        path = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name
        df.to_csv(path, index=False)

        with open(path, "rb") as f:
            st.download_button(
                "⬇ Download CSV",
                f,
                file_name="converted.csv"
            )

# ---------------------------------------------------
# IMAGE FORMAT CONVERSION
# ---------------------------------------------------
elif tool in ["JPG → PNG", "PNG → JPG"]:
    st.subheader("🖼 Image Format Converter")

    img = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if img and st.button("Convert"):
        image = Image.open(img)
        fmt = "PNG" if "PNG" in tool else "JPEG"
        ext = ".png" if fmt == "PNG" else ".jpg"

        output = tempfile.NamedTemporaryFile(delete=False, suffix=ext).name
        image.save(output, fmt)

        with open(output, "rb") as f:
            st.download_button(
                "⬇ Download Image",
                f,
                file_name="converted" + ext
            )

st.divider()
st.success("✅ Ready | Single-file All-in-One Converter")
