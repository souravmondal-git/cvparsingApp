from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
import mammoth
import io
import os
import nltk
import re


def extract_pdf(path):
    resource_manager = PDFResourceManager()
    output = io.StringIO()
    text_converter = TextConverter(resource_manager, output, laparams=LAParams())
    interpreted_page = PDFPageInterpreter(resource_manager, text_converter)
    with open(path, 'rb') as file:
        for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
            interpreted_page.process_page(page)
            text = output.getvalue()
    text_converter.close()
    output.close()

    return text


def read_file(filename):
    if (filename.endswith(".pdf")):
        try:
            fileTEXT = extract_pdf(filename)
        except Exception:
            print('Error raised reading the pdf file:' + filename)

    elif (filename.endswith(".docx")):
        try:
            with open(filename, "rb") as docx_file:
                result = mammoth.extract_raw_text(docx_file)
                fileTEXT = result.value
        except IOError:
            print('Error raised reading the docx file:' + filename)

    elif (filename.endswith(".doc")):
        try:
            fileTEXT = textract.process(filename).decode('utf-8')
        except Exception:
            print('Error raised reading the doc file:' + filename)

    elif (filename.endswith(".txt")):
        try:
            text_file = open(filename, "rt")
            fileTEXT = text_file.read()
        except Exception:
            print('Error raised reading the txt file:' + filename)
    else:
        print(filename + 'not supported!')

    return fileTEXT

def email_ids(text):
    pattern_email = re.compile(r'[A-Za-z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    email_objs = pattern_email.findall(str(text))
    email_objs = list(set(email_objs))
    return email_objs


def phone_number(text):
    pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')

    pt = pattern.findall(text)
    pt = [re.sub(r'[,.]', '', ah) for ah in pt if len(re.sub(r'[()\-.,\s+]', '', ah)) > 9]
    pt = [re.sub(r'\D$', '', ah).strip() for ah in pt]
    pt = [ah for ah in pt if len(re.sub(r'\D', '', ah)) <= 15]
    for ah in list(pt):

        if len(ah.split('-')) > 3: continue
        for x in ah.split("-"):
            try:
                if x.strip()[-4:].isdigit():
                    if int(x.strip()[-4:]) in range(1900, 2100):
                        pt.remove(ah)
            except:
                pass
    number = None
    number = list(set(pt))
    return number

def find_contact_info(filename):
    text = read_file(filename)
    email = ",".join(email_ids(text))
    phone = ",".join(phone_number(text))
    return {'Email-ids':email, 'Phone Numbers':phone}
