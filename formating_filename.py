import os
import ipdb; ipdb.set_trace()
path = "./exam_prob/"
for filename in os.listdir(path):
    if not filename.endswith(".pdf"):
        continue
    rename_str = filename
    if filename.startswith("cs70_"):
        rename_str = rename_str[5:]
    if filename.endswith("_mt1.pdf"):
        rename_str = rename_str[:-7] + ".pdf"
    os.rename(path + filename, path + rename_str)
