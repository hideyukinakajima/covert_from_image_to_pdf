#!/usr/bin/env python3
"""
Image to PDF Converter
イメージファイルをPDFに変換するアプリケーション
"""

import os
import sys
import argparse
from PIL import Image
from pathlib import Path

def convert_images_to_pdf(image_paths, output_path):
    """
    複数のイメージファイルを1つのPDFに変換
    
    Args:
        image_paths (list): イメージファイルのパスのリスト
        output_path (str): 出力PDFファイルのパス
    """
    if not image_paths:
        print("エラー: イメージファイルが指定されていません")
        return False
    
    try:
        # 最初の画像を開く
        first_image = Image.open(image_paths[0])
        
        # RGBモードに変換（PDFではRGBが必要）
        if first_image.mode != 'RGB':
            first_image = first_image.convert('RGB')
        
        # 他の画像があるかチェック
        if len(image_paths) > 1:
            other_images = []
            for img_path in image_paths[1:]:
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                other_images.append(img)
            
            # 複数画像をPDFとして保存
            first_image.save(
                output_path,
                "PDF",
                save_all=True,
                append_images=other_images
            )
        else:
            # 単一画像をPDFとして保存
            first_image.save(output_path, "PDF")
        
        print(f"成功: PDFを作成しました - {output_path}")
        return True
        
    except Exception as e:
        print(f"エラー: PDF変換に失敗しました - {e}")
        return False

def get_supported_image_files(directory):
    """
    指定されたディレクトリからサポートされているイメージファイルを取得
    
    Args:
        directory (str): ディレクトリパス
        
    Returns:
        list: イメージファイルのパスのリスト
    """
    supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    image_files = []
    
    path = Path(directory)
    if path.is_dir():
        for file_path in path.iterdir():
            if file_path.suffix.lower() in supported_extensions:
                image_files.append(str(file_path))
    
    return sorted(image_files)

def main():
    parser = argparse.ArgumentParser(
        description='イメージファイルをPDFに変換するツール',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 単一のイメージをPDFに変換
  python image_to_pdf_converter.py image.jpg -o output.pdf
  
  # 複数のイメージを1つのPDFに変換
  python image_to_pdf_converter.py image1.jpg image2.png image3.jpg -o combined.pdf
  
  # ディレクトリ内の全イメージをPDFに変換
  python image_to_pdf_converter.py -d /path/to/images -o all_images.pdf
        """
    )
    
    # 引数設定
    parser.add_argument(
        'images',
        nargs='*',
        help='変換するイメージファイルのパス'
    )
    parser.add_argument(
        '-d', '--directory',
        help='イメージファイルが含まれるディレクトリのパス'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='出力PDFファイルのパス'
    )
    
    args = parser.parse_args()
    
    # イメージファイルのリストを取得
    if args.directory:
        image_paths = get_supported_image_files(args.directory)
        if not image_paths:
            print(f"エラー: ディレクトリ '{args.directory}' にサポートされているイメージファイルが見つかりません")
            return 1
    elif args.images:
        image_paths = args.images
    else:
        print("エラー: イメージファイルまたはディレクトリを指定してください")
        return 1
    
    # ファイルの存在確認
    for img_path in image_paths:
        if not os.path.exists(img_path):
            print(f"エラー: ファイルが見つかりません - {img_path}")
            return 1
    
    # PDF変換実行
    success = convert_images_to_pdf(image_paths, args.output)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())