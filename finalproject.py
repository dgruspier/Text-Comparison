#
#
# finalproject.py       CS 111 Final Project
#
# Daniel Gruspier, Ernest Wallace
#
#

from math import *

class TextModel:
    """ a class for recording the syntactic attributes of pieces of
        text and determining their similarity
    """

    def __init__(self, model_name):
        """ initialize attributes
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.para_lengths = {}

    def __repr__(self):
        """ returns a string represtnation of the TextModel
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) \
             + '\n' 
        s += '  number of stems: ' + str(len(self.stems)) + '\n'

        s += '  number of sentence lengths: ' \
             + str(len(self.sentence_lengths)) + '\n'
        s += '  number of paragraph lengths: ' \
             + str(len(self.para_lengths))

        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """
        paragraphs = s.split('\n\n')

        for p in paragraphs:
            para_words = clean_text(p)
            if para_words != '':
                if len(para_words) not in self.para_lengths:
                    self.para_lengths[len(para_words)] = 1
                else:
                    self.para_lengths[len(para_words)] += 1

        sentences = s.split('.')
        for e in sentences:
            e.split('?')
        for n in sentences:
            n.split('!')

        for sen in sentences:
            words = sen.split(' ')
            words = remove_empty_strings(words)
            if sen != '':
                if len(words) not in self.sentence_lengths:
                     self.sentence_lengths[len(words)] = 1
                else:
                     self.sentence_lengths[len(words)] += 1

        word_list = clean_text(s)

        for w in word_list:
            if w not in self.words:
                self.words[w] = 1      
            else:
                self.words[w] += 1

        for w in word_list:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1

        for w in word_list:
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1


    def add_file(self, filename):
        """adds all text in filename to TextModel"""

        f = open(filename, 'r', encoding='utf8', errors='ignore')
        words = f.read()

        self.add_string(words)


    def save_model(self):
        """ saves the TextModel object by writing its various
            feature dictionaries to files
            words becomes self.name_w.txt
            word_lengths becomes self.name_wl.txt
        """
        fw = open(self.name + '_w.txt', 'w')
        fwl = open(self.name + '_wl.txt', 'w')
        fstems = open(self.name + '_stems.txt', 'w')
        fsenlens = open(self.name + '_senlens.txt', 'w')
        fparalens = open(self.name + '_paralens.txt', 'w')
        
        fw.write(str(self.words))
        fwl.write(str(self.word_lengths))
        fstems.write(str(self.stems))
        fsenlens.write(str(self.sentence_lengths))
        fparalens.write(str(self.para_lengths))

        fw.close()
        fwl.close()
        fstems.close()
        fsenlens.close()
        fparalens.close()

    def read_model(self):
        """ reads dictionaries from words and word_lengths
            files and assigns them to the attributes of
            the TextModel object
            w.txt corresponds to self.words
            wl.txt corresponds to self.word_lengths
        """
        fw = open(self.name + '_w.txt', 'r')
        fwl = open(self.name + '_wl.txt', 'r')
        fstems = open(self.name + '_stems.txt', 'r')
        fsenlens = open(self.name + '_senlens.txt', 'r')
        fparalens = open(self.name + '_paralens.txt', 'r')

        words = fw.read()
        word_lengths = fwl.read()
        stems = fstems.read()
        sentence_lengths = fsenlens.read()
        para_lengths = fparalens.read()
        
        self.words = dict(eval(words))
        self.word_lengths = dict(eval(word_lengths))
        self.stems = dict(eval(stems))
        self.sentence_lengths = dict(eval(sentence_lengths))
        self.para_lengths = dict(eval(para_lengths))

        fw.close()
        fwl.close()
        fstems.close()
        fsenlens.close()
        fparalens.close()


    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores between
        the dictionaries self and other"""

        word_score = compare_dictionaries(other.words, self.words)
        word_len_score = compare_dictionaries(other.word_lengths, \
                                    self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        sen_len_score = compare_dictionaries(other.sentence_lengths, \
                                    self.sentence_lengths)
        para_len_score = compare_dictionaries(other.para_lengths, \
                                    self.para_lengths)

        scores = [word_score, word_len_score, stem_score, sen_len_score, \
                  para_len_score]
        return scores

    def classify(self, source1, source2):
        """ compares the called TextModel to two other specified
            sources and determines which of these others is more
            likely to be the source of self
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        print('scores for', source1.name + ':', scores1)
        print('scores for', source2.name + ':', scores2)

        weighted_sum1 = (10*scores1[0] + 5*scores1[1] + 7*scores1[2] \
                        + 3*scores1[3] + 2*scores1[4]) / 100
        weighted_sum2 = (10*scores2[0] + 5*scores2[1] + 7*scores2[2] \
                        + 3*scores2[3] + 2*scores2[4]) / 100

        if weighted_sum1 > weighted_sum2:
            print(self.name, 'is more likely to have come from',\
                  source1.name)
        else:
            print(self.name, 'is more likely to have come from',\
                  source2.name)

        

def clean_text(txt):
    """ returns a list containing the words in a string after
        the text has been 'cleaned'
    """
    for p in ['.', ',', '?', '!', '\'', ':', ';', '&', '(', ')', \
              '"', '*', '$', '#', '“', '”' ,'_', '’', "'"]:
        txt = txt.replace(p, '')
    for stupid_char in ['\n', '[', ']', '-']:
        txt = txt.replace(stupid_char, ' ')
    txt = txt.lower()
    word_list = txt.split(' ')
    return word_list

def stem(s):
    """ returns the 'stem' of a given word
    """
    if len(s) == 4 and s[-3:] == 'ing':
        return s
    if len(s) < 4:
        return s
    if s[-3:] == 'ing' and len(s) > 4:
        if s[-4] == s[-5] and s[-4] not in 'slfz':
            s = s[:-4]
        else:
            s = s[:-3]
    elif s[-2:] == 'er':
        if s[-3] == s[-4] and s[-3] not in 'slfz':
            s = s[:-3]
        else:
            s = s[:-2]
    elif s[-2:] == 'ed':
        if s[-3] == s[-4] and s[-3] not in 'slfz':
            s = s[:-3]
        else:
            s = s[:-2]
    elif s[-2:] == 'ly' and len(s) > 5:
        s = s[:-2]
    elif s[-3:] == 'ous':
        if s[-4] in 'ie':
            s = s[:-4]
        else:
            s = s[:-3]
    elif s[-1] == 's' and s[-2] != 's' and s[-2:] != 'is':
        s = s[:-1]
    elif s[-2:] == 'en':
        if s[-3] == s[-4] and s[-3] not in 'slfz':
            s = s[:-3]
        else:
            s = s[:-2]
    if s[-3:] == 'ing' or s[-2:] == 'er' or s[-2:] == 'ed' \
       or s[-3:] == 'ous' or s[-2:] == 'en':
        s = stem(s)
    return s
    

def compare_dictionaries(d1, d2):
    """ computes the log Naive-Bayes similarity score between two
        given dictionaries
    """
    score = 0
    total = 0
    for key in d1:
        total += d1[key]
    for key in d2:
        if key in d1:
            score += d2[key]*log(d1[key]/total)
        else:
            score += d2[key]*log(.5 / total)

    return score


def test():
    """ tests the TextModel class """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def run_tests():
    """ runs additional tests of the TextModel class """
    
    source1 = TextModel('NYT')
    source1.add_file('nyt_isis.txt')
    source1.add_file('nyt_school.txt')

    source2 = TextModel('Forbes')
    source2.add_file('forbes_crypto.txt')
    source2.add_file('forbes_ocean.txt')

    new1 = TextModel('Different NYT')
    new1.add_file('nyt_taxes.txt')
    new1.classify(source1, source2)
    print('\n')
    
    new2 = TextModel('Different Forbes')
    new2.add_file('forbes_pinterest.txt')
    new2.classify(source1, source2)
    print('\n')

    new3 = TextModel('Jackson\'s Paper')
    new3.add_file('jackson_paper.txt')
    new3.classify(source1, source2)
    print('\n')

    new4 = TextModel('WP')
    new4.add_file('wp_rosenstein.txt')
    new4.classify(source1, source2)
    print('\n')
    

def remove_empty_strings(words):
    """ removes all empty strings from a list of strings
    """
    if words == []:
        return []
    else:
        rest_remove = remove_empty_strings(words[1:])
        if words[0] == '':
            return rest_remove
        else:
            return [words[0]] + rest_remove
