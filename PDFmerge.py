import streamlit as st
from PyPDF2 import PdfMerger
import os
import tempfile

st.set_page_config(page_title="PDFマージアプリ", layout="centered")
st.title("📂 フォルダごとPDFをアップロードして結合")

uploaded_files = st.file_uploader(
    "📁 結合したいPDFファイルを**複数選択**してアップロードしてください。",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("🚀 PDFをマージする"):
        with tempfile.TemporaryDirectory() as tmpdirname:
            merger = PdfMerger()
            temp_paths = []

            # 一時フォルダに保存し、ファイル名順にソート
            for file in uploaded_files:
                temp_path = os.path.join(tmpdirname, file.name)
                with open(temp_path, "wb") as f:
                    f.write(file.read())
                temp_paths.append(temp_path)

            for path in sorted(temp_paths):  # ファイル名順にマージ
                merger.append(path)

            merged_path = os.path.join(tmpdirname, "merged_output.pdf")
            merger.write(merged_path)
            merger.close()

            with open(merged_path, "rb") as f:
                st.download_button(
                    label="⬇️ マージ済みPDFをダウンロード",
                    data=f,
                    file_name="merged_output.pdf",
                    mime="application/pdf"
                )