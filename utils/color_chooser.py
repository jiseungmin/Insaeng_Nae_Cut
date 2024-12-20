from tkinter.colorchooser import askcolor

def choose_color():
    color = askcolor(title="배경 색 선택")[1] 
    if color:
        return tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    return (255, 255, 0)  
