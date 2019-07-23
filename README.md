# Invoice OCR
Invoice OCR Project: To extract important data of Invoice and Import-Export Entry like Number, Consignee, Date, Price, Exchange Rate

### Requirement
- Python 2.7+ or 3.x
- PDF2Image [Link] (https://pypi.org/project/pdf2image/)
- Tesseract OCR [Link] (https://github.com/tesseract-ocr/tesseract)
- PyTesseract [Link] (https://pypi.org/project/pytesseract/#description)

### Installation
First, 
- Install Tesseract OCR [Link] (https://github.com/tesseract-ocr/tesseract)
- Install Poppler : For Window [Link] (http://blog.alivate.com.au/poppler-windows/) and add `bin/` folder to `PATH`. , Linux: `sudo apt install poppler-utils`
```
pip install pytesseract 
pip install pdf2image 
pip install pandas
```
OR
```
pip install -r requirements.txt
```

### Usage
