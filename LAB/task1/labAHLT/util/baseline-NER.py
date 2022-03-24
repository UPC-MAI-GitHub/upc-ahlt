#! /usr/bin/python3
import sys
from os import listdir,system
import re

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize

import evaluator
import pandas as pd 
CHEAT_PATH = "/Users/Eric/Documents/Uni/Msc/Courses/Sem2/AHLT/LAB/task1/labAHLT/data/drugs.csv"
df = pd.read_csv(CHEAT_PATH)
dd = dict(zip(df.comp.values,df.type.values))

## adding a specific path 
PATH = "/Users/Eric/Documents/uni/msc/courses/Sem2/AHLT/LAB/task1/labAHLT"
## dictionary containig information from external knowledge resources
## WARNING: You may need to adjust the path to the resource files
external = {}
with open(PATH + "/resources/HSDB.txt") as h :
    for x in h.readlines() :
        external[x.strip().lower()] = "drug"

with open(PATH + "/resources/DrugBank.txt") as h :
    for x in h.readlines() :
        (n,t) = x.strip().lower().split("|")
        external[n] = t

        
## --------- tokenize sentence ----------- 
## -- Tokenize sentence, returning tokens and span offsets

def tokenize(txt):
    offset = 0
    tks = []
    for t in word_tokenize(txt):
        offset = txt.find(t, offset)
        tks.append((t, offset, offset+len(t)-1))
        offset += len(t)
    return tks

## check if the name contains special symbols 
def check_chemical_name(some_text:str) -> str:
    """Function which checks whether a text contains"""

## -----------------------------------------------
## -- check if a token is a drug part, and of which type
## --------------------- ADDED STUFF
greek_prefix = ["hemi","mono",
                "di","tri",
                "tetra","penta",
                "hexa","hepta",
                "octa","nona",
                "deca"]
## Metallic Names 
metal_names = ["cuprous","cupric",
               "ferrous","ferric",
               "mercurous","mercuric",
               "stannous","stannic"]
## Non-metal suffixes 
non_metal_names = ["ide"]
## Others
oxyanion = ['ite','ate']
## Bonds 
bonds = ["ene",'yne']
## functional groups 
func_groups = [
               "carboxy","carbamoyl",
               "chloroformyl","hydroxy",
               "formyl","oxo","alkyl",
               "alkoxy","epoxy","halo",
               "amine","cyano","nitro","nitroso",
               "azo","sulpho","alkyl thio","mercapto"
               ]
## functional group suffixes 
func_g_suffix = [
                "oic","amide","oyl","chloride","acid",
                "ol","al","one","carboxylate","amine","nitrile",
                "sulphonic","thiol"
                ]
## other names 
other_names2 = ["meth","eth","methyl","ethyl","yl"]
org_prefix = ["meth","eth","prop",
                  "but","pent","hex",
                  "hept","oct","non","dec"]
## bring them all together 
tmp_list = [greek_prefix,
            metal_names,non_metal_names,
            oxyanion,
            bonds,
            func_groups,
            func_g_suffix,other_names2,org_prefix]
## merging & making into a set
full_list = set(sum(tmp_list, []))
## --------------------- END OF ADDED STUFF
suffixes = ['azole', 'idine', 'amine', 'mycin']

def classify_token(txt):
    ## set up the counter 
    cnt = 0
    for something in full_list: 
        if something in txt: 
            cnt+1
    ## other rules 
    starts_with_digit = txt[:1].isdigit()
    ## contains numbers?
    contains_number = any(char.isdigit() for char in txt)
    ## does it contain hyphens?
    contain_hyphen = ("-" in txt)
    ## contains parenthesis
    contain_parenthesis = ("(" in txt) and (")" in txt)
    ## does it contain a comma?
    contain_comma = ("," in txt)
    ## final values 
    val = (starts_with_digit+contains_number+contain_hyphen+contain_parenthesis+contain_comma)
    ## cheat a little bit 
    #if txt in dd: return dd[txt]
   # WARNING: This function must be extended with 
   #          more and better rules

    if txt.lower() in external : return external[txt.lower()]
    elif txt.isupper() : return "brand"
    elif txt[-5:] in suffixes : return "drug"
    elif contains_number and contain_hyphen and contain_parenthesis:
        return "drug"
    elif val >= 3 and cnt>=1: 
        return "drug"
    else : return "NONE"

   

## --------- Entity extractor ----------- 
## -- Extract drug entities from given text and return them as
## -- a list of dictionaries with keys "offset", "text", and "type"

def extract_entities(stext) :

    # WARNING: This function must be extended to
    #          deal with multi-token entities.
    
    # tokenize text
    tokens = tokenize(stext)
         
    result = []
    # classify each token and decide whether it is an entity.
    for (token_txt, token_start, token_end)  in tokens:
        drug_type = classify_token(token_txt)
        
        if drug_type != "NONE" :
            e = { "offset" : str(token_start)+"-"+str(token_end),
                  "text" : stext[token_start:token_end+1],
                  "type" : drug_type
                 }
            result.append(e)
                    
    return result
      
## --------- main function ----------- 

def nerc(datadir, outfile) :
   
    # open file to write results
    outf = open(outfile, 'w')

    # process each file in input directory
    for f in listdir(datadir) :
      
        # parse XML file, obtaining a DOM tree
        tree = parse(datadir+"/"+f)
      
        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences :
            sid = s.attributes["id"].value   # get sentence id
            stext = s.attributes["text"].value   # get sentence text
            
            # extract entities in text
            entities = extract_entities(stext)
         
            # print sentence entities in format requested for evaluation
            for e in entities :
                print(sid,
                      e["offset"],
                      e["text"],
                      e["type"],
                      sep = "|",
                      file=outf)
            
    outf.close()


   
## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir
## --

# directory with files to process
datadir = sys.argv[1]
outfile = sys.argv[2]

nerc(datadir,outfile)

evaluator.evaluate("NER", datadir, outfile)





















