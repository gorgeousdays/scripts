import PyPDF2
import os

left_margin = 50
right_margin = 40
top_margin = 230
bottom_margin = 235
def split(page):
    page.mediaBox.lowerLeft = (left_margin, bottom_margin)
    page.mediaBox.lowerRight = (width - right_margin, bottom_margin)
    page.mediaBox.upperLeft = (left_margin, height - top_margin)
    page.mediaBox.upperRight = (width - right_margin, height - top_margin)

input_file = PyPDF2.PdfFileReader(open("input.pdf", 'rb'))
output_file = PyPDF2.PdfFileWriter()
page_info = input_file.getPage(0)
width = float(page_info.mediaBox.getWidth())
height = float(page_info.mediaBox.getHeight())
page_count = input_file.getNumPages()

this_page = input_file.getPage(0)
split(this_page)
output_file.addPage(this_page)

output_file.write(open("output.pdf", 'wb'))
