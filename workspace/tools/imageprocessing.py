import os
import subprocess
from PIL import Image, ImageFilter

class imageprocessing:
    def __init__(self):
        pass

    def image_enhancer(self, image_path, enhancement_type):
        """
        Enhances image quality using AI techniques. Can improve resolution,
        reduce noise, and adjust colors for better visual appeal.
        """
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"The file {image_path} does not exist.")

            # Open the image
            image = Image.open(image_path)

            # Apply enhancements based on the enhancement_type
            if enhancement_type == "resolution":
                enhanced_image = image.resize((image.width * 2, image.height * 2), Image.ANTIALIAS)
            elif enhancement_type == "noise_reduction":
                enhanced_image = image.filter(ImageFilter.MedianFilter(size=3))
            elif enhancement_type == "color_adjustment":
                enhanced_image = image.convert("RGB").point(lambda p: p * 1.1)
            else:
                  raise ValueError("Invalid enhancement type. Choose from 'resolution', 'noise_reduction', or 'color_adjustment'.")

            # Save the enhanced image
            enhanced_image_path = self._get_enhanced_image_path(image_path, enhancement_type)
            enhanced_image.save(enhanced_image_path)

            return enhanced_image_path
        except Exception as e:
            return str(e)

    def _get_enhanced_image_path(self, original_path, enhancement_type):
        """
        Helper method to create a path for the enhanced image.
        """
        base, ext = os.path.splitext(original_path)
        return f"{base}_{enhancement_type}{ext}"
    
    def delete_image(self, image_name):
        """
        This tool allows users to delete a specified image file, helping manage and organize their workspace.
        """
        try:
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "images")
            file_path = os.path.join(workspace_folder, image_name)

            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted image: {image_name}")
            else:
                print(f"The image {image_name} does not exist.")
        except Exception as e:
            print(f"An error occurred while deleting {image_name}: {str(e)}")

    def list_images(self):
        """
        This tool lists all the image files created within the current session or project, helping users keep track of their files.
        """
        try:
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "images")
            files = [f for f in os.listdir(workspace_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            print("Images in workspace:")
            for file in files:
                print(file)
            return files
        except Exception as e:
            print(f"An error occurred while listing image files: {str(e)}")
            return []
