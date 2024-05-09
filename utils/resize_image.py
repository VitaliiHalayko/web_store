from PIL import Image

def resize_image(image, width, height, path):
    img = Image.open(image)

    aspect_ratio = img.width / img.height

    target_aspect_ratio = width / height

    if aspect_ratio > target_aspect_ratio:
        new_height = int(img.width / target_aspect_ratio)
        y_offset = (img.height - new_height) / 2
        img = img.crop((0, y_offset, img.width, img.height - y_offset))
    else:
        new_width = int(img.height * target_aspect_ratio)
        x_offset = (img.width - new_width) / 2
        img = img.crop((x_offset, 0, img.width - x_offset, img.height))

    img = img.resize((width, height))

    img.save(path)