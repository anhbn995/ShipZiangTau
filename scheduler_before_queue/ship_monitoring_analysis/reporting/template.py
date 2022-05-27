import tempfile

import numpy as np
import rasterio
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from skimage import io, transform

######################
### CONSTANTS
######################

PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]

# DARK = colors.mediumslateblue
# LIGHT = colors.lavender
DARK = colors.grey
LIGHT = colors.lightgrey
WHITE = colors.white

######################
### STYLES
######################

stylesheet = getSampleStyleSheet()

H1 = ParagraphStyle(
    name='H1',
    parent=stylesheet['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=16,
    # textColor = DARK,
)

H2 = ParagraphStyle(
    name='H2',
    parent=stylesheet['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=14,
)

H3 = ParagraphStyle(
    name='H3',
    parent=stylesheet['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=12,
)

Text = ParagraphStyle(
    name='Text',
    parent=stylesheet['Normal'],
    fontName='Helvetica',
    fontSize=11,
)

Header = ParagraphStyle(
    name='Header',
    parent=stylesheet['Normal'],
    fontName='Helvetica',
    fontSize=11,
    alignment=TA_RIGHT,
)


def header(txt):
    p = Paragraph(txt, Header)
    # Report.append(p)
    return p


def footer(canvas, doc):
    canvas.saveState()
    canvas.setTitle("Ship Detection Report")
    canvas.setFont('Helvetica', 9)
    page_number_text = "%d" % (doc.page)
    canvas.drawCentredString(
        PAGE_WIDTH / 2,
        0.5 * inch,
        page_number_text
    )
    canvas.restoreState()


def line():
    style = TableStyle([
        ("LINEABOVE", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ])
    t = Table([""], colWidths=PAGE_WIDTH - 150, rowHeights=0.2 * inch)
    t.setStyle(style)

    # Report.append(t)
    return t


def spacer():
    # Report.append(Spacer(1,0.2*inch))
    return Spacer(1, 0.2 * inch)


def title(txt):
    # Report.append()
    # line()
    return Paragraph(txt, H1), line()


def subtitle(txt):
    # Report.append()
    return Paragraph(txt, H2)


def subsubtitle(txt):
    return Paragraph(txt, H3)


def summary(aoi_name, date):
    data = [
        ['Area of Interest', ': ' + aoi_name, ''],
        ['Date', ': ' + str(date), ''],
    ]

    i = Table(data,
              colWidths=150,
              repeatRows=1,
              )
    # Report.append(i)
    # spacer()
    return i, spacer()


def image_info(info):
    data = [
        ['Scene Id', ': ' + str(info['scene_id']), ''],
        ['Acquired Time', ': ' + str(info['acquired']), ''],
        ['Number of Ships', ': ' + str(info['num_ship']), ''],
    ]

    i = Table(data,
              colWidths=150,
              )
    # Report.append(i)
    # spacer()
    return i, spacer()


def table(data):
    t = Table(data,
              # colWidths=(PAGE_WIDTH-150)/(len(data[0])),
              repeatRows=1,
              )

    t.setStyle(TableStyle([('ALIGN', (0, 0), (2, -1), 'LEFT'),
                           ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('GRID', (0, 0), (-1, -1), 0.5, DARK),
                           ('ROWBACKGROUNDS', (0, 0), (-1, -1), [LIGHT, WHITE]),
                           ('BACKGROUND', (0, 0), (-1, 0), DARK),
                           ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
                           ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')
                           ]))

    # Report.append(t)
    return t


def image_resizer(image, image_width, image_height, max_width, max_height):
    image_ratio = image_width / image_height
    frame_ratio = max_width / max_height
    if image_ratio > frame_ratio:
        # keep width, resize height
        new_width = max_width
        new_height = round(new_width / image_ratio)
    else:
        new_height = max_height
        new_width = round(new_height * image_ratio)
    # print(new_height, new_width)
    # return transform.resize(image, (new_height, new_width, image.shape[2]), preserve_range=False)
    return (new_height, new_width)


def image(image, manifactor=2):
    # image = io.imread(path)
    # print(PAGE_HEIGHT, PAGE_WIDTH)
    # print(image.shape)
    image_height = image.shape[0]
    image_width = image.shape[1]
    max_width = 430
    max_height = 680
    if image_height > max_height or image_width > max_width:
        new_height, new_width = image_resizer(image, image_width, image_height, max_width, max_height)
        resized_image = transform.rescale(image / 255., scale=max(
            [manifactor * new_height / image_height, manifactor * new_width / image_width]), preserve_range=True)
    else:
        resized_image = image
        new_height = image_height
        new_width = image_width
    x = tempfile.NamedTemporaryFile()
    io.imsave(x.name + '.png', resized_image)
    im = Image(x.name + '.png', width=new_width, height=new_height)

    # im = Image(path, width=new_width, height=new_height)
    return im, spacer()


def image_file(path):
    with rasterio.open(path) as src:
        image = src.read()
        image = np.transpose(image, (1, 2, 0))
    # print(PAGE_HEIGHT, PAGE_WIDTH)
    # print(image.shape)
    image_height = image.shape[0]
    image_width = image.shape[1]
    max_width = 430
    max_height = 680
    if image_height > max_height or image_width > max_width:
        # resized_image = image_resizer(image, image_width, image_height, max_width, max_height)
        new_height, new_width = image_resizer(image, image_width, image_height, max_width, max_height)
    x = tempfile.NamedTemporaryFile()
    io.imsave(x.name + '.png', image)
    im = Image(x.name + '.png', width=new_width, height=new_height)

    # im = Image(path, width=new_width, height=new_height)
    return im, spacer()


def build_report(report_parts, output_name):
    pdf = SimpleDocTemplate(output_name, author='Skymap Global')
    pdf.build(report_parts, onFirstPage=footer, onLaterPages=footer)
