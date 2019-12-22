from bs4 import BeautifulSoup
import os
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords 
import string

page_list = ['CNN.html', 'FOX_NEWS.html', 'MSNBC.html', 'NTD.html', 'VOA.html']
occurrence_lists = []

class TrieNode(object):
    def __init__(self):
        self.child = {}
        self.isEnd = False
        self.index_OL = None

class Trie(object):
    def __init__(self):
        self.root = TrieNode()
    
    # Add word into trie and update occurrence lists
    def addWord(self, word, page_index):
        curNode = self.root
        
        for i in range(0, len(word)):
            if curNode.child.get(word[i]) is None:
                curNode.child[word[i]] = TrieNode()
            curNode = curNode.child[word[i]]
        if curNode.isEnd == False:
            curNode.isEnd = True
            occur_list = [0] * len(page_list)
            occurrence_lists.append(occur_list)
            curNode.index_OL = len(occurrence_lists) - 1
        else:
            occurrence_lists[curNode.index_OL][page_index] += 1
    
    # Filter valid words from the input string, search them in the trie and return filtered words and their corresponding occurrence list
    def searchWord(self, word):
        word_NP = removePunctuation(word)
        word_list = wordList(word_NP)
        word_list_filtered = wordListFiltered(word_list)
        print("******************************************************")
        print("Valid search words: [" + ", ".join(word_list_filtered) + "]")
        index_OL_list = []
        
        for word in word_list_filtered:
            curNode = self.root
            word_not_found = False
            for i in range(0, len(word)):
                if curNode.child.get(word[i]) is None:
                    word_not_found = True
                    break
                curNode = curNode.child[word[i]]
            if curNode.isEnd == False:
                word_not_found = True
            if word_not_found == True:
                index_OL_list.append([0] * len(page_list))
            else:
                index_OL_list.append(occurrence_lists[curNode.index_OL])
        return word_list_filtered, index_OL_list
            
# Load page content 
def loadHtml(page):
    html_file = open(os.path.join('Input_Files', page), "r")
    html_content = html_file.read()
    html_file.close()
    return html_content

# Store useful text into a string
def getTextFromHtml(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    html_text = soup.get_text()
    return html_text

# Replace punctuation with white space from the string
def removePunctuation(html_text):
    html_text_NP = html_text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
    return html_text_NP

# Convert all characters to lowercase and put each word from the string into a list
def wordList(html_text_NP):
    word_list = html_text_NP.lower().split()
    return word_list

# Remove stop words from the list
def wordListFiltered(word_list):
    stop_words = set(stopwords.words('english'))
    word_list_filtered = [w for w in word_list if not w in stop_words]
    return word_list_filtered

# Print the ranked search result 
def printSearchResult(word_list_filtered, index_OL_list):
    for i in range(0, len(word_list_filtered)):
        print("******************************************************")
        # index_OL_list[i].sort(reverse = True)
        page_OL = {}
        for p in range(0, len(page_list)):
            # print("Word '" + word_list_filtered[i] + "' appears in " + page_list[p] + " " + str(index_OL_list[i][p]) + " time(s).")
            page_OL["Word '" + word_list_filtered[i] + "' appears in " + page_list[p] + " " + str(index_OL_list[i][p]) + " time(s)."] = index_OL_list[i][p]
        sorted_page_OL = sorted(page_OL.items(), key=lambda x: x[1], reverse=True)
        for item in sorted_page_OL:
            print(item[0])



if __name__ == "__main__":
    T = Trie()
    q = False
    print("=========================")
    for i in range(0, len(page_list)):
        print("Reading " + page_list[i])
        html_content = loadHtml(page_list[i])
        html_text = getTextFromHtml(html_content)
        html_text_NP = removePunctuation(html_text)
        word_list = wordList(html_text_NP)
        word_list_filtered = wordListFiltered(word_list)
        for word in word_list_filtered:
            T.addWord(word, i)
    print("=========================")
    print("Done reading pages.")
    
    while q == False:
        print("******************************************************")
        words_input = input("Search words (Enter 'q' to quit): ")
        if words_input == 'q':
            q = True
            break
        word_list_filtered, index_OL_list = T.searchWord(words_input)
        if len(word_list_filtered) == 0:
            print("No valid words entered.")
            continue
        printSearchResult(word_list_filtered, index_OL_list)

