import os
from PIL import Image
import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np

def selectImageAndColor():
    # Create a Tkinter window for image selection
    Tk().withdraw()
    
    coordinates = [0, 0]  # Initialize coordinates [x, y]
    selected_color = None  # Initialize color variable

    def onMouseClick(event, x, y, flags, param):
        nonlocal selected_color  # Use the color variable from the outer scope
        if event == cv2.EVENT_LBUTTONDOWN:
            coordinates[0] = x
            coordinates[1] = y
            pixel_color = image[y, x]  # Get the color of the selected pixel (BGR format)
            selected_color = tuple(cv2.cvtColor(np.array([pixel_color], dtype=np.uint8), cv2.COLOR_BGR2RGBA)[0][0])
            print(selected_color)
  # Convert BGR to a tuple(R, G, B, A)
            cv2.destroyWindow("Image")  # Close the image window
            cv2.waitKey(1)  # Release any pending key event

    # Ask the user to select an image file
    image_path = askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico")])
    image = cv2.imread(image_path)

    if image is None:
        print("Unable to read the image")
        return

    cv2.namedWindow("Image")
    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", onMouseClick)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image_path, selected_color  # Return the image path and the selected color tuple

def removeSelectedColor(input_image_path, output_image_path, color_to_remove):
    try:
        # Load the image using PIL
        img = Image.open(input_image_path)
        img = img.convert('RGBA')

        # Convert the PIL image to a NumPy array for OpenCV
        img_np = np.array(img)

        # Define the color to remove (R, G, B, A)
        r, g, b, a = color_to_remove

        # Create a mask for the color to remove
        color_mask = (img_np[:, :, 0] == r) & (img_np[:, :, 1] == g) & (img_np[:, :, 2] == b) & (img_np[:, :, 3] == a)

        # Set the color to remove to transparent (0 alpha)
        img_np[color_mask] = [0, 0, 0, 0]

        # Convert the NumPy array back to a PIL image
        result_img = Image.fromarray(img_np)

        # Save the resulting image
        result_img.save(output_image_path)

        print("Image with selected color removed successfully saved to:", output_image_path)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Create a Tkinter window to select an image
    Tk().withdraw()

    # Get the path of the image and the color to remove
    input_image_path, color_to_remove = selectImageAndColor()

    # Get the absolute path of the current directory
    current_directory = os.path.abspath(os.path.dirname(__file__))

    # Build the complete path to save the resulting image
    output_image_path = os.path.join(current_directory, input("Name of the new image:") + ".png")

    # Call the function to remove the selected color
    removeSelectedColor(input_image_path, output_image_path, color_to_remove)
