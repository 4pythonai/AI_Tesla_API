from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
import random

origins = [
    "http://localhost",
    "http://localhost:3000",  # Example: React development server
]

 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Function to generate a random image
def generate_random_image():
    width = 1024
    height = 1024
    image = Image.new("RGB", (width, height))
    pixels = image.load()

    for i in range(width):
        for j in range(height):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            pixels[i, j] = (r, g, b)

    return image

# Route to generate and serve random images 
@app.get('/images/{image_name}')
def serve_image(image_name: str):
    image_path = f'images/{image_name}'
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type='image/png')
    else:
        return "Image not found", 404

# API to generate random images
@app.get('/txt2img')
def generate_images():
    # Delete all files in the images folder
    for filename in os.listdir("images"):
        file_path = os.path.join("images", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    image1 = generate_random_image()
    image2 = generate_random_image()

    image_name1 = f"random1.png"
    image_path1 = f'images/{image_name1}'
    image1.save(image_path1)

    image_name2 = f"random2.png"
    image_path2 = f'images/{image_name2}'
    image2.save(image_path2)

    image_files = [filename for filename in os.listdir("images") if filename.endswith(".png")]

    return {"code":200, "message": "Stable Difussion Done.", "files": image_files}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
