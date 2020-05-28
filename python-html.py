from bs4 import BeautifulSoup
import spacy
import re


class PrivacyPolicy(object):

    def __init__(self, html, remove_Array) :
        self.html = html
        with open(html) as fp:
            self.soup = BeautifulSoup(fp, features="html.parser")
        self.removed_strings = remove_Array


    def print_plain_text(self) :
        for strings in self.soup.stripped_strings:
            print(strings)


    def output_plain_text(self) :
        for strings in self.soup.stripped_strings:
            with open("plaintext.html", "w") as file:
                file.write(str(strings))

    def simplifier(self) :
        nlp = spacy.load('en_core_web_sm')
        for x in self.soup.find_all("p"):
            temp = str(x.contents[0].string)
            strr = ":"
            if (temp.rfind(strr) == len(temp) - 1 or temp.rfind(strr) == len(temp) - 2) :
                for sibling in x.next_siblings:
                    if sibling.name == "li" or sibling.name == "ul" or sibling.name == "ol" :
                        ellipsis_doc = nlp(temp)
                        ellipsis_sentences = list(ellipsis_doc.sents)
                        lastSentence = ellipsis_sentences[len(ellipsis_sentences) - 1]
                        allStrings = []
                        for child in sibling.stripped_strings:
                            #print(sibling.find(string=re.compile(child)))
                            #print("############################################")
                            allStrings = sibling.find_all(string=re.compile(child))
                            #print(allStrings)
                        for text in allStrings :
                            print(text)
                            print()
                            if (text.parent.name == "li") :
                                if ( (text.rfind(".") != len(text) - 1 and text.rfind(".") != len(text) - 2) and
                                (text.rfind("?") != len(text) - 1 and text.rfind("?") != len(text) - 2) and
                                (text.rfind("!") != len(text) - 1 and text.rfind("!") != len(text) - 2) ):
                                    text += "."
                                new_tag = self.soup.new_tag("p")
                                x.insert_before(new_tag)
                                new_tag.string = str(lastSentence) + " " + text
                                #print(new_tag.string)
                            else :
                                self.removed_strings.append(text)
                        sibling.extract()
                        x.extract()


    def outputFile(self) :
        with open("output1.html", "w") as file:
            file.write(str(self.soup))
