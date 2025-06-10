import streamlit as st
from PyPDF2 import PdfMerger
import os
import tempfile

st.set_page_config(page_title="PDFマージアプリ", layout="centered")
st.title("📂 フォルダごとPDFをアップロードして結合")

# セッションステートでファイル管理
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

uploaded = st.file_uploader(
    "📁 結合したいPDFファイルを**複数選択**してアップロードしてください。",
    type=["pdf"],
    accept_multiple_files=True,
    key="file_uploader"
)

if uploaded:
    st.session_state.uploaded_files = uploaded

if st.session_state.uploaded_files:
    if st.button("🚀 PDFをマージする"):
        with tempfile.TemporaryDirectory() as tmpdirname:
            merger = PdfMerger()
            temp_paths = []

            # 一時フォルダに保存し、ファイル名順にマージ
            for file in st.session_state.uploaded_files:
                temp_path = os.path.join(tmpdirname, file.name)
                with open(temp_path, "wb") as f:
                    f.write(file.read())
                temp_paths.append(temp_path)

            for path in sorted(temp_paths):
                merger.append(path)

            merged_path = os.path.join(tmpdirname, "merged_output.pdf")
            merger.write(merged_path)
            merger.close()

            with open(merged_path, "rb") as f:
                st.download_button(
                    label="⬇️ マージ済みPDFをダウンロード",
                    data=f.read(),
                    file_name="merged_output.pdf",
                    mime="application/pdf",
                    on_click=lambda: st.session_state.clear()  # ← 状態リセット
                )
