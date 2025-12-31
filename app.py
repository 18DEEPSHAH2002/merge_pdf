import streamlit as st
from pypdf import PdfReader, PdfWriter
import tempfile
import os

st.set_page_config(page_title="PDF Merger", page_icon="📄")

st.title("📄 High-Quality PDF Merger")
st.write("Upload up to 20 PDFs and merge them without quality loss.")

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 20:
        st.error("Maximum 20 PDFs allowed.")
    else:
        filenames = [file.name for file in uploaded_files]

        order = st.multiselect(
            "Select PDF order (top → bottom)",
            filenames,
            default=filenames
        )

        if len(order) != len(filenames):
            st.warning("Please select all PDFs.")
        else:
            if st.button("🔗 Merge PDFs"):
                writer = PdfWriter()
                temp_dir = tempfile.mkdtemp()
                file_map = {}

                # Save uploaded files
                for file in uploaded_files:
                    path = os.path.join(temp_dir, file.name)
                    with open(path, "wb") as f:
                        f.write(file.read())
                    file_map[file.name] = path

                # Merge PDFs
                for name in order:
                    reader = PdfReader(file_map[name])
                    for page in reader.pages:
                        writer.add_page(page)

                output_path = os.path.join(temp_dir, "merged.pdf")
                with open(output_path, "wb") as f:
                    writer.write(f)

                with open(output_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download Merged PDF",
                        f,
                        file_name="merged.pdf",
                        mime="application/pdf"
                    )

                st.success("PDFs merged successfully 🎉")
