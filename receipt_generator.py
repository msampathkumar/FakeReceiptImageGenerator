'''
A Simple Experimental Receipt Generator
'''

from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageOps


def insert_text(draw: ImageDraw, x, y, text,
                color='rgb(0, 0, 0)',
                font_file='fonts/Roboto-Bold.ttf',
                font_size=12):
    text = str(text)
    font = ImageFont.truetype(font_file, size=font_size)
    draw.text((x, y), text, fill=color, font=font)
    return draw


def text_image(text, font_size=12, size=(320, 480), border=False):
    width, height = size
    _text = text.center(int(int(width / font_size) * 3.2))
    if border:
        _text = _text.replace(' ', '.')
    image = Image.new(mode="RGB", size=(width, font_size + 4), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw = insert_text(draw=draw, x=0 + 4, y=0, text=_text, font_size=font_size)
    if border:
        image = ImageOps.expand(image, border=2, fill='black')
    return image


def combine_all_images_horizantally(images):
    # images = map(Image.open, sys.argv[1:-1])
    w = sum(i.size[0] for i in images)
    mh = max(i.size[1] for i in images)

    result = Image.new("RGBA", (w, mh))

    x = 0
    for i in images:
        result.paste(i, (x, 0))
        x += i.size[0]
    return result


def combine_all_images_vertically(images):
    # images = map(Image.open, sys.argv[1:-1])
    w = max(i.size[0] for i in images)
    mh = sum(i.size[1] for i in images)

    result = Image.new("RGBA", (w, mh))

    x = 0
    for i in images:
        result.paste(i, (0, x))
        x += i.size[1]
    return result


## Testing
# text_image('hello', font_size=25, size=(320, 220))
# text_image('hello', font_size=20, size=(320, 120))
# text_image('hello', font_size=15, size=(320, 120))

################################################################################ MERCHANT

text_data = [
    'Merchant Name',
    'Shop is in Okalhama, OA',
    '000-123-997'
]

image1 = combine_all_images_vertically([
    text_image(text_data[0], font_size=25, size=(320, 0)),
    text_image(text_data[1], font_size=12, size=(320, 0)),
    text_image(text_data[2], font_size=12, size=(320, 0)),
]
)
# image1

################################################################################ MERCHANT ADDR

image2 = combine_all_images_horizantally([
    text_image('Receipt: 12313', font_size=12, size=(160, 0)),
    text_image('Date: 12/12/2009', font_size=12, size=(160, 0))
])

# image2

################################################################################ LINE ITEMS

line_items = [
    ('S.No', 'Item Description', 'Items', 'Cost'),
    ('1', 'Chocolate Cake(1 Kg) ', '1', '895.0'),
    ('2', 'Flower Bookie', '1', '500.50'),
    ('3', 'Rat Poisen(500ml)', '1', '50.50'),
]

bag = []

for each_line in line_items:
    _image_line_item = combine_all_images_horizantally([
        text_image(each_line[0], font_size=14, size=(40, 0)),
        text_image(each_line[1], font_size=12, size=(160, 0)),
        text_image(each_line[2], font_size=12, size=(40, 0)),
        text_image(each_line[3], font_size=12, size=(80, 0)),
    ])
    bag.append(_image_line_item)

image3 = combine_all_images_vertically(bag)

################################################################################ LINE ITEMS

text_items = [
    ('      Tax:', '5.15'),
    ('      GST:', '1.15'),
    ('      SST:', '1.15'),
    ('Total Tax:', '1299.10'),
]

bag = []
for each_line in text_items:
    _image_text = combine_all_images_horizantally([
        text_image('', font_size=14, size=(160, 0)),
        text_image(each_line[0], font_size=14, size=(80, 0)),
        text_image(each_line[1], font_size=14, size=(80, 0))
    ])
    bag.append(_image_text)

image4 = combine_all_images_vertically(bag)

# image4
################################################################################ LINE SEP

image5 = text_image('--' * 35, font_size=14, size=(320, 0))
# image5

################################################################################ LINE SEP
image6 = text_image(' ', font_size=14, size=(320, 0))
# image6

################################################################################ LINE SEP
final_output_image = combine_all_images_vertically([
    image6,
    image1,
    image6,
    image2,
    image6,
    image3,
    image5,
    image6,
    image4
])

final_output_image.save('sample-out.png')


