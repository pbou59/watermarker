from PIL import Image, ImageTk
import tkinter as tk
from tkinter.filedialog import askopenfilename

SOURCE_DIRECTORY = "../Users/Paul/Pictures"
TARGET_DIRECTORY = "../Users/Paul/Pictures/Watermarked Photos"


def open_file():
    # Change text on browse button and open dialog box,
    browse_text.set("Loading...")
    photo_name = askopenfilename(initialdir=SOURCE_DIRECTORY, title="Select A File", filetype=(("jpeg files", "*.jpg"),
                                                                                               ("all files", "*.*")))

    # If photo exits, (which it should since we selected it), then start the processing.
    if photo_name:
        image = Image.open(photo_name).convert("RGBA")  # Seems like only "RGBA" will work.
        wm_image = Image.open("images/Paul Watermark 2.png").convert("RGBA")

        # Size watermark relative to size of base image
        wm_resized = wm_image.resize((round(image.size[0]*.35), round(image.size[1]*.35)))
        wm_mask = wm_resized.convert("RGBA")

        # Set position to lower right corner
        position = (image.size[0] - wm_resized.size[0], image.size[1] - wm_resized.size[1])

        # Start stacking layers on top of a black background.
        transparent = Image.new('RGBA', image.size, (0, 0, 0, 0))
        transparent.paste(image, (0, 0))
        transparent.paste(wm_mask, position, mask=wm_mask)

        # Display image
        transparent.show()

        # Save watermarked photo
        finished_img = transparent.convert("RGB")  # Convert back to 3-channel image
        finished_img_name = photo_name[:-4] + " WM.jpg"
        finished_img.save(finished_img_name)

        success_text.set(f"Success!  File saved to {finished_img_name}.")

        browse_text.set("Browse")


def quit_app():
    root.destroy()


# GUI set-up
root = tk.Tk()
root.title("Photo Watermark App")

# Create the canvas
canvas = tk.Canvas(root, width=600, height=500)
canvas.grid(columnspan=5, rowspan=4)

# Add a flashy logo
logo = Image.open("images/logo.png")
logo = logo.resize((200, 200))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=3, row=0)

instruction_label = tk.Label(root, text="Select photo to watermark.", font="Ariel")
instruction_label.grid(columnspan=5, column=0, row=1)

# Browse dialog button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, command=open_file, textvariable=browse_text, font="Ariel", bg="#0099ff", fg="white",
                       height=2, width=15)
browse_text.set("Browse")
browse_btn.grid(column=2, row=2)

# Success Message
success_text = tk.StringVar()
success_text.set(" ")
success_label = tk.Label(root, textvariable=success_text)
success_label.grid(columnspan=5, column=0, row=3)

# Cancel Button
cancel_btn = tk.Button(root, text="Quit", command=quit_app, font="Ariel", bg="#0099ff", fg="white", height=2, width=15)
cancel_btn.grid(column=4, row=2, padx=10)

root.mainloop()