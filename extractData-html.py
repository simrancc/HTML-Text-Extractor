from bs4 import BeautifulSoup
import spacy
import re
import sys
import html2text
import os

class PrivacyPolicy(object):

    def __init__(self, html) :
        self.html = html
        with open(html) as fp:
            self.inputSoup = BeautifulSoup(fp, features="html.parser")
        self.removed_strings = []
        self.listAvg = 0
        self.paragraphAvgLength = 0
        self.nlp = spacy.load('en_core_web_sm')


    def print_plain_text(self, html) :
        html = open(html).read()
        print(html2text.html2text(html))


    def output_plain_text(self, html) :
        # Open your file
        with open(html, 'r') as f_html:
            html = f_html.read()
        # Open a file and write to it
        with open('plaintext.txt', 'w') as f:
            f.write(html2text.html2text(html))


    def simplify_html(self) :
        #loop through all <p> elements
        for x in self.inputSoup.find_all("p"):
            text = str(x.contents[0].string) #get text of <p>
            colon = ":"
            #find <p> that end in a colon
            if (text.rfind(colon) == len(text) - 1 or text.rfind(colon) == len(text) - 2) :
                for sibling in x.next_siblings:
                    if sibling.name == "li" or sibling.name == "ul" or sibling.name == "ol" :
                        ellipsis_sentences = get_sentences(text)
                        lastSentence = ellipsis_sentences[len(ellipsis_sentences) - 1]
                        allStrings = []
                        #loop through all the list elements within the <p>
                        for child in sibling.stripped_strings:
                            allStrings = sibling.find_all(string=re.compile(child))
                            for strings in allStrings :
                                if (strings.parent.name == "li") :
                                    if (is_punctuation(strings)):
                                        strings += "."
                                    #create new paragraph element and insert before list
                                    new_tag = self.inputSoup.new_tag("p")
                                    sibling.insert_before(new_tag)
                                    new_tag.string = str(lastSentence) + " " + strings
                                #if parent is not <li> it is not a list element (subtitle, comment, etc.)
                                else :
                                    self.removed_strings.append(strings)
                        #delete entire bulleted list
                        sibling.extract()

    def outputFile(self) :
        with open("output2.html", "w") as file:
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
                        ellipsis_sentences = get_sentences(text)
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
            ellipsis_sentences = get_sentences(text)
            #sum up length of all sentences in one paragraph
            sum += len(ellipsis_sentences)
        self.paragraphAvgLength = sum / count
        return self.paragraphAvgLength


    def get_sentences(self, text) :
        ellipsis_doc = self.nlp(text)
        ellipsis_sentences = list(ellipsis_doc.sents)
        return ellipsis_sentences


    def is_punctuation(strings) :
        if ( (strings.rfind(".") != len(strings) - 1 and strings.rfind(".") != len(strings) - 2) and
        (strings.rfind("?") != len(strings) - 1 and strings.rfind("?") != len(strings) - 2) and
        (strings.rfind("!") != len(strings) - 1 and strings.rfind("!") != len(strings) - 2) ) :
            return false
        else :
            return true



for root, dirs, files in os.walk('/Users/simrancc/Downloads/policy_crawl') :
    for file in files:
        print(file)
        if file == "policy.simple.html":

html = sys.argv[1]
p = PrivacyPolicy(html)
p.simplify_html()
p.output_plain_text("output3.html")
