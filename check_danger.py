import cv2
import pytesseract


OCR_CONFIG = r"-l ukr --oem 3 --psm 6"
DANGER_WORDS = ("тривога", "сирена", "укриття")
SAFE_WORDS = ("відбій",)


def check_text_is_danger(text: str) -> bool:
    text = " ".join(text.lower().split())
    if any(danger_word in text for danger_word in DANGER_WORDS) and not any(
        safe_word in text for safe_word in SAFE_WORDS
    ):
        return True
    return False


def check_image_is_danger(image_path: str) -> bool:
    image_text = ocr(image_path)
    return check_text_is_danger(image_text)


def ocr(image_path):
    img = cv2.imread(image_path)
    return pytesseract.image_to_string(img, config=OCR_CONFIG)


def main():
    print("here")


if __name__ == "__main__":
    print(ocr("danger.jpg"))
