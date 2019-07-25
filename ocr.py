import glob
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


def extract_invoice(data, from_file):
    number = extract_data(data, ['B.D.S', 'B.DS'])
    number = number.split('\n')[0].strip().replace('.', '') if number is not None else None
    date = extract_data(data, ['Date'])
    date = date.split('\n')[0].strip()[1:].strip().split(' ')[0] if date is not None else None
    consignee = extract_data(data, ['Consignee', 'Gonsignee'])
    consignee = consignee.split('\n')[0].strip()[1:].strip() if consignee is not None else None
    if consignee:
        consignee_2 = extract_data(data, ['KHLONGSONG'])
        consignee_2 = consignee_2.split('\n')[0].strip()[1:].strip() if consignee_2 is not None else None
    else:
        consignee_temp = extract_data(data, ['Consignee', 'Gonsignee'])
        consignee = consignee_temp.split('\n')[2].strip() if consignee_temp is not None else None
        consignee_2 = consignee_temp.split('\n')[3].strip() if consignee_temp is not None else None
    price = extract_data(data, ['TOTAL'])
    price = price.split('\n')[0].strip().split(' ')[-1] if price is not None else None
    return {'number': number, 'invoice_date': date, 'consignee': consignee, 'consignee_2': consignee_2, 'price': price, 'inv_file': from_file}


def extract_entry(data, from_file):
    # entry_no = data.split('0735553001939')[1].split('\n')[0].strip().split(' ')[-1]
    # print(entry_no)
    temp = extract_data(data, ['# B', '# 8', '# 5', '#B', '#8', '#5'])
    number = temp.split('\n')[0].strip().split('.')[-1].split(',')[-1].split(' ')[0].strip() if temp is not None else None
    entry_date = temp.split('\n')[0].strip().split(' ')[-1].replace(':', '').replace('-', '').strip() if temp is not None else None
    thai_price = data.split('THB')[-1] if len(data.split('THB')) >= 2 else None
    thai_price = thai_price.split('\n')[0].strip().split(' ')[0].strip() if thai_price is not None else None
    if not thai_price:
        thai_price = data.split('THp')[-1] if len(data.split('THB')) >= 2 else None
        thai_price = thai_price.split('\n')[0].strip().split(' ')[0].strip() if thai_price is not None else None
    temp = data.split('THB')[0].split('\n')[-1][-17:]
    out_unit = temp.split('=')[0].strip()
    exchange = temp.split('=')[-1].strip().replace(':', '.')
    out_price = data.split(out_unit)[-1] if len(data.split(out_unit)) >= 2 else None
    out_price = out_price.split('\n')[0].strip().split(' ')[0].strip() if out_price is not None else None
    return {'number': number, 'entry_date': entry_date, 'exchange': exchange, 'out_unit': out_unit, 'out_price': out_price, 'thai_price': thai_price, 'entry_file': from_file}


def open_csv(path_pdf):
    if os.path.isfile(path_project + "/result/" + path_pdf + ".csv"):
        csv = pd.read_csv(path_project + "/result/" + path_pdf + ".csv", index_col=0)
    else:
        csv = pd.DataFrame([], columns=['number', 'invoice_date', 'consignee', 'consignee_2', 'price', 'entry_no', 'entry_date', 'exchange', 'out_unit', 'out_price', 'thai_price', 'inv_file', 'entry_file'])
        csv.set_index('number', inplace=True)
    return csv


def record_extract(csv, extract):
    if extract['number'] in csv.index:
        if 'inv_file' in extract and not csv.isnull()['inv_file'].loc[extract['number']]:
            extract['inv_file'] = csv.loc[extract['number']]['inv_file'] + " / " + extract['inv_file']
        elif 'entry_file' in extract and not csv.isnull()['entry_file'].loc[extract['number']]:
            extract['entry_file'] = csv.loc[extract['number']]['entry_file'] + " / " + extract['entry_file']
        extract = pd.DataFrame.from_records([extract])
        extract.set_index('number', inplace=True)
        csv.update(extract)
    else:
        extract = pd.DataFrame.from_records([extract])
        extract.set_index('number', inplace=True)
        csv = pd.concat([csv, extract], sort=False)
    print(csv)
    return csv


if __name__ == '__main__':
    path_pdf = "2016-June"
    csv = open_csv(path_pdf)
    for pdf_file in glob.glob(path_project + "/data/" + path_pdf + "/*.pdf"):
        print("////////////////////////////////////////////////////////////////////////////////////////////////")
        print(pdf_file)
        images = pdf2image.convert_from_path(pdf_file, dpi=600, fmt="jpg")
        count_page = 0
        # save_img(images, pdf_file)
        for image in images:
            count_page += 1
            print(str(count_page) + " / " + str(len(images)))
            data = pytesseract.image_to_string(image, lang='eng+osd')
            if 'INVOICE' in data or'Invoice' in data or 'invoice' in data:
                print("INVOICE")
                extracted = extract_invoice(data, pdf_file.split('\\')[-1] + "_" + str(count_page))
            else:
                print("ENTRY")
                extracted = extract_entry(data, pdf_file.split('\\')[-1] + "_" + str(count_page))
            csv = record_extract(csv, extracted)
            print("------------------------------------------------------------------------------------------------")
    csv.to_csv(path_project + "/result/" + path_pdf + ".csv", index=True, header=True)
