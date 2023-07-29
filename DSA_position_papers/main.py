import PyPDF2
import os
import re
import pandas as pd
import pytesseract
from pdf2image import convert_from_path


def extract_text_from_pdf(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        text += page_obj.extract_text()
    pdf_file_obj.close()
    return text


def get_files_from_folder(folder_name):
    links_list = []
    folders = os.listdir(os.getcwd() + '/' + folder_name)
    for folder in folders:
        link = os.getcwd() + '/Task_2_DSA_position_papers/' + folder
        for folder_path, folders, files in os.walk(link):
            for file in files:
                if '.pdf' in file:
                    links_list.append(link + '/' + file)
    return links_list


def clean_text(text):
    text = text.strip()
    text = re.sub('\n', '', text)
    return text


def extract_text_from_image(pdf_path):
    text = ''
    pages = convert_from_path(pdf_path)
    for i, page in enumerate(pages):
        text_tmp = pytesseract.image_to_string(page)
        text += text_tmp
    return text

def collect_text_from_PDF(paths):
    data_list = []
    for i, pdf_path in enumerate(paths):
        print(i)
        try:
            text_pdf = extract_text_from_pdf(pdf_path)
            if len(text_pdf) < 1500:
                text_pdf = extract_text_from_image(pdf_path)
            if not text_pdf:
                raise ValueError("No text extracted from PDF")
        except:
            text_pdf = extract_text_from_image(pdf_path)
        finally:
            data_list.append({'link': pdf_path,
                              'file_name': pdf_path.split('/')[-1],
                              'folder': pdf_path.split('/')[-2],
                              'text': clean_text(text_pdf)})
    return data_list

def add_spaces_to_text(text):
    # Add spaces after punctuation marks and before capitalized words
    text_with_spaces = re.sub(r'([.!?,:;])(\w)', r'\1 \2', text)
    text_with_spaces = re.sub(r'(\w)([A-Z])', r'\1 \2', text_with_spaces)
    return text_with_spaces

pdf_paths = get_files_from_folder('Task_2_DSA_position_papers')
text_list = collect_text_from_PDF(pdf_paths)
text_df = pd.DataFrame(text_list)

text_df['len'] = [len(text) for text in text_df.text]
add_spaces_to_text(text_df.text[0])

text_df.to_csv('DSA_position_paper_improved.csv')