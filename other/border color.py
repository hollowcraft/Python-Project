from tkinter import Tk, filedialog, simpledialog
from PIL import Image, ImageOps, ImageChops

def hex_to_rgb(hex_color):
    """Convert hexadecimal color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    raise ValueError("Invalid hexadecimal color format. Use #RRGGBB.")

def add_border_around_object(image_path, border_color):
    """Add a border around the object in the image with the specified color."""
    # Open the image
    img = Image.open(image_path).convert("RGBA")

    # Create a mask by extracting the alpha channel or converting to grayscale
    if "A" in img.getbands():
        mask = img.getchannel("A")
    else:
        gray = img.convert("L")
        mask = gray.point(lambda x: 0 if x < 128 else 255, mode="1")

    # Expand the mask to create a border
    border_size = simpledialog.askinteger("Border Size", "Enter the border size in pixels:", minvalue=1, maxvalue=500)

    if border_size is None:
        print("Operation cancelled.")
        return

    expanded_mask = ImageOps.expand(mask, border=border_size, fill=255)

    # Create a new image with the border color
    border_image = Image.new("RGBA", expanded_mask.size, border_color + (255,))

    # Paste the original image onto the border image using the mask
    border_image.paste(img, (border_size, border_size), mask=mask)

    # Save the result
    output_path = filedialog.asksaveasfilename(
        title="Save Image As",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )

    if output_path:
        border_image.save(output_path)
        print(f"Image saved to {output_path}")
    else:
        print("No file selected for saving.")

def main():
    # Hide the root window
    root = Tk()
    root.withdraw()

    # Ask user for the image file
    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")]
    )

    if not image_path:
        print("No image selected.")
        return

    # Ask user for the border color in hexadecimal format
    hex_color = simpledialog.askstring("Border Color", "Enter the border color in hexadecimal format (#RRGGBB):")

    if not hex_color:
        print("No color entered.")
        return

    try:
        border_color = hex_to_rgb(hex_color)
    except ValueError as e:
        print(e)
        return

    # Add the border
    add_border_around_object(image_path, border_color)

if __name__ == "__main__":
    main()
