from bs4 import BeautifulSoup
import spacy
import re

nlp = spacy.load('en_core_web_sm')
with open("sephoraPP.html") as fp:
    soup = BeautifulSoup(fp, features="html.parser")
    #print(soup)

removed_strings = []
for x in soup.find_all("p"):
    temp = str(x.contents[0].string)
    strr = ":"
    if (temp.rfind(strr) == len(temp) - 1 or temp.rfind(strr) == len(temp) - 2) :
        for sibling in x.next_siblings:
            if sibling.name == "li" or sibling.name == "ul" or sibling.name == "ol" :
                ellipsis_doc = nlp(temp)
                ellipsis_sentences = list(ellipsis_doc.sents)
                lastSentence = ellipsis_sentences[len(ellipsis_sentences) - 1]
                for child in sibling.stripped_strings:
                    print(child)
                    print("############################################")
                    allStrings = sibling.find_all(string=re.compile(child))
                    for text in allStrings :
                        print(text)
                        print()
                        if (text.parent.name == "li") :
                            if ( (text.rfind(".") != len(text) - 1 and text.rfind(".") != len(text) - 2) and
                            (text.rfind("?") != len(text) - 1 and text.rfind("?") != len(text) - 2) and
                            (text.rfind("!") != len(text) - 1 and text.rfind("!") != len(text) - 2) ):
                                text += "."
                            new_tag = soup.new_tag("p")
                            x.insert_before(new_tag)
                            new_tag.string = str(lastSentence) + " " + text
                            #print(new_tag.string)
                            #print(soup.prettify())
                        else :
                            removed_strings.append(text)
                sibling.extract()
                x.extract()

with open("output1.html", "w") as file:
    file.write(str(soup))
