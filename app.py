import streamlit as st
from pypdf import PdfMerger
import tempfile
import os

st.set_page_config(page_title="PDF Merger", page_icon="📄")

st.title("📄 High-Quality PDF Merger")
st.write("Upload up to 20 PDFs and merge them into one high-quality PDF.")

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 20:
        st.error("You can upload a maximum of 20 PDFs.")
    else:
        st.success(f"{len(uploaded_files)} PDFs uploaded.")

        # Reorder PDFs
        filenames = [file.name for file in uploaded_files]
        selected_order = st.multiselect(
            "Select PDF order (top → bottom)",
            filenames,
            default=filenames
        )

        if len(selected_order) != len(uploaded_files):
            st.warning("Please select all PDFs to continue.")
        else:
            if st.button("🔗 Merge PDFs"):
                merger = PdfMerger()

                temp_dir = tempfile.mkdtemp()
                file_map = {}

                # Save uploaded PDFs temporarily
                for file in uploaded_files:
                    temp_path = os.path.join(temp_dir, file.name)
                    with open(temp_path, "wb") as f:
                        f.write(file.read())
                    file_map[file.name] = temp_path

                # Merge in selected order
                for name in selected_order:
                    merger.append(file_map[name])

                output_path = os.path.join(temp_dir, "merged.pdf")
                merger.write(output_path)
                merger.close()

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Merged PDF",
                        data=f,
                        file_name="merged.pdf",
                        mime="application/pdf"
                    )

                st.success("PDFs merged successfully!")
