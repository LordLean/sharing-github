import sys
#sys.path.append(r'\\ad.susx.ac.uk\ITS\TeachingResources\Departments\Informatics\LanguageEngineering\resources')
sys.path.append(r'/Users/alex/resources') 
import nltk
from pandas import * 
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic



df = pd.read_excel(r'/Users/alex/Downloads/test.xlsx', sheetName = "Coding") #insert xlsx
creative = df["Creative"].tolist()
comment = df["Comment"].tolist()

test_list = list()
for i in range(len(comment)):
    test_list.append(word_tokenize(str(comment[i])))


def get_syns(word):

    synonyms = list()
    for syn in wn.synsets(word):
        for l in syn.lemmas():
                synonyms.append(l.name())

    return synonyms

#get_syns('boring')



def gimme_word(tagged_word,tagname):
    
    null_list = list()
    
    for i in range(len(test_list)):
        truth = False
        for word in test_list[i]:
            if word.lower() in get_syns(tagged_word):
                truth = True
        if truth:
            null_list.append(tagname)
        else:
            null_list.append(" ")

    return null_list
    
#gimme_word("boring", "NEG-boring")



import xlwt
from tempfile import TemporaryFile
book = xlwt.Workbook()
sheet1 = book.add_sheet('sheet1')


def convert_to_csv(tagged_word,tagname):

    for i,e in enumerate(gimme_word(tagged_word, tagname)):
        sheet1.write(i,1,e)

    name = tagname + ".xls"
    book.save(name)
    book.save(TemporaryFile())




convert_to_csv("boring", "NEG-test")

