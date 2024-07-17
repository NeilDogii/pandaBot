from PIL import Image,ImageSequence

def resize_image(imagePath,savePath):
    img = Image.open(imagePath)
    img = img.resize((42,42))
    img.save(savePath)
    
def resize_gif(imagePath, savePath, new_size=(42, 42)):
    img = Image.open(imagePath)
    frames = []
    durations = []

    for frame in ImageSequence.Iterator(img):
        frame = frame.convert("RGBA")
        resized_frame = frame.resize(new_size, Image.Resampling.LANCZOS)
        new_frame = Image.new("RGBA", new_size)
        new_frame.paste(resized_frame, (0, 0), resized_frame)
        frames.append(new_frame)
        durations.append(frame.info['duration'])

    frames[0].save(savePath, save_all=True, append_images=frames[1:], loop=0, duration=durations, disposal=2)