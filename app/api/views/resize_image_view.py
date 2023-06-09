from django.http import HttpResponse
from PIL import Image
import os
import numpy as np

from api.tools.logging_tools import info_log

def get_most_common_color(img):
    # convert the image to a numpy array
    img_array = np.array(img.convert('RGB'))

    # flatten the array and count the occurrences of each color
    flattened_array = img_array.reshape(-1, 3)
    counts = np.bincount(flattened_array[:,0] * 256 * 256 + flattened_array[:,1] * 256 + flattened_array[:,2])

    # get the index of the most common color
    most_common_color_index = counts.argmax()

    # convert the index back to RGB values
    r = most_common_color_index // (256 * 256)
    g = (most_common_color_index - r * 256 * 256) // 256
    b = most_common_color_index % 256

    return (r, g, b)


def generate_resized_image(request, id):
    width = request.GET.get('width', None)
    height = request.GET.get('height', None)
    info_log("id: {} width: {} height: {}".format(id, width, height))
    # Load the original image from the media folder
    if str(id).split('.')[-1] != 'png':
        id = str(id)+".png"
    file_path = os.path.join('media', 'creative', id)
    
    # open the image using PIL
    with Image.open(file_path) as img:
        # get the original dimensions of the image
        original_width, original_height = img.size

        # get the requested dimensions from the request
        requested_width = request.GET.get('width', None)
        requested_height = request.GET.get('height', None)

        # if no dimensions are specified, return the original image
        if not requested_width and not requested_height:
            response = HttpResponse(content_type='image/png')
            img.save(response, 'PNG')
            return response

        # calculate the new dimensions while maintaining aspect ratio
        if requested_width and requested_height:
            new_width, new_height = int(requested_width), int(requested_height)
        elif requested_width:
            new_width = int(requested_width)
            new_height = int((new_width / original_width) * original_height)
        else:
            new_height = int(requested_height)
            new_width = int((new_height / original_height) * original_width)

        # resize the image while maintaining aspect ratio
        img.thumbnail((new_width, new_height), Image.ANTIALIAS)

        # create a new image with the requested dimensions and fill it with the most used color in the image
        most_common_color = get_most_common_color(img)
        new_img = Image.new("RGB", (new_width, new_height))

        # paste the resized image onto the new image
        new_img.paste(img, ((new_width - img.size[0]) // 2, (new_height - img.size[1]) // 2))

        # convert the new image to bytes and return it as an HTTP response
        response = HttpResponse(content_type='image/png')
        new_img.save(response, 'png')
        return response

