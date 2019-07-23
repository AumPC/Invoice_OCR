import glob
import cv2
import pytesseract
import pdf2image


def save_img(images, filename):
    index = 1
    filename = filename.split('\\')[-1].split('.')[0]
    for image in images:
        image.save("data/img/" + filename + "_" + str(index) + ".jpg")
        index += 1


def extract_invoice(data):
    number = data.split('B.D.S')[1].split('\n')[0].strip().replace('.','')
    consignee = data.split('Consignee')[1].split('\n')[0].replace(':','').strip()
    price = data.split('TOTAL')[1].split('\n')[0].replace('CNF','').replace('()','').strip()
    print(number)
    print(consignee)
    print(price)
    return number, consignee, price


if __name__ == '__main__':
    # path_pdf = "data/300DPI/2016-June/"
    path_pdf = "data/300DPI/2016-June-Invoice/"
    for pdf_file in glob.glob("D:\Project\Invoice_OCR/" + path_pdf + "*.pdf"):
        print("------------------------------------------------------------------------------------------------")
        print(pdf_file)

        images = pdf2image.convert_from_path(pdf_file, dpi=300, fmt="jpg")
        # save_img(images, pdf_file)

        for image in images:
            data = pytesseract.image_to_string(image, lang='tha+eng')
            if 'INVOICE' in data or'Invoice' in data or 'invoice' in data:
                print("INVOICE")
                extract_invoice(data)
            else:
                print("ENTRY")
                # extract_entry(data)

        # get_ocr_text()
        print("------------------------------------------------------------------------------------------------")