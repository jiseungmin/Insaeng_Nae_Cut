from PIL import Image

# 인생네컷 프레임 이미지 파일 경로
background_path = "./assets/insaeng_frame.png"  
background = Image.open(background_path)

positions = [
    (37, 69, 510, 320),   
    (37, 405, 510, 320),  
    (37, 740, 510, 320),  
    (37, 1075, 510, 320), 
]
