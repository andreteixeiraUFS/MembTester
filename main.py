import io
from fastapi import FastAPI, File
from PIL import Image
import imageAnalyzer as imgA

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "Hello World"}

#recebe uma imagem e retorna um resultado
@app.post('/tester')
async def predict(image: bytes = File(...)):
    img = io.BytesIO(image)
    img.seek(0)

    byteImg = Image.open(img)
    byteImg.save('image.jpg', 'JPEG')

    print(type(img))
    print(type(byteImg))
    return imgA.imgAnalyzer('image.jpg')


# para start no servidor: uvicorn main:app --host 0.0.0.0 --port 8000