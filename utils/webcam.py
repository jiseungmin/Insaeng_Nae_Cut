import subprocess

def capture_image(image_path):
    try:
        command = f"fswebcam -r 1280x960 --no-banner {image_path}"
        subprocess.run(command, shell=True, check=True)
        print(f"사진이 저장되었습니다: {image_path}")
    except subprocess.CalledProcessError as e:
        print(f"캡처 중 오류 발생: {e}")
