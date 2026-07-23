# extract_images.py - 从 PDF 提取图片（内嵌图 + 扫描件区域渲染）
# 用法: python extract_images.py <pdf_path> <output_dir> [page_ranges]
# page_ranges 格式: "1,3:5" 表示第1页和第3-5页（1-based）
import fitz  # PyMuPDF
import os, sys

def extract_embedded_images(pdf_path, output_dir):
    """抽取内嵌图片（适用于数字版 PDF）"""
    doc = fitz.open(pdf_path)
    count = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        for img_idx, img in enumerate(images):
            xref = img[0]
            base = doc.extract_image(xref)
            ext = base["ext"]
            img_bytes = base["image"]
            fname = f"page{page_num+1}_img{img_idx+1}.{ext}"
            with open(os.path.join(output_dir, fname), "wb") as f:
                f.write(img_bytes)
            count += 1
    doc.close()
    return count

def render_full_pages(pdf_path, output_dir, dpi=200):
    """整页渲染为 PNG（扫描件回退方案）"""
    doc = fitz.open(pdf_path)
    count = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        mat = fitz.Matrix(dpi/72, dpi/72)
        pix = page.get_pixmap(matrix=mat)
        fname = f"page{page_num+1}.png"
        pix.save(os.path.join(output_dir, fname))
        count += 1
    doc.close()
    return count

def render_region(pdf_path, output_dir, page_num, x0, y0, x1, y1, dpi=300, name="region"):
    """按区域渲染裁剪（坐标为页面比例 0-1）"""
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    rect = page.rect
    clip = fitz.Rect(rect.width * x0, rect.height * y0, rect.width * x1, rect.height * y1)
    mat = fitz.Matrix(dpi/72, dpi/72)
    pix = page.get_pixmap(matrix=mat, clip=clip)
    pix.save(os.path.join(output_dir, f"{name}.png"))
    doc.close()
    return 1

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)
    embedded = extract_embedded_images(pdf_path, output_dir)
    print(f"内嵌图片: {embedded} 张")
    if embedded == 0:
        n = render_full_pages(pdf_path, output_dir)
        print(f"扫描件整页渲染: {n} 张 (回退方案)")
