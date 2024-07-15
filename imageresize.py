from PIL import Image

def resize_image(imagePath,savePath):
    img = Image.open(imagePath)
    img = img.resize((32,32))
    img.save(savePath)