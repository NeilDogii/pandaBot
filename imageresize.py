from PIL import Image

def resize_image(imagePath,savePath):
    img = Image.open(imagePath)
    img = img.resize((42,42))
    img.save(savePath)
    
