"""
Landing AI – OCR lấy Markdown
==============================
Cài đặt:
  pip install landingai-ade python-dotenv

.env:
  VISION_AGENT_API_KEY=land_sk_xxxxxxxxxxxxxxxxxxxxxxxx
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from landingai_ade import LandingAIADE

load_dotenv()

client = LandingAIADE(apikey=os.environ.get("VISION_AGENT_API_KEY"))

# ==============================================================================
# CẤU HÌNH ĐẦU VÀO / ĐẦU RA 
# ==============================================================================
# 1. Thư mục chứa các file PDF gốc (Đầu vào: File .pdf)
PDF_DIR = Path("./data/01_raw_pdf")

# 2. Thư mục lưu kết quả Markdown sau khi OCR (Đầu ra: File .md)
OUTPUT_DIR = Path("./data/02_ocr_markdown")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Danh sách các file cần chạy (Để rỗng [] nếu muốn tự động chạy tất cả file trong PDF_DIR)
PDF_FILES = []

def get_pdf_files():
    if PDF_FILES:
        return PDF_FILES
    if not PDF_DIR.exists():
        PDF_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[*] Đã tạo thư mục đầu vào: {PDF_DIR}. Vui lòng copy file PDF vào đây!")
        return []
    return [f.name for f in PDF_DIR.glob("*.pdf")]


def ocr_pdf(pdf_path: Path) -> None:
    print(f"\n[OCR] {pdf_path.name}")
    print("  processing...", end=" ", flush=True)

    result = client.parse(document=pdf_path, model="dpt-2-latest")
    print(f"{len(result.chunks)} chunks")

    out_md = OUTPUT_DIR / f"{pdf_path.stem}_ocr.md"
    out_md.write_text(result.markdown, encoding="utf-8")
    print(f"  saved → {out_md.name}")


def main():
    print("━" * 50)
    print("  Landing AI OCR")
    print("━" * 50)
    
    files_to_process = get_pdf_files()
    if not files_to_process:
        print("\n  ✗ Không có file PDF nào để xử lý.")
        return

    for name in files_to_process:
        path = PDF_DIR / name
        if not path.exists():
            print(f"\n  ✗ not found: {name}")
            continue
        try:
            ocr_pdf(path)
        except Exception:
            import traceback; traceback.print_exc()
    print("\n" + "━" * 50)
    print("  done —", OUTPUT_DIR)
    print("━" * 50)


if __name__ == "__main__":
    main()
