from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, LTChar
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import os

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos):
        interpreter.process_page(page)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

def parse_problems():
    path = "./exam_prob/"
    filenames = [filename for filename in os.listdir(path) if filename != '.DS_Store']
    filename = filenames[0]
    text = convert_pdf_to_txt(path+filename)
    lines = [line for line in text.split('\n') if len(line) > 0]

    keywords = ['Problem', 'Section']
    for i in range(26):
        keywords.append('{}. '.format(i))
        keywords.append('({})'.format(chr(ord('a') + i)))
    sub_keywords = ['pts', 'points']
    problem, problems = [], []
    for line in lines:
        new_prob = False
        for keyword in keywords:
            if keyword in line:
                new_prob = True
        if new_prob:
            problems.append(problem)
            problem = []
        problem.append(line)

    problems.append(problem)
    return problems

if __name__ == "__main__":
    problems = parse_problems()
    import ipdb; ipdb.set_trace()
