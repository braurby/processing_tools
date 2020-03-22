from pathlib import Path
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def print_text(image, text):
    """Prints text on an image"""
    W = image.size[0]
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Arial.ttf", 32)
    w = draw.textsize(text)[0]
    draw.text(((W-w)/2, 10), text, (252, 3, 3), font=font)

    return image


def merge_images(locations, output, text=[]):
    # Define images
    images = []
    sizes = []

    for loc in locations:
        try:
            image = Image.open(loc)

            # Resize images to the same values
            if not sizes:
                sizes = image.size
            if image.size is not sizes:
                image = image.resize(sizes)

            images.append(image)
        except OSError:
            print(f'File not an image: {loc.name}')
            continue

    # Print text on image
    if text:
        for i in range(len(images)):
            images[i] = print_text(images[i], text[i])

    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0

    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save(output / Path(locations[0]).name)
    print(f'\tImage {Path(locations[0]).name} saved to {output} folder.')
