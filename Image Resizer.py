import PIL.Image
import PIL.ImageTk

from tkinter import *     # from tkinter import Tk for Python 3.x
from tkinter import messagebox 
from tkinter.filedialog import askopenfilename

#global filename

#filename = None

def calculate_dpi(image, width_cm, height_cm):
    """
    Calculate the DPI needed to match the given dimensions in cm.
    """
    img_width_px, img_height_px = image.size
    dpi_width = img_width_px / (width_cm / 2.54)
    dpi_height = img_height_px / (height_cm / 2.54)
    
    # Typically, DPI is uniform, so we return an average or either value.
    return int(dpi_width), int(dpi_height)

def cm_to_pixels(cm, dpi):
    """Convert centimeters to pixels based on DPI."""
    return int(cm * dpi / 2.54)

def resize_image(input_path, output_path, width_cm, height_cm, dpi=300):
    """
    Resize an image to the specified dimensions in centimeters.
    """
    global filename, input_image_path
    with PIL.Image.open(input_path) as img:
        width_px = cm_to_pixels(width_cm, dpi)
        height_px = cm_to_pixels(height_cm, dpi)
        resized_img = img.resize((width_px, height_px), PIL.Image.LANCZOS)
        resized_img.save(output_path, dpi=(dpi, dpi))
        print(f"Resized image saved to {output_path}")
        return resized_img

def split_into_a4_pages(image, dpi=300):
    """
    Splits an image into A4-sized pages (21x29.7 cm) and saves them as separate files.
    """
    # A4 dimensions in pixels
    a4_width_px = cm_to_pixels(21, dpi)
    a4_height_px = cm_to_pixels(29.7, dpi)

    # Image dimensions
    img_width, img_height = image.size

    # Calculate the number of pages
    cols = (img_width + a4_width_px - 1) // a4_width_px
    rows = (img_height + a4_height_px - 1) // a4_height_px

    print(f"Image will be split into {cols}x{rows} A4 pages.")

    # Split the image into pages
    for row in range(rows):
        for col in range(cols):
            left = col * a4_width_px
            upper = row * a4_height_px
            right = min(left + a4_width_px, img_width)
            lower = min(upper + a4_height_px, img_height)

            # Crop the current A4 section
            page = image.crop((left, upper, right, lower))

            # Save the cropped page
            page_path = f"a4_page_{row+1}_{col+1}.jpg"
            page.save(page_path)
            print(f"Saved {page_path}")


def selectFile():
    global filename, imageLabel
    filename = askopenfilename()
    print(filename)
    if filename:
        with PIL.Image.open(filename) as img:
            img.thumbnail((200, 200), PIL.Image.LANCZOS)
            tkimg = PIL.ImageTk.PhotoImage(img)
            
            if 'imageLabel' in globals() and imageLabel.winfo_exists():
                imageLabel.config(image=tkimg)
                imageLabel.image = tkimg
        

def run():
    global filename, input_image_path
    input_image_path = filename  # Replace with your input image path
    resized_image_path = "resized_image.jpg"  # Path for the resized image
    dpi = int(dpiEntry.get())  # Set DPI for high quality
    width_in_cm = int(widthInput.get())  # Width in cm for the resized image
    height_in_cm = int(heightInput.get())  # Height in cm for the resized image

    # Step 1: Resize the image
    resized_image = resize_image(input_image_path, resized_image_path, width_in_cm, height_in_cm, dpi)

    # Step 2: Split the resized image into A4-sized pages
    split_into_a4_pages(resized_image, dpi)

    messagebox.showinfo("Done!", "Done!")



root = Tk() # we don't want a full GUI, so keep the root window from appearing
leftframe = Frame(root)
leftframe.grid(row=0, column=0)

rightframe = Frame(root)
rightframe.grid(row=0, column=1)

root.title("Image Resizer")
root.resizable(False, False)


height = Label(leftframe, text="Height (cm)")
height.grid(row=0, column=0)
heightInput = Entry(leftframe)
heightInput.grid(row=0, column=1, pady=5)

width = Label(leftframe, text="Width (cm)")
width.grid(row=1, column=0)
widthInput = Entry(leftframe)
widthInput.grid(row=1, column=1, pady=5)

dpiText = Label(leftframe, text="DPI")
dpiText.grid(row=2, column=0, pady=5)
dpiEntry = Entry(leftframe)
dpiEntry.insert(0,300)
#dpiEntry.setvar("300")
dpiEntry.grid(row=2, column=1)

imageLabel = Label(rightframe)
imageLabel.pack(expand=1, fill="both", padx=10)


picker = Button(leftframe, text="Choose Image", command=selectFile)
picker.grid(row=3,column=0, pady=10, padx=10)


runBtn = Button(leftframe, text="Create Images", command=run)
runBtn.grid(row=3,column=1, pady=10)




root.mainloop()