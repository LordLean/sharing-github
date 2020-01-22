#!/usr/bin/env python
# coding: utf-8

# # NLE Assessed Coursework 3: Question 3
# 
# For this assessment, you are expected to complete and submit 4 notebook files.  There is 1 notebook file for each question (to speed up load times).  This is notebook 3 out of 4.
# 
# Marking guidelines are provided as a separate document.
# 
# In order to provide unique datasets for analysis by different students, you must enter your candidate number in the following cell.

# In[1]:


candidateno=183708 #this MUST be updated to your candidate number so that you get a unique data sample


# In[2]:


#preliminary imports
import sys
sys.path.append(r'\\ad.susx.ac.uk\ITS\TeachingResources\Departments\Informatics\LanguageEngineering\resources')
#sys.path.append(r'/Users/juliewe/resources')
import re
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from itertools import zip_longest
from sussex_nltk.corpus_readers import ReutersCorpusReader
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import math
import spacy
nlp=spacy.load('en')
from nltk.corpus import gutenberg

import operator


# ## Question 3: Named Entity Recognition and Linking (25 marks)
# 
# The code below will run the SpaCy system on the text from Persuasion by Jane Austen.  `mysample` contains a 50% sample which is unique to your candidate number.

# In[3]:


#Do NOT change the code in this cell.

#preparing corpus

def clean_text(astring):
    #replace newlines with space
    newstring=re.sub("\n"," ",astring)
    #remove title and chapter headings
    newstring=re.sub("\[[^\]]*\]"," ",newstring)
    newstring=re.sub("VOLUME \S+"," ",newstring)
    newstring=re.sub("CHAPTER \S+"," ",newstring)
    newstring=re.sub("\s\s+"," ",newstring)
    #return re.sub("([^\.|^ ])  +",r"\1 .  ",newstring).lstrip().rstrip()
    return newstring.lstrip().rstrip()


def get_sample(sentslist,seed=candidateno):
    random.seed(seed)
    random.shuffle(sentslist)
    testsize=int(len(sentslist)/2)
    return sentslist[testsize:]
    
persuasion=clean_text(gutenberg.raw('austen-persuasion.txt'))
nlp_persuasion=list(nlp(persuasion).sents)

mysample=get_sample(nlp_persuasion)


# In[4]:


type(mysample[0])


# ## Part A

# a) **Write code** and **extract**:
# * the 30 most common strings referring to PEOPLE in `mysample`.
# * the 30 most common strings referring to PLACES in `mysample`.
# 
# \[6 marks\]

# `make_tag_lists()` takes a list of sentences as it's parameter and returns three lists of equal length. For any index i of the lists it will return the token/word itself and that words named entity tag. <br> These returned lists are for use with the `extract_entities()`. This function takes those lists as its parameters along with a specified tag-type. It iterates through both lists using enumerate (as they are indexed identically) and returns a dictionary of chunks which match the passed tag-type parameter, displayed as word : frequency.  

# In[5]:


def make_tag_lists(sentences):
    
    tokens = list()    
    ner = list()   
    
    for sent in sentences: 
        for word in sent: 
            tokens.append(word.text)
            ner.append(word.ent_type_)
            
    return tokens,ner

def extract_entities(tokenlist,taglist,tagtype): 
    
    entities = dict()   
    inentity = False 
    
    for i,(token,tag) in enumerate(zip(tokenlist,taglist)): 
        if tag==tagtype:          
            if inentity:              
                entity+=" "+token  
            else:         
                entity=token      
                inentity=True     
        elif inentity:   
            entities[entity]=entities.get(entity,0)+1   
            inentity=False 
            
    return entities


# In[6]:


def extract(tokenlist,taglist,tagtype):
    
    ent = dict()
    
    for i, (token,tag) in enumerate(zip(tokenlist,taglist)):
        if tag==tagtype:
            ent[token] = ent.get(token,0) + 1
            
    return ent


# The two cells below show the 30 most common strings referring to the specified tag-types in `mysample`. In regards to "PLACES" I felt as if it was ambigious whether this was refering to geopolitical entities such as countries etc. or locations and as displaying both gives more data to reference from for the next question, both were included.

# In[7]:


toks,ner=make_tag_lists(mysample)

people = extract_entities(toks,ner,"PERSON")
places = extract_entities(toks,ner,"GPE")
nonGPE = extract_entities(toks,ner,"LOC")

top_people=sorted(people.items(),key=operator.itemgetter(1),reverse=True)[:30]
top_places=sorted(places.items(),key=operator.itemgetter(1),reverse=True)[:30]
top_nonGPE=sorted(nonGPE.items(),key=operator.itemgetter(1),reverse=True)[:30]


# In[8]:


print("PEOPLE",top_people)
print("")
print("PLACES",top_places)
print("")
print("LOCATIONS",top_nonGPE)


# In[9]:


df_people = pd.DataFrame(top_people, columns = ["PEOPLE", "Frequency"])
df_GPE = pd.DataFrame(top_places, columns = ["PLACES_GPE", "Frequency"])
df_nonGPE = pd.DataFrame(top_nonGPE, columns = ["PLACES_nonGPE", "Frequency"])

pd.concat([df_people, df_GPE, df_nonGPE], axis = 1)


# ## Part B

# b) Making reference to specific examples from the text in `mysample`, **discuss** the different types of errors made by the named entity recogniser. \[6 marks\]

# spaCy default models trained on web text for general all-purpose use. For specific cases like English literature model should be customized further. Predictions are of course based on the data it is trained on.
# <br><br>
# Refering to the table of most common strings above we can easily spot various mistakes: 
# * Captain Wentworth being labeled as a LOC. This may have been due to fewer tokens being pulled than desired, i.e. it should have been Captain Wentworth's. The String Captain also had this. If these incorrect tokens had been merged under the LOC of Captain Wentworth's it would have been the most frequently occuring String of this entity type. <br> There is also the chance they were mislabelled even further and prehaps were not refering to the place but the person.
# <br><br>
# * Vague was incorrectly labeled as a GPE type however there is no area or location under that name in Persuasion. This most likely will be due to the surrounding tokens being of a similar format to the surroundings of a genuine GPE.
# <br><br>
# * The PERSON category shows the most mistakes. The String "Elliot" features as the 2nd most occuring of all PERSON entity types. Which of the Elliot family this tag refers to is hard to tell without the surrounding context. Once again another example of fewer tokens being evaluated than desired to make accurate predictions. The Strings "Anne Elliot" and "Miss Anne" most likely refer to our most common PERSON String "Anne" however were included as seperate. The amount of "Anne" occurences would have been largely increased if "Anne" was the wrapper String for all these variations. Likewise with "Walter Elliot" and  "Walter" and "Wentworth" and "Captain Wentworth" etc.
# <br><br> 
# * "secret,)--" from the sentence "Sir Walter's concerns could not be kept a secret,)-- accidentally hearing" may have been mislabeled due to the preceding "a" or prehaps confusion caused by the ",)--" after.
# <br><br>One possible fix is to extract these mis-labeled entity predictions, correct them and then add to training data. Or prehaps even confirm correctly labeled entities to avoid catastrophic interference.

#  

# ## Part C

# c) **Design** and **implement** a system to track the locations of characters throughout the story.  For a given PERSON named entity, your system should return a list of time-ordered LOCATIONS for that character.  Test your system using the complete text of "Persuasion" (**not** `mysample`) for at least 3 major characters.   \[13 marks\]

# **Initial thoughts:**
# * Input: Takes a name parameter: `finder(name)`  i.e `finder("Anne")`.
# * Output: A list of lists with each inner list containing the passed name and the words in that sentence tagged with the entity type "GPE" for geopolitical entity (prehaps LOC as well however this option will be explored to see how much it adds to the time ordered location list).

# In[10]:


def finder(name):

    new_list = list()

    for sentence in nlp_persuasion:
        
        sent_list = list()

        for i, word in enumerate(sentence):
            
            if word.ent_type_ == "PERSON" and word.text == name and name not in sent_list:
                sent_list.append(word.text)
            if word.ent_type_ == "GPE":
                sent_list.append(word.text)
            if word.ent_type == "LOC":
                sent_list.append(word.text)
                        
        if name in sent_list and len(sent_list) != 1: #Check if name is in list and != 1 as name at least will appear.
            new_list.append(sent_list)

    return new_list

finder("Anne")


# **Alterations:**
# * Location (LOC) could be removed as one of the conditionals due to mislabeling of data or ambiguity due to Persuasion being a piece of fiction and certain LOC entity types did not refer to actual locations the chosen character was in - For example `Captain Wentworth` being labed under LOC was a confusion due to `Captain Wentworth's` (place) and so it was outputing imformation that meant a character was with the person Wentworth rather than at their place. 
# * Add in a neighbouring features conditional; whilst average sentence length is ~26.7 words there is huge variance with the largest sentence being 227 words long. E.g the mention of "Anne" at the start of a sentence and "London" being the 227 word in that sentence tells us less than a GPE word would at a closer distance. Implement a window parameter to specify GPE locations within that window distance from name in the sentence.
# * Including name in every sentence list is unnecessary - can just be added in at the end of the final list to specify. 
# * More useful to include the index of the sentence it pulled data from so correctness can be checked by hand.
# <br>
# 
# * Input: `name` parameter to specify character and `window` with a default of 100 words to measure distance from "name" word in sentence.
# * Output: A list of lists with inner lists containing sentence index and all GPE entity types of that sentence within that window. "name" appended to end of final list for clarity.

# In[11]:


def finder_v2(name, window = 100):

    new_list = list()
    sentence_counter = 0

    for sentence in nlp_persuasion:
        
        sent_list = list()
        sent_list.append(sentence_counter)

        for i, word in enumerate(sentence):
            
            if word.ent_type_ == "PERSON" and word.text == name and name not in sent_list:
                sent_list.append(word.text)
            if word.ent_type_ == "GPE" and (name in sentence[max(0,i-window):i].text or name in sentence[i+1:i+window+1].text):
                sent_list.append(word.text)
                
        sentence_counter += 1
        
        if name in sent_list and len(sent_list) > 2:
            sent_list.remove(name)
            new_list.append(sent_list)

    new_list.append(name)
    
    return new_list


# Below is an example output of the `finder()` function. 20 words either side of name occurences seemed a good estimate to still contain useful GPE types. Of course 226 would definately contain every GPE tagged words although under testing length of output remained the same once 98 was passed (for top 5 characters):

# In[12]:


finder_v2("Anne", 20)


# `length_calc()` as seen below takes a number of characters (starting from the most mentioned character) and works out the minimum window value that needs to be passed to `num_of_characters()` to include every instance of name (PERSON type) occuring in the same sentence as a place (GPE type) for that amount of characters.
# <br>E.g. Including 5 characters the window value that needs to be passed is 98.

# In[13]:


def length_calc(num):
    
    length_list = list()
    
    for ppl in top_people[:num]:
    
        maximum = len(finder_v2(ppl[0],226))
        current = 0

        for i in range(226):        
            if maximum == len(finder_v2(ppl[0],i)):
                current = i
                break

        length_list.append(current)

    return max(length_list)
        

length_calc(5)


# `num_of_characters()` displays the time ordered locations of however many characters are passed through to the parameter num. It can be given a window parameter of type int however if none is passed it will automatically use `length_calc()` to calculate the value needed to show all possible datasets.

# In[14]:


def num_of_characters(num, window = None):
    
    ppl_list = list()
    
    if window == None:
        window = length_calc(num)
        
    for ppl in top_people[:num]:
        ppl_list.append(finder_v2(ppl[0], window))
    
    return ppl_list

num_of_characters(5)


# In[15]:


def sentence_finder(name):
    
    for i in range(len(finder_v2(name)) - 1):
        sentence_index = finder_v2(name)[i][0]
        print(nlp_persuasion[sentence_index])
        print(" ")
        
sentence_finder("Mary")


# Below code to calculate maximum sentence length and average sentence length. 

# In[16]:


average = list()
for sentence in nlp_persuasion:
    average.append(len(sentence))
print("Maximum sentence length is: " + str(max(average)))
print("Average sentence length is: " + str(sum(average)/len(average)))


# Commented Out Code:

# In[17]:


# def finder(name):
    
#     listy = list()
#     window = 3
    
#     for i in range(len(nlp_persuasion)):
        
#         sentence_list = list()
        
#         for word in nlp_persuasion[i]:
            
#             if word.ent_type_ == "PERSON" and word.text == name and name not in sentence_list:
               
#                 sentence_list.append(word.text)
                
#             if word.ent_type_ == "GPE":
#                 sentence_list.append(word.text)
                
#         if name in sentence_list and len(sentence_list) > 1:
#             listy.append(sentence_list)
                
#     return listy

# finder("Anne")

