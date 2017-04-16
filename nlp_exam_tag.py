import PyPDF2
from sklearn.decomposition import LatentDirichletAllocation
pdfFileObj = open('example_exam.pdf','rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pdfReader.numPages
pageObj = pdfReader.getPage(0)
pageObj.extractText()
import ipdb; ipdb.set_trace()
