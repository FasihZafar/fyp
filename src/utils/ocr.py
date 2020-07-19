# import pytesseract as pt
# import pdf2image
# import os
# import concurrent.futures
# import sys

# data_dir = os.path.join(os.getcwd(), 'data')
# files = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

# for file in files:
#     print(file)
#     pages = pdf2image.convert_from_path( file, dpi=300, thread_count=sys.maxsize)
#     print('pdf2image done')
#     text = [ pt.image_to_string( page, lang="eng", config="--psm 10 --psm 11 --psm 6 -c preserve_interword_spaces=1")  for page in pages ]
#     print('pytesseract done')
#     text = "\n".join(text)
#     text = text.lower()
#     with open(file+".txt", 'w') as fh:
#         fh.writelines(text)

