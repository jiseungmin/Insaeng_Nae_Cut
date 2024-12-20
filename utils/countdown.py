def countdown(timer_label, seconds, callback):
    if seconds > 0:
        timer_label.config(
            text=f"카메라를 바라봐 주세요. 촬영까지 {seconds}초...",
            font=("Arial", 18),
            bg="#f0f0f0",
            fg="red",
        )
        timer_label.master.update_idletasks()
        timer_label.master.after(1000, countdown, timer_label, seconds - 1, callback)
    else:
        timer_label.config(text="촬영 중...", font=("Arial", 18), fg="green")
        timer_label.master.update_idletasks()
        callback()
