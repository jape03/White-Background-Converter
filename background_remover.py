import os
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

def make_background_white(input_folder, output_folder):
   
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all image files
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

    for image_file in tqdm(image_files, desc="Processing Images"):
        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + ".png")  

        try:
            # Open the image using OpenCV
            img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

            if img is None:
                print(f"Error: Could not open {image_file}")
                continue
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply adaptive threshold to make light areas fully white
            _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Convert back to color and apply the white mask
            result = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

            # Save the processed image
            cv2.imwrite(output_path, result)
        
        except Exception as e:
            print(f"Error processing {image_file}: {e}")

if __name__ == "__main__":
    input_folder = r"C:\Users\jayyy\Desktop\Words-jape\c\c-removedNotWhite\c-page51"  # PALITAN NYO TO NG LOCAL PATH NYO 
    output_folder = os.path.join(input_folder, "output")  

    make_background_white(input_folder, output_folder)
    print("Background normalization completed! All images now have a white background.")
