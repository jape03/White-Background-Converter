import os
import cv2
import numpy as np
from tqdm import tqdm

def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))
    ]

    for image_file in tqdm(image_files, desc="Processing Images"):
        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + ".png")

        try:
            # Load image
            img = cv2.imread(input_path, cv2.IMREAD_COLOR)
            if img is None:
                print(f"Error: Could not open {image_file}")
                continue

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to isolate text from background
            _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

            # Upscale image to improve anti-aliasing
            upscaled = cv2.resize(binary, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

            # Apply bilateral filter (preserves edges but removes noise)
            smoothed = cv2.bilateralFilter(upscaled, 9, 75, 75)

            # Apply morphological operations to clean up edges
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(smoothed, cv2.MORPH_CLOSE, kernel)

            # Downscale back to original size (to reduce jagged edges)
            final_resized = cv2.resize(cleaned, (binary.shape[1], binary.shape[0]), interpolation=cv2.INTER_AREA)

            # Invert back to white background
            final_result = cv2.bitwise_not(final_resized)

            # Convert to BGR for saving
            final_image = cv2.cvtColor(final_result, cv2.COLOR_GRAY2BGR)

            # Save processed image
            cv2.imwrite(output_path, final_image)

        except Exception as e:
            print(f"Error processing {image_file}: {e}")

if __name__ == "__main__":
    input_folder = r"C:\Users\jayyy\Desktop\Words-jape\c\c-removedNotWhite\c-page51" # palitan nyo ng local path nyo dito
    output_folder = os.path.join(input_folder, "output")

    process_images(input_folder, output_folder)
    print("Processing completed! Check the output folder for the modified images.")
