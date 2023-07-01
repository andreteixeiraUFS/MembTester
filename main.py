import io
from typing import Optional, List

from fastapi import FastAPI, File, Form, UploadFile
from PIL import Image
import imageAnalyzer as imgA


app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "Hello World"}

#recebe uma imagem e retorna um resultado
@app.post('/tester')
async def predict(diabetes: str = Form(...), image: UploadFile = File(...)):
    content = await image.read()  # async read
    print(type(content))

    img = io.BytesIO(content)
    img.seek(0)

    byteImg = Image.open(img)
    byteImg.save('lastImage.jpg', 'JPEG')

    return imgA.imgAnalyzer(diabetes,'lastImage.jpg')


# para start no servidor: uvicorn main:app --host 0.0.0.0 --port 8000