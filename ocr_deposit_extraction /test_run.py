from ocr_deposit_extraction import extract_amount

test_images = [
    "images.jpeg",
    "rtaImage.jpg"
]

for img in test_images:
    print("Image:", img)
    print("Extracted:", extract_amount(img))
    print("----------------------")