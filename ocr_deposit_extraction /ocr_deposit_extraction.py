import re
import cv2
import easyocr
import pytesseract

reader = easyocr.Reader(['en'])

AMOUNT_LABELS = ("jumlah", "amount", "ahount", "amaun", "nount")

MONEY_RE = re.compile(r'\d[\d,]*\.\d{2}')


def _box(bbox):
    xs = [p[0] for p in bbox]
    ys = [p[1] for p in bbox]
    return min(xs), max(xs), min(ys), max(ys)


def _find_amount_box(results):
    label = None
    for bbox, text, _conf in results:
        if any(word in text.lower() for word in AMOUNT_LABELS):
            label = _box(bbox)
            break
    if label is None:
        return None

    lx0, lx1, _ly0, ly1 = label
    candidates = []
    for bbox, _text, _conf in results:
        b = _box(bbox)
        x_overlap = min(lx1, b[1]) - max(lx0, b[0])
        if b[2] >= ly1 - 4 and x_overlap > 0:
            candidates.append((b[2], b))

    if not candidates:
        return None
    return candidates[0][1]


def _read_cell(gray, box):
    x0, x1, y0, y1 = (int(v) for v in box)
    pad = 4
    crop = gray[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad]
    config = '--psm 7 -c tessedit_char_whitelist=0123456789.,RM'
    for scale in (4, 5, 3, 6):
        big = cv2.resize(crop, None, fx=scale, fy=scale,
                         interpolation=cv2.INTER_CUBIC)
        text = pytesseract.image_to_string(big, config=config)
        match = MONEY_RE.search(text)
        if match:
            return float(match.group(0).replace(',', ''))
    return None


def extract_amount(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return "Image not found"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    results = reader.readtext(gray)

    print("DEBUG OCR TEXT:", " ".join(t[1] for t in results))

    box = _find_amount_box(results)
    if box is not None:
        amount = _read_cell(gray, box)
        if amount is not None:
            return f"{amount:.2f}"

    text = pytesseract.image_to_string(gray)
    rm = re.search(r'RM\s*([\d,]+\.\d{2})', text, re.IGNORECASE)
    if rm:
        return f"{float(rm.group(1).replace(',', '')):.2f}"

    return "Not Found"


if __name__ == "__main__":
    print("Extracted Deposit:", extract_amount("images.jpeg"))
