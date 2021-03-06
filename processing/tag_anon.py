'''
Created on March 2 2021

Still working on content_removed; others are done
'''

from bs4 import BeautifulSoup
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

__target_file__ = '../webscraping-o/htmlfiles/2ch.txt' #relative to the tag_anon.py 
org_file_name = os.path.basename(__target_file__)


with open(os.path.join(__location__,__target_file__), 'r', encoding="ISO-8859-1") as f:
    try:
        target_html = f.read() 
    except Exception as e:
        print('During file reading, this error occurred:', e)

soup = BeautifulSoup(target_html, 'html.parser')

cur_classes = {
    #'orgName': 'newName' 
    }
class_counter = 1
id_counter = 1

def tag_removed(soup):
    '''
    manipulate html tag names
    '''

    for tag in soup.findAll(True):
        # tag.attrs = tag.attrs.fromkeys(tag.attrs,"")
        tag.attrs = _tag_removed_helper(tag.attrs)
    return soup



def _tag_removed_helper(attrs):
    '''
    Class need to check if already assigned a number, then replace with that
    Id can only be used once in html, so just a simple counter to give names
    '''
    global cur_classes
    global class_counter
    global id_counter

    for attr_type, attr_values in attrs.items():
        if attr_type == 'class':
            for i, class_name in enumerate(attr_values):
                if class_name in cur_classes:
                    attr_values[i] = cur_classes[class_name]
                else:
                    new_class_name = 'Class_' + str(class_counter)
                    attr_values[i] = new_class_name
                    cur_classes[class_name] = new_class_name
                    class_counter += 1
        elif attr_type == "id":
            new_id_name = 'Id_' + str(id_counter)
            attrs[attr_type] = new_id_name
            id_counter += 1
        else:
            attrs[attr_type] = ""

    return attrs

def script_removed(soup):
    '''
    empties script tags; ie. remove embedded javascript while still keeping the <script> 
    '''
    for tag in soup.findAll('script'):
        tag.clear()
    return soup

def content_removed(soup):
    '''
    anonymize text content
    '''
    for tag in soup.findAll('True'):
        tag.string = "None"
    return soup


soup = tag_removed(soup)
soup = script_removed(soup)

with open(os.path.join(__location__, f"./modified_{org_file_name}"), 'wb') as f_out:
    try: 
        f_out.write(soup.prettify("utf-8"))
    except Exception as e:
        print('During file writing, this error occurred:', e)


