from bs4 import BeautifulSoup
import spacy
import re


class PrivacyPolicy(object):

    #initialize class with var to store various metadata info
    def __init__(self, html, remove_Array, listAvg, pLength) :
        self.html = html
        with open(html) as fp:
            self.inputSoup = BeautifulSoup(fp, features="html.parser")
        self.removed_strings = remove_Array
        self.listAvg = listAvg
        self.paragraphAvgLength = pLength

    #only print plain text for whichever html passed in
    def print_plain_text(self, html) :
        #open html and create BS object to parse
        with open(html) as fp:
            soup = BeautifulSoup(fp, features="html.parser")
        #loop through all strings within entire html file then print
        for strings in soup.stripped_strings:
            print(strings)

    #store plain text into an output file for whichever html passed in
    def output_plain_text(self, html) :
        #open html and create BS object to parse
        with open(html) as fp:
            soup = BeautifulSoup(fp, features="html.parser")
        allStrings = []
        #loop through all strings within entire html file and store into array
        for strings in soup.stripped_strings:
            allStrings.append(strings)
        #write allStrings to output file
        with open("plaintext.txt", "w") as file:
            file.write(str(allStrings))


    def simplify_html(self) :
        #load english dic for spaCy to get sentences later
        nlp = spacy.load('en_core_web_sm')
        #loop through all paragraph elements
        for x in self.inputSoup.find_all("p"):
            text = str(x.contents[0].string) #get text of <p>
            colon = ":"
            #find <p> that end in a colon
            if (text.rfind(colon) == len(text) - 1 or text.rfind(strr) == len(text) - 2) :
                for sibling in x.next_siblings:
                    #find sibling that is li/ul/ol
                    if sibling.name == "li" or sibling.name == "ul" or sibling.name == "ol" :
                        ellipsis_doc = nlp(text)
                        ellipsis_sentences = list(ellipsis_doc.sents)
                        #get last sentence from <p> text
                        lastSentence = ellipsis_sentences[len(ellipsis_sentences) - 1]
                        allStrings = []
                        #loop through all the list elements within the <p>
                        for child in sibling.stripped_strings:
                            #print(sibling.find(string=re.compile(child)))
                            #print("############################################")
                            allStrings = sibling.find_all(string=re.compile(child))
                            #print(allStrings)
                        for string in allStrings :
                            #print(string)
                            #if parent of string is <li> include
                            if (string.parent.name == "li") :
                                #check if ending of list text is correct punctuation otherwise add '.'
                                if ( (string.rfind(".") != len(string) - 1 and string.rfind(".") != len(string) - 2) and
                                (string.rfind("?") != len(string) - 1 and string.rfind("?") != len(text) - 2) and
                                (string.rfind("!") != len(string) - 1 and string.rfind("!") != len(text) - 2) ):
                                    string += "."
                                #create new paragraph element and insert before orginial <p>
                                new_tag = self.inputSoup.new_tag("p")
                                x.insert_before(new_tag)
                                new_tag.string = str(lastSentence) + " " + string
                                #print(new_tag.string)
                            #if parent is not <li> it is not a list element (subtitle, comment, etc.)
                            else :
                                self.removed_strings.append(string)
                        #delete entire bulleted list and original <p>
                        sibling.extract()
                        x.extract()

    #output html
    def outputFile(self) :
        with open("output1.html", "w") as file:
            file.write(str(self.inputSoup))

    #calc average list of length
    #going to change into heuristic later
    def average_list_length(self) :
        average = 0
        ellipsis_sentences = 0
        #load english dic for spaCy to get sentences later
        nlp = spacy.load('en_core_web_sm')
        #loop through all paragraph elements
        for x in self.inputSoup.find_all("p"):
            text = str(x.contents[0].string)
            colon = ":"
            #find <p> that end in a colon
            if (text.rfind(colon) == len(text) - 1 or text.rfind(strr) == len(text) - 2) :
                for sibling in x.next_siblings:
                    #find sibling that is li/ul/ol
                    if sibling.name == "li" or sibling.name == "ul" or sibling.name == "ol" :
                        ellipsis_doc = nlp(text)
                        ellipsis_sentences = list(ellipsis_doc.sents)
                        sum = 0
                        #sum up length of all bulleted text
                        for sentence in ellipsis_sentences:
                            sum += len(sentence)
        self.listAvg = sum / len(ellipsis_sentences)
        return self.listAvg

    #calc average # of sentences per paragraph
    def average_sentences_in_paragraph(self) :
        average = 0
        count = 0
        #get all <p> elements and loop through
        for x in self.inputSoup.find_all("p"):
            count = count + 1
            text = str(x.contents[0].string)
            ellipsis_doc = nlp(text)
            #get all sentences from paragraph
            ellipsis_sentences = list(ellipsis_doc.sents)
            #sum up length of all sentences in one paragraph
            sum += len(ellipsis_sentences)
        self.paragraphAvgLength = sum / count
        return self.paragraphAvgLength