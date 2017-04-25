from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import logging

root = 'INSERT HERE'
logging.propagate = False
logging.getLogger().setLevel(logging.ERROR)

def split_pdf_into_questions (filename):
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    questions = []
    curr = ''
    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                text = lt_obj.get_text()
                if 'pts' in text.lower() or 'points' in text.lower():
                    if len(curr) > 0:
                        questions.append(curr)
                    curr = text
                else :
                    curr = curr + text
    return questions

def parse_all_questions ():
    names = ['fa01.pdf', 'fa02.pdf','fa03.pdf','fa04.pdf','fa06.pdf',
             'fa14.pdf', 'sp01.pdf', 'sp01.pdf','sp05.pdf', 'sp06.pdf',
             'sp07.pdf','sp08.pdf','sp09.pdf','sp14.pdf','sp16.pdf']
    all_questions = []
    for name in names:
        all_questions.extend(split_pdf_into_questions(root + name))
    return all_questions

def lsa ():
    questions = parse_all_questions()
    vectorizer = TfidfVectorizer()
    doc_matrix = vectorizer.fit_transform(questions)
    lsa_transformer = TruncatedSVD(n_components = 100)
    svd = lsa_transformer.fit_transform(doc_matrix)
    return vectorizer, svd, lsa_transformer

def cluster():
    vectorizer, svd, lsa_transformer = lsa()
    clusters = KMeans(n_clusters=5).fit(svd)
    return clusters

def categorize(filepath, num):
    names = ['fa01.pdf', 'fa02.pdf','fa03.pdf','fa04.pdf','fa06.pdf',
                 'fa14.pdf', 'sp01.pdf', 'sp01.pdf','sp05.pdf', 'sp06.pdf',
                 'sp07.pdf','sp08.pdf','sp09.pdf','sp14.pdf','sp16.pdf']
    classes = ['intro', 'stable marriage', 'other', 'numbers / grab bag', 'induction / proofs']
    if filepath in names:
        questions = split_pdf_into_questions(root + filepath)
        if num <= len(questions):
            question = questions[num - 1]
            #print('Generating Clusters ...')
            clusters = cluster()
            #print('Performing LSA ...')
            vectorizer, svd, lsa_transformer = lsa()
            vectorized = vectorizer.transform([question])
            reduced = lsa_transformer.transform(vectorized)
            return classes[clusters.predict(reduced)[0] - 1]
        else:
            print("ERROR: question not found")
    else:
        print("ERROR: file not found")

def generate_names ():
    txtOutput = open('classes.txt', 'w')
    names = ['fa01.pdf', 'fa02.pdf','fa03.pdf','fa04.pdf','fa06.pdf',
                     'fa14.pdf', 'sp01.pdf', 'sp01.pdf','sp05.pdf', 'sp06.pdf',
                     'sp07.pdf','sp08.pdf','sp09.pdf','sp14.pdf','sp16.pdf']
    classes = ['intro', 'stable marriage', 'other', 'numbers / grab bag', 'induction / proofs']
    vectorizer, svd, lsa_transformer = lsa()
    clusters = cluster()
    for name in names:
        q = split_pdf_into_questions(root + name)
        num_q = len(q)
        for i in range(num_q):
            vectorized = vectorizer.transform([q[i]])
            reduced = lsa_transformer.transform(vectorized)
            prediction = classes[clusters.predict(reduced)[0]]
            txtOutput.write(name + " " + str(i + 1) + ": " + str(prediction))
            txtOutput.write("")
            txtOutput.write('--------------------------------')
            txtOutput.write(q[i])
            txtOutput.write('--------------------------------')
    txtOutput.close()
