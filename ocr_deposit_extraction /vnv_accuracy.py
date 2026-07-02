from ocr_deposit_extraction import extract_amount

test_data = {
    "images.jpeg": "1000.00",
    "rtaImage.jpg": "60.00"
}

correct = 0
total = len(test_data)

for img, expected in test_data.items():
    result = extract_amount(img)

    print(f"{img} → Expected: {expected}, Got: {result}")

    if expected in result:
        print("✔ PASS\n")
        correct += 1
    else:
        print("❌ FAIL\n")

accuracy = (correct / total) * 100
print("FINAL ACCURACY:", accuracy, "%")