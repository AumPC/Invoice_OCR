import glob
from PIL import Image
import PyPDF4
import pytesseract

temp_image = "data/temp.png"

def pdf_to_image(pdf_file):
    pdf_data = PyPDF4.PdfFileReader(open(pdf_file, "rb")).getPage(0)
    pdf_page = pdf_data['/Resources']['/XObject'].getObject()
    for name_page in pdf_page:
        page = pdf_page[name_page]
        if page['/Subtype'] == '/Image':
            size = (page['/Width'], page['/Height'])
            data = page.getData()
            mode = "RGB" if (page['/ColorSpace'] == '/DeviceRGB') else "P"
            if page['/Filter'] == '/FlateDecode':
                img = Image.frombytes(mode, size, data)
                img.save(temp_image)
            else:
                img = open(temp_image, "wb")
                img.write(data)
                img.close()
            print(temp_image)
        break


def get_ocr_text():
    print(pytesseract.image_to_string(temp_image, lang='tha+eng'))


if __name__ == '__main__':
    path_pdf = "data/2016-June/"
    for pdf_file in glob.glob("D:\Project\Invoice_OCR/" + path_pdf + "*.pdf"):
        pdf_to_image(pdf_file)
        get_ocr_text()
        # break


