from flask import Flask, request, send_file
from pypdf import PdfMerger
import os

app = Flask(__name__)

# 파일 업로드 임시 경로
UPLOAD_FOLDER = '/tmp'

@app.route('/')
def home():
    return "Lightweight PDF API Server is Running!"

# PDF 합치기 API
@app.route('/merge', methods=['POST'])
def merge_pdfs():
    # 요청에서 파일 리스트 가져오기
    if 'files' not in request.files:
        return "No files provided", 400
    
    files = request.files.getlist('files')
    merger = PdfMerger()
    
    try:
        # 파일 합치기
        for file in files:
            merger.append(file)
        
        # 합쳐진 파일 저장 경로
        output_path = os.path.join(UPLOAD_FOLDER, "merged.pdf")
        merger.write(output_path)
        merger.close()
        
        # 클라이언트로 결과 파일 전송
        return send_file(output_path, as_attachment=True, download_name="merged.pdf")
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)