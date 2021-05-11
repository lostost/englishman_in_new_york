from pdf_translate import convert_pdf_to_txt
from pdf_translate_google_api import go_translate

raw = convert_pdf_to_txt('book1.pdf')
translated_raw = go_translate(raw, 'ru')
print(translated_raw)
