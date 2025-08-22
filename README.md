# Image to PDF Converter

イメージファイルをPDFに変換するPythonアプリケーション

## 機能
- 単一または複数のイメージファイルを1つのPDFに変換
- サポートファイル形式: JPG, JPEG, PNG, BMP, TIFF
- ディレクトリ内の全イメージを一括変換
- コマンドライン操作

## セットアップ
```bash
pip install -r requirements_image_to_pdf.txt
```

## 使用方法

### 単一イメージの変換
```bash
python image_to_pdf_converter.py image.jpg -o output.pdf
```

### 複数イメージを1つのPDFに結合
```bash
python image_to_pdf_converter.py image1.jpg image2.png image3.jpg -o combined.pdf
```

### ディレクトリ内の全イメージを変換
```bash
python image_to_pdf_converter.py -d /path/to/images -o all_images.pdf
```

## オプション
- `-d, --directory`: イメージファイルが含まれるディレクトリのパス
- `-o, --output`: 出力PDFファイルのパス（必須）
- `-h, --help`: ヘルプを表示