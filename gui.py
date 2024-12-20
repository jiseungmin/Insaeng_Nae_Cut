import cv2
import tkinter as tk
from PIL import Image, ImageTk
from utils.countdown import countdown
from utils.webcam import capture_image
from utils.color_chooser import choose_color
from tkinter import ttk, filedialog, messagebox
from utils.background_removal import remove_background
from utils.image_processing import positions, background

def create_gui():
    global root  
    global show_image_button  
    root = tk.Tk()
    root.title("인생네컷")
    root.geometry("700x600")
    root.resizable(False, False)

    configure_style(root)

    frame = tk.Frame(root, bg="#1F1F1F")
    frame.place(relwidth=1, relheight=1)

    title_label = tk.Label(
        frame,
        text="✨ 인생네컷 제작 도구 ✨",
        font=("Roboto", 26, "bold"),
        bg="#1F1F1F",
        fg="#ECF0F1",
    )
    title_label.pack(pady=30)

    progress_label = tk.Label(
        frame,
        text="시작 버튼을 눌러 작업을 시작하세요!",
        font=("Roboto", 14),
        bg="#1F1F1F",
        fg="#95A5A6",
    )
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(
        frame,
        orient="horizontal",
        length=500,
        mode="determinate",
        style="TProgressbar",
    )
    progress_bar.pack(pady=20)

    ttk.Button(
        frame,
        text="📂 이미지 선택 및 배경 제거",
        command=lambda: select_images(progress_label, progress_bar),
        style="Modern.TButton",
    ).pack(pady=20)

    ttk.Button(
        frame,
        text="📸 웹캠으로 촬영",
        command=lambda: capture_and_use_image(progress_label, progress_bar),
        style="Modern.TButton",
    ).pack(pady=20)

    show_image_button = ttk.Button(
        frame,
        text="결과 이미지 보기",
        command=show_result_image,
        state=tk.DISABLED,
        style="Modern.TButton",
    )
    show_image_button.pack(pady=20)

    footer_label = tk.Label(
        frame,
        text="© 2024 임베디드 시스템 11팀 인생네컷 제작 도구 | All Rights Reserved",
        font=("Roboto", 10),
        bg="#1F1F1F",
        fg="#7F8C8D",
    )
    footer_label.pack(side="bottom", pady=10)

    root.mainloop()


def configure_style(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(
        "Modern.TButton",
        font=("Roboto", 14, "bold"),
        padding=10,
        foreground="#ECF0F1",
        background="#3498db",
        borderwidth=0,
        anchor="center",
        width=30,
        relief="flat",
    )
    style.map(
        "Modern.TButton",
        background=[("active", "#2980b9")],
        foreground=[("disabled", "#95A5A6")],
    )
    style.configure(
        "TProgressbar",
        thickness=10,
        background="#3498db",
        troughcolor="#1F1F1F",
        borderwidth=0,
    )


def select_images(progress_label, progress_bar):
    for i in range(4):
        progress_label.config(text=f"Processing image {i + 1}/4...")
        progress_bar["value"] = (i + 1) * 25
        root.update_idletasks()

        file_path = filedialog.askopenfilename(
            title=f"Select image ({i + 1}/4)",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")],
        )
        if file_path:
            bg_color = choose_color()
            processed_image = remove_background(file_path, bg_color)
            if processed_image is not None:
                img = Image.fromarray(cv2.cvtColor(processed_image, cv2.COLOR_BGRA2RGBA))
                img = img.resize((positions[i][2], positions[i][3]), Image.LANCZOS)
                background.paste(img, (positions[i][0], positions[i][1]), img)

    output_path = "./assets/output_inseang_necut.png"
    background.save(output_path)
    progress_label.config(text="Process Complete! Output saved.")
    progress_bar["value"] = 100

    show_image_button.config(state=tk.NORMAL)  


def capture_and_use_image(progress_label, progress_bar):
    timer_label = tk.Label(root, text="", font=("Arial", 18), bg="#f0f0f0", fg="red")
    timer_label.place(relx=0.5, rely=0.4, anchor="center")

    def capture_single_image(index):
        progress_label.config(text=f"Capturing image {index + 1}/4...")
        progress_bar["value"] = (index + 1) * 25
        root.update_idletasks()

        image_path = f"./assets/captured_image_{index + 1}.jpg"
        capture_image(image_path)
        captured_image = Image.open(image_path)
        resized_image = captured_image.resize((positions[index][2], positions[index][3]), Image.LANCZOS)
        background.paste(resized_image, (positions[index][0], positions[index][1]))

        if index < 3:  
            countdown(timer_label, 3, lambda: capture_single_image(index + 1))
        else:
            output_path = "./assets/output_inseang_necut.png"
            background.save(output_path)
            progress_label.config(text="Process Complete! Output saved.")
            progress_bar["value"] = 100
            show_image_button.config(state=tk.NORMAL)  
            timer_label.destroy()

    countdown(timer_label, 3, lambda: capture_single_image(0))


def show_result_image():
    try:
        output_path = "./assets/output_inseang_necut.png"
        result_image = Image.open(output_path)
        result_image = result_image.resize((350, 1000))

        img_tk = ImageTk.PhotoImage(result_image)
        result_window = tk.Toplevel()
        result_window.title("Result Image")
        result_label = tk.Label(result_window, image=img_tk)
        result_label.image = img_tk
        result_label.pack()
    except FileNotFoundError:
        messagebox.showerror("Error", "Result image not found!")
