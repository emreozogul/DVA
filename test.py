import eel
from PIL import Image
import io

eel.init('test')  # Your web files (HTML, JS, CSS) are in a folder called 'web'

@eel.expose
def process_cropped_image(image_data):
    # Convert the Blob to a PIL Image
    image = Image.open(io.BytesIO(image_data))
    image.save('cropped_image.png')
    print("Image has been saved.")

eel.start('index.html', size=(800, 600) , port=8080)
