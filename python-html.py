from bs4 import BeautifulSoup
#import spacy

#nlp = spacy.load('en_core_web_sm')
with open("sephoraPP.html") as fp:
    soup = BeautifulSoup(fp, features="html.parser")
    #print(soup)

#def dataLoaded(err, data) :
  #$ = cheerio.load('' + data + '');
  #console.log($.html($('ul')[0]));

for x in soup.find_all("p"):
    temp = str(x.contents[0].string)
    strr = ":"
    if (temp.rfind(strr) == len(temp) - 1 or temp.rfind(strr) == len(temp) - 2) :
        for sibling in x.next_siblings:
            if sibling.name == "li" or sibling.name == "ul" or sibling.name == "ol" :
                count = 0
                #for child in sibling.descendants :
                    #print(child.parent)
                for child in sibling.stripped_strings:
                    print(repr(child))
                    print()
                    #ellipsis_doc = nlp(temp)
                    #ellipsis_sentences = list(ellipsis_doc.sents)
                    #for sentence in ellipsis_sentences:
                        #print(sentence)
                        #print()
                    new_tag = soup.new_tag("p")
                    x.append(new_tag)
                    new_tag.string = child
                    #print(soup)
                    #if type(child) != type(x.contents[0].string) :
                        #for y in child.descendants :
                            #if type(child) != type(x.contents[0].string)
                            #print(y)
                            #print("yayyayayya")
                            #combine = ""
                            #for string in y.strings :
                                #combine = combine + " " + string
                            #print(combine)
