import cv2
import numpy as np

def remove_background(image_path, bg_color):
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"이미지를 로드할 수 없습니다. 경로: {image_path}")
            return None

        original = image.copy()
        mask = np.zeros(image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        height, width = image.shape[:2]
        rect = (10, 10, width - 20, height - 20)

        cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")

        result = cv2.cvtColor(original, cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = mask2 * 255

        colored_background = np.zeros_like(result, dtype=np.uint8)
        colored_background[:, :, :3] = bg_color
        colored_background[:, :, 3] = 255

        final_image = np.where(mask2[:, :, None] == 1, result, colored_background)
        return final_image
    except Exception as e:
        print(f"배경 제거 중 오류 발생: {e}")
        return None
