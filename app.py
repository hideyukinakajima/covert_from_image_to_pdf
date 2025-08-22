#!/usr/bin/env python3
"""
Image to PDF Converter - Web Application
ブラウザで動作するイメージからPDF変換アプリケーション
"""

import os
import uuid
from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import tempfile
import zipfile

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB制限

def allowed_file(filename):
    """アップロードファイルの拡張子をチェック"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_images_to_pdf(image_paths, output_path):
    """複数のイメージファイルを1つのPDFに変換"""
    try:
        if not image_paths:
            return False, "エラー: イメージファイルが指定されていません"
        
        first_image = Image.open(image_paths[0])
        if first_image.mode != 'RGB':
            first_image = first_image.convert('RGB')
        
        if len(image_paths) > 1:
            other_images = []
            for img_path in image_paths[1:]:
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                other_images.append(img)
            
            first_image.save(
                output_path,
                "PDF",
                save_all=True,
                append_images=other_images
            )
        else:
            first_image.save(output_path, "PDF")
        
        return True, "PDFの変換が成功しました"
        
    except Exception as e:
        return False, f"PDF変換エラー: {str(e)}"

@app.route('/')
def index():
    """メインページを表示"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """ファイルアップロードとPDF変換処理"""
    if 'files' not in request.files:
        flash('ファイルが選択されていません')
        return redirect(request.url)
    
    files = request.files.getlist('files')
    
    if not files or all(file.filename == '' for file in files):
        flash('ファイルが選択されていません')
        return redirect(url_for('index'))
    
    uploaded_files = []
    session_id = str(uuid.uuid4())
    
    # ファイルをアップロードして保存
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{session_id}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            uploaded_files.append(file_path)
        else:
            flash(f'サポートされていないファイル形式: {file.filename}')
    
    if not uploaded_files:
        flash('有効なイメージファイルがありません')
        return redirect(url_for('index'))
    
    # PDF変換
    output_filename = f"{session_id}_converted.pdf"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    
    success, message = convert_images_to_pdf(uploaded_files, output_path)
    
    # アップロードされたファイルを削除
    for file_path in uploaded_files:
        try:
            os.remove(file_path)
        except:
            pass
    
    if success:
        flash(message)
        return send_file(output_path, as_attachment=True, download_name='converted_images.pdf')
    else:
        flash(message)
        return redirect(url_for('index'))

@app.route('/cleanup')
def cleanup():
    """古いファイルをクリーンアップ"""
    try:
        for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        return "クリーンアップが完了しました"
    except Exception as e:
        return f"クリーンアップエラー: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)