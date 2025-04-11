import easyocr
import cv2

# Inisialisasi EasyOCR reader (pakai English dulu)
reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_path):
    """
    Fungsi untuk ekstrak teks dari gambar menggunakan EasyOCR.
    """
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result)