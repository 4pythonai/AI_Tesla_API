from fastapi import FastAPI, Request

from fastapi.responses import FileResponse
import os
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from sd import sd_image
import random

origins = ["*"]


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
@app.get("/images/{image_name}")
def serve_image(image_name: str):
    image_path = f"images/{image_name}"
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/png")
    else:
        return "Image not found", 404


def clearImages():

    for filename in os.listdir("images"):
        file_path = os.path.join("images", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


# API to generate random images
@app.post("/txt2img")
async def generate_images(request: Request):
    data = await request.json()
    prompt = data["prompt"]
    clearImages()

    sd_image(prompt)
    image_files = [f for f in os.listdir("images") if f.endswith(".png")]
    return {"code": 200, "message": "Stable Difussion Done.", "files": image_files}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=6789)
