from bs4 import BeautifulSoup
import spacy

nlp = spacy.load('en_core_web_sm')
with open("sephoraPP.html") as fp:
    soup = BeautifulSoup(fp, features="html.parser")
    #print(soup)

#def dataLoaded(err, data) :
  #$ = cheerio.load('' + data + '');
  #console.log($.html($('ul')[0]));
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
                #print(lastSentence)
                for child in sibling.stripped_strings:
                    hello = sibling.find_all(string=child)
                    if (child not in hello) :
                        if (child.rfind(".") != len(child) - 1 and child.rfind(".") != len(child) - 2) :
                            child += "."
                        new_tag = soup.new_tag("p")
                        x.parent.append(new_tag)
                        new_tag.string = str(lastSentence) + " " + child
                        print(new_tag.string)
                    else :
                        removed_strings.append(child)
                sibling.extract()
                x.extract()

with open("output1.html", "w") as file:
    file.write(str(soup))
