from django.conf import settings

from PIL import Image
import os


# def resize_image(width, height, file_name):
#     file_path = os.path.join(settings.MEDIA_ROOT,"creative/",file_name)
#     return_path = os.path.join(settings.MEDIA_ROOT,"creative/",'resized-'+file_name)
#     print(file_path)
#     file = Image.open(file_path)
#     if file.width < width and file.height < height:
#         img = file.copy()
#         img = img.convert("RGB")
#         img = img.resize((round(width), round(height)), resample=0)
#         dominant_color = img.getpixel((0, 0))
#         background_color = dominant_color
#         background_size = (width, height)
#         new_background_im = Image.new("RGB", background_size, background_color)
#         new_background_im.paste(file, (round((width-file.width)/2), round((height-file.height)/2)))
#         new_background_im.save(return_path)
#     else:
#         new_file = file.resize((width, height))
#         new_file.save(return_path)
#
#     return '/media/creative/resized-'+file_name


def create_background(img, width, height):
    img = img.convert("RGB")
    dominant_color = img.getpixel((0, 0))
    background_color = dominant_color
    background_size = (width, height)
    new_background_im = Image.new("RGB", background_size, background_color)
    return new_background_im


def based_on_width(width, height, file, img):
    new_width = width
    a = file.height / file.width
    new_height = int(new_width * a)
    img = img.resize((new_width, new_height), resample=0)
    new_background_im = create_background(img, width, height)
    new_background_im.paste(img, (round((width - new_width) / 2), round((height - new_height) / 2)))
    return new_background_im


def based_on_height(width, height, file, img):
    new_height = height
    a = file.height / file.width
    new_width = int(new_height / a)
    img = img.resize((new_width, new_height), resample=0)
    new_background_im = create_background(img, width, height)
    new_background_im.paste(img, (round((width - new_width) / 2), round((height - new_height) / 2)))
    return new_background_im


# 722 480 my file sizes
def resize_image(width, height, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, "creative/", file_name)
    return_path = os.path.join(settings.MEDIA_ROOT, "creative/", 'resized-' + file_name)

    file = Image.open(file_path)
    img = file.copy()
    if file.width <= width and file.height <= height:
        if width - file.width < height - file.height:
            new_background_im = based_on_width(width, height, file, img)
            new_background_im.save(return_path)
        elif height - file.height < width - file.width:
            new_background_im = based_on_height(width, height, file, img)
            new_background_im.save(return_path)

    elif file.width >= width and file.height >= height:
        if width <= height:
            new_background_im = based_on_width(width, height, file, img)
            new_background_im.save(return_path)
        elif width > height:
            new_background_im = based_on_height(width, height, file, img)
            new_background_im.save(return_path)

    elif file.width <= width and file.height > height:
        new_background_im = based_on_height(width, height, file, img)
        new_background_im.save(return_path)

    elif file.height <= height and file.width > width:
        new_background_im = based_on_width(width, height, file, img)
        new_background_im.save(return_path)

    return '/media/creative/resized-' + file_name
