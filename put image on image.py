import os
from PIL import Image
import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def getImageAndCoordinates():
    # Create a Tkinter window to select an image
    Tk().withdraw()
    
    coordinates = [0, 0]  # Initialize coordinates as a list [x, y]

    def onMouseClick(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            coordinates[0] = x
            coordinates[1] = y
            cv2.destroyWindow("Image")  # Close the image window
            cv2.waitKey(1)  # Release any pending key event

    # Ask the user to select an image file
    image_path = askopenfilename()
    image = cv2.imread(image_path)

    if image is None:
        print("Unable to read the image")
        return

    cv2.namedWindow("Image")
    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", onMouseClick)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image_path, tuple(coordinates)  # Convert coordinates back to a tuple

# Function to add image to an image
def addImageToImage(backgroundImagePath, frontImagePath, coordinates, outImageName="output_image"):
    try:
        # Open the images
        bgImg = Image.open(backgroundImagePath)
        bgImg = bgImg.convert('RGBA')
        ftImg = Image.open(frontImagePath)
        ftImg = ftImg.convert('RGBA')
        
        # Fuse the images
        bgImg.paste(ftImg, coordinates, ftImg)

        # Get the absolute path of the current directory
        currentDirectory = os.path.abspath(os.path.dirname(__file__))

        # Build the complete path to save the resulting image
        outputPath = os.path.join(currentDirectory, outImageName + ".png")

        # Save the resulting image
        bgImg.save(outputPath)

        print("Image successfully saved to:", outputPath)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    bgImgPath, coordinates = getImageAndCoordinates()
    ftImgPath = askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico")])
    addImageToImage(bgImgPath, ftImgPath, coordinates)
