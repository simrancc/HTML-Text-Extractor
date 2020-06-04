from bs4 import BeautifulSoup
import spacy
import re
import sys
import html2text
import os

class PrivacyPolicy(object):

    def __init__(self, html) :
        self.html = html
        with open(html) as infile:
            self.inputSoup = BeautifulSoup(infile, features="html.parser")
            #print("######################################")
            #print(self.inputSoup.prettify())
            #print("######################################")
        self.removed_strings = []
        self.listAvg = 0
        self.paragraphAvgLength = 0
        self.listElements = ['li', 'ul', 'ol']


    def print_plain_text(self, html) :
        html = open(html).read()
        print(html2text.html2text(html))


    def output_plain_text(self, html, outputFileName) :
        # Open your file
        with open(html, 'r') as f_html:
            html = f_html.read()
        # Open a file and write to it
        with open(outputFileName, 'w') as f:
            f.write(html2text.html2text(html))


    def getSentence(self, text) :
        nlp = spacy.load('en_core_web_sm')
        ellipsis_doc = nlp(text)
        ellipsis_sentences = list(ellipsis_doc.sents)
        return ellipsis_sentences


    def is_punctuation(self, strings) :
        if ( (strings.rfind(".") != len(strings) - 1 and strings.rfind(".") != len(strings) - 2) and
        (strings.rfind("?") != len(strings) - 1 and strings.rfind("?") != len(strings) - 2) and
        (strings.rfind("!") != len(strings) - 1 and strings.rfind("!") != len(strings) - 2) and
        (strings.rfind(",") != len(strings) - 1 and strings.rfind(",") != len(strings) - 2) and
        (strings.rfind(";") != len(strings) - 1 and strings.rfind(";") != len(strings) - 2) ) :
            return True
        else :
            return False


    def simplify_html(self) :
        #loop through all <p> elements
        #print("######################################")
        #print(self.inputSoup.prettify())
        #print("######################################")
        for x in self.inputSoup.find_all(["p", "b"]):
            print("######################################")
            print(x.contents)
            print("######################################")
            text = str(x.contents[0].string) #get text of <p>
            colon = ":"
            #find <p> that end in a colon
            if (text.rfind(colon) == len(text) - 1 or text.rfind(colon) == len(text) - 2) :
                if ( (type(x.next_sibling) == type(x.contents[0].string) and x.next_sibling.next_sibling is not None and x.next_sibling.next_sibling.name in self.listElements)
                    or (x.next_sibling is not None and x.next_sibling.name in self.listElements) ):
                #for sibling in x.next_siblings:
                    if (x.next_sibling.name in self.listElements) :
                        sibling = x.next_sibling
                    else :
                        sibling = x.next_sibling.next_sibling
                    #if sibling.name in self.listElements:
                    ellipsis_sentences = self.getSentence(text)
                    lastSentence = ellipsis_sentences[len(ellipsis_sentences) - 1]
                    #loop through all the list elements within the <p>
                    for child in sibling.contents:
                         if (type(child) != type(x.contents[0].string)) :
                             strings = child.text
                        #allStrings = sibling.find_all(string=re.compile(child))
                        #for strings in allStrings :
                            #if (strings.parent.name == "li") :
                             if (self.is_punctuation(strings)):
                                strings += "."
                                #create new paragraph element and insert before list
                             new_tag = self.inputSoup.new_tag("p")
                             sibling.insert_before(new_tag)
                             new_tag.string = str(lastSentence) + " " + strings
                            #if parent is not <li> it is not a list element (subtitle, comment, etc.)
                         else :
                             self.removed_strings.append(child)
                    #delete entire bulleted list
                    sibling.extract()
        #print(self.inputSoup.prettify())

    def outputFile(self, html) :
        with open(html, "w") as file:
            file.write(str(self.inputSoup))


    #going to change into heuristic later
    def average_list_length(self) :
        average = 0
        #loop through all <p> elements
        for x in self.inputSoup.find_all("p"):
            text = str(x.contents[0].string)
            colon = ":"
            if (text.rfind(colon) == len(text) - 1 or text.rfind(colon) == len(text) - 2) :
                for sibling in x.next_siblings:
                    #find sibling that is li/ul/ol
                    if sibling.name == "li" or sibling.name == "ul" or sibling.name == "ol" :
                        ellipsis_sentences = getSentence(text)
                        sum = 0
                        #sum up length of all bulleted text
                        for sentence in ellipsis_sentences:
                            sum += len(sentence)
        self.listAvg = sum / len(ellipsis_sentences)
        return self.listAvg


    def average_sentences_in_paragraph(self) :
        average = 0
        count = 0
        #get all <p> elements and loop through
        for x in self.inputSoup.find_all("p"):
            count = count + 1
            text = str(x.contents[0].string)
            ellipsis_sentences = getSentence(text)
            #sum up length of all sentences in one paragraph
            sum += len(ellipsis_sentences)
        self.paragraphAvgLength = sum / count
        return self.paragraphAvgLength


count = 1
for root, dirs, files in os.walk('/Users/simrancc/Downloads/policy_crawl') :
   for name in files:
       count = count + 1
       #print(name)
       #print(root)
       if name == "policy.simple.html" and count < 25:
           print(os.path.join(root, name))
           html = os.path.join(root, name)
           p = PrivacyPolicy(html)
           p.simplify_html()
           completeName = os.path.join(root, "clean.html")
           p.outputFile(completeName)

# html = sys.argv[1]
# p = PrivacyPolicy(html)
# p.simplify_html()
# p.outputFile("output6.html")
#p.output_plain_text("output2.html")
