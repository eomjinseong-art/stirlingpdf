from flask import Flask, request, send_file, render_template_string
from pypdf import PdfMerger, PdfReader, PdfWriter
import os

app = Flask(__name__)

# 간단한 업로드 폼 페이지 (테스트용)
@app.route('/')
def home():
    return "Lightweight PDF API Server is Running!"

# 1. PDF 합치기 API
@app.route('/merge', methods=['POST'])
def merge_pdfs():
    if 'files' not in request.files:
        return "No files provided", 400
    
    files = request.files.getlist('files')
    merger = PdfMerger()
    
    try:
        for file in files:
            merger.append(file)
        
        output_path = "/tmp/merged.pdf"
        merger.write(output_path)
        merger.close()
        
        return send_file(output_path, as_attachment=True, download_name="merged.pdf")
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)