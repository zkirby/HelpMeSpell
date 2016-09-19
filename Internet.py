'''
This module contains all the information for getting information
form the internet.
This should be pretty abstract for the majority of the modules, only the Textwork
module understands how this works.
Hopefully, only a few calls will be submitted to this module
the majority of the calls will be re-routed to the sqlDatabase.

@author: Zachary
'''
from lxml import html
import requests

#Command to just Get the connector words
#deep_words = tree.xpath('//div[@class="definition"]/a/text()')

# Below is the Logic for requesting a word from the internet.
# This should all be filtered and only seen by the Textwork module.
# The only way that a word can be requested is if it has already been checked
# agaisnt the database and seen that it isn't in there.
def make_request(word, synm=False):
    '''make a request for a word
    additionally may contain a synonym'''
    try:
        request = 'http://ninjawords.com/'+word
        page = requests.get(request)
        tree = html.fromstring(page.content)

        text_body = tree.xpath('//div[@class="definition"]/text() | //div[@*]/a/text()')
        if synm:
            synonyms = tree.xpath('//dd[@class="synonyms"]/a/text()')
            return (text_body, synonyms)
        return (text_body,)
    except Exception as e:
        print("Failed to make a request to the dictionary server: "+str(e))

def grab_definition(definition, retVal=0):
    '''The function used by Text_work to
    ask the internet module for a definition'''
    try:
        if retVal == 0:
            text = make_request(definition)[0]
            return filterbody(combine_text(text))
        elif retVal == 1:
            text = make_request(definition)
            return filterbody(combine_text(text[0])), text[1]
        else:
            raise IndexError("Incorrect parameter value passed")
    except Exception as e:
        print("Failed to grab definition: "+str(e))


# Below is the Logic for filtering the text.
def filterbody(body):
    '''Removes useless stuff from the text body'''
    new_text = [(item.strip() + " ") for item in body if item.strip() != '']
    return ''.join(new_text)

def combine_text(lis):
    '''Combines the grammatical characters with
    the rest of the definition'''
    if len(lis) <= 1:
        return lis
    else:
        if condition(lis[1]):
            lis[0] = (lis[0] + lis[1])
            return [lis[0]] + combine_text(lis[2:])
        return [lis[0]] + combine_text(lis[1:])

def condition(item):
    '''checks if a specific text object
    meets a condition to be concatenated'''
    grammatical_chr = ".);,("
    for char in grammatical_chr:
        if item.startswith(char) or item == char:
            return True
    return False

def main():
    pass

if __name__ == '__main__':main()
