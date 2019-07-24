import glob
import cv2
import pytesseract
import pdf2image
import pandas as pd
import os

path_project = os.path.dirname(os.path.abspath(__file__))

def save_img(images, filename):
    index = 1
    filename = filename.split('\\')[-1].split('.')[0]
    for image in images:
        image.save("data/img/" + filename + "_" + str(index) + ".jpg", "JPEG")
        index += 1


def extract_data(data, keys):
    for key in keys:
        if len(data.split(key)) >= 2:
            return data.split(key)[1]
    return None


def extract_invoice(data):
    number = extract_data(data, ['B.D.S', 'B.DS'])
    number = number.split('\n')[0].strip().replace('.','') if number is not None else None
    date = extract_data(data, ['Date'])
    date = date.split('\n')[0].strip()[1:].strip().split(' ')[0] if date is not None else None
    consignee = extract_data(data, ['Consignee', 'Gonsignee'])
    consignee = consignee.split('\n')[0].strip()[1:].strip() if consignee is not None else None
    price = extract_data(data, ['TOTAL'])
    price = price.split('\n')[0].strip().split(' ')[-1] if price is not None else None
    return {'number': number, 'invoice_date': date, 'consignee': consignee, 'price': price}


def extract_entry(data):
    entry_no = data.split('0735553001939')[1].split('\n')[0].strip().split(' ')[-1]
    print(entry_no)


def open_csv(path_pdf):
    print(path_project + "/result/" + path_pdf + ".csv")
    if os.path.isfile(path_project + "/result/" + path_pdf + ".csv"):
        csv = pd.read_csv(path_project + "/result/" + path_pdf + ".csv", index_col=0)    
    else:
        csv = pd.DataFrame([], columns = ['number', 'invoice_date', 'consignee', 'price', 'entry_no', 'entry_date', 'exchange', 'out_unit', 'out_price', 'thai_price'])
        csv.set_index('number', inplace=True)
    return csv


def record_extract(csv, extract):
    if extract['number'] in csv.index:
        extract = pd.DataFrame.from_records([extract])
        extract.set_index('number', inplace=True)
        csv.update(extract)
    else:
        column_list = ['number', 'invoice_date', 'consignee', 'price', 'entry_no', 'entry_date', 'exchange', 'out_unit', 'out_price', 'thai_price']
        extract = { x: extract[x] if x in extract else None for x in column_list }
        extract = pd.DataFrame.from_records([extract])
        extract.set_index('number', inplace=True)
        csv.update(extract)
        csv = pd.concat([csv, extract])
    print(csv)
    return csv


if __name__ == '__main__':
    # path_pdf = "2016-June"
    path_pdf = "2016-June-Invoice"
    csv = open_csv(path_pdf)
    for pdf_file in glob.glob(path_project + "/data/" + path_pdf + "/*.pdf"):
        print("------------------------------------------------------------------------------------------------")
        print(pdf_file)
        images = pdf2image.convert_from_path(pdf_file, dpi=600, fmt="jpg")
        # save_img(images, pdf_file)
        for image in images:
            data = pytesseract.image_to_string(image, lang='tha+eng+osd')
            if 'INVOICE' in data or'Invoice' in data or 'invoice' in data:
                data = pytesseract.image_to_string(image, lang='eng+osd')
                print("INVOICE")
                extracted = extract_invoice(data)
                csv = record_extract(csv, extracted)
            elif 'ขาออก' in data:
                print("ENTRY")
                extract_entry(data)
            else:
                print("Not Found")
        print("------------------------------------------------------------------------------------------------")

    csv.to_csv (path_project + "/result/" + path_pdf + ".csv", index=True, header=True)    