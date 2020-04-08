from pathlib import Path
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def print_text(image, text):
    """Prints text on an image"""
    base = image.convert('RGBA')
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
    W = base.size[0]

    draw = ImageDraw.Draw(txt)
    font = ImageFont.truetype("Arial.ttf", 48)
    w, h = draw.textsize(text, font=font)

    draw.rectangle((((W-w)/2 - 10, 15), ((W + w)/2 + 10, h + 10)), fill=(255, 255, 255, 150))
    draw.text(((W-w)/2, 10), text, (252, 3, 3), font=font)

    out = Image.alpha_composite(base, txt)

    return out


def merge_images(locations, output, text=None):
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
    print(f'\tImage {Path(locations[0]).name} saved to {str(output)} folder.')
