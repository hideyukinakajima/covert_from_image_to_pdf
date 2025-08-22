import streamlit as st
import os
from PIL import Image
import io

st.title("Image to PDF Converter")
st.write("イメージファイルをPDFに変換するPythonアプリケーション")

uploaded_file = st.file_uploader("画像を選択してください", type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='アップロードされた画像', use_column_width=True)
    
    if st.button('PDFに変換'):
        # PDF変換処理
        pdf_bytes = io.BytesIO()
        image.convert('RGB').save(pdf_bytes, format='PDF')
        pdf_bytes.seek(0)
        
        st.download_button(
            label="PDFをダウンロード",
            data=pdf_bytes,
            file_name="converted.pdf",
            mime="application/pdf"
        )
