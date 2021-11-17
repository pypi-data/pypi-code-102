import os
import base64
import io
from PIL import Image

class Library_Functions():
    
    def reduce_and_prepare_image(image_path):
        image = Image.open(image_path)
        image = image.resize((224, 224))
        image_byte_array = io.BytesIO()
        image.save(image_byte_array, format='PNG')
        image_byte_array = image_byte_array.getvalue()

        image_base64_string = base64.b64encode(image_byte_array)
        image_base64_string = image_base64_string.decode('utf-8')
        
        return image_base64_string
    

    def reconstruct_image_learner(image_learner):
        for image, images in image_learner['image'].items():
            for i in range(len(images)):
                images[i] = Library_Functions.reduce_and_prepare_image(images[i])
        
        return image_learner