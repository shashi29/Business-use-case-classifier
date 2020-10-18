import os
import sys
import os, sys, re, unicodedata

# custom imports
from gensim.utils import deaccent
from collections import Counter
verbose = True


WPLACEHOLDER = 'word_placeholder'

def _check_replace(w):
    return not bool(re.search(WPLACEHOLDER, w))

def _make_cleaning(s, c_dict):
    if _check_replace(s):
        s = s.translate(c_dict)
    return s

def _check_vocab(c_list, vocabulary, response='default'):
    try:
        words = set([w for line in c_list for w in line.split()])
        print('Total Words :',len(words))
        u_list = words.difference(set(vocabulary))
        k_list = words.difference(u_list)
    
        if response=='default':
            print('Unknown words:', len(u_list), '| Known words:', len(k_list))
        elif response=='unknown_list':
            return list(u_list)
        elif response=='known_list':
            return list(k_list)
    except:
        return []
    
def _make_dict_cleaning(s, w_dict):
    if _check_replace(s):
        s = w_dict.get(s, s)
    return s

def _print_dict(temp_dict, n_items=10):
    run = 0
    for k,v in temp_dict.items():
        print(k,'---',v)
        run +=1
        if run==n_items:
            break  
        
def to_lower(data):
    if verbose: print('#'*10 ,'Step - Lowering everything:')
    data = list(map(lambda x: x.lower(), data))
    return data

def clean_contractions(data):
    

    helper_contractions = {
     "aren't": 'are not',
     "Aren't": 'Are not',
     "AREN'T": 'ARE NOT',
     "C'est": "C'est",
     "C'mon": "C'mon",
     "c'mon": "c'mon",
     "can't": 'cannot',
     "Can't": 'Cannot',
     "CAN'T": 'CANNOT',
     "con't": 'continued',
     "cont'd": 'continued',
     "could've": 'could have',
     "couldn't": 'could not',
     "Couldn't": 'Could not',
     "didn't": 'did not',
     "Didn't": 'Did not',
     "DIDN'T": 'DID NOT',
     "don't": 'do not',
     "Don't": 'Do not',
     "DON'T": 'DO NOT',
     "doesn't": 'does not',
     "Doesn't": 'Does not',
     "else's": 'else',
     "gov's": 'government',
     "Gov's": 'government',
     "gov't": 'government',
     "Gov't": 'government',
     "govt's": 'government',
     "gov'ts": 'governments',
     "hadn't": 'had not',
     "hasn't": 'has not',
     "Hasn't": 'Has not',
     "haven't": 'have not',
     "Haven't": 'Have not',
     "he's": 'he is',
     "He's": 'He is',
     "he'll": 'he will',
     "He'll": 'He will',
     "he'd": 'he would',
     "He'd": 'He would',
     "Here's": 'Here is',
     "here's": 'here is',
     "I'm": 'I am',
     "i'm": 'i am',
     "I'M": 'I am',
     "I've": 'I have',
     "i've": 'i have',
     "I'll": 'I will',
     "i'll": 'i will',
     "I'd": 'I would',
     "i'd": 'i would',
     "ain't": 'is not',
     "isn't": 'is not',
     "Isn't": 'Is not',
     "ISN'T": 'IS NOT',
     "it's": 'it is',
     "It's": 'It is',
     "IT'S": 'IT IS',
     "I's": 'It is',
     "i's": 'it is',
     "it'll": 'it will',
     "It'll": 'It will',
     "it'd": 'it would',
     "It'd": 'It would',
     "Let's": "Let's",
     "let's": 'let us',
     "ma'am": 'madam',
     "Ma'am": "Madam",
     "she's": 'she is',
     "She's": 'She is',
     "she'll": 'she will',
     "She'll": 'She will',
     "she'd": 'she would',
     "She'd": 'She would',
     "shouldn't": 'should not',
     "that's": 'that is',
     "That's": 'That is',
     "THAT'S": 'THAT IS',
     "THAT's": 'THAT IS',
     "that'll": 'that will',
     "That'll": 'That will',
     "there's": 'there is',
     "There's": 'There is',
     "there'll": 'there will',
     "There'll": 'There will',
     "there'd": 'there would',
     "they're": 'they are',
     "They're": 'They are',
     "they've": 'they have',
     "They've": 'They Have',
     "they'll": 'they will',
     "They'll": 'They will',
     "they'd": 'they would',
     "They'd": 'They would',
     "wasn't": 'was not',
     "we're": 'we are',
     "We're": 'We are',
     "we've": 'we have',
     "We've": 'We have',
     "we'll": 'we will',
     "We'll": 'We will',
     "we'd": 'we would',
     "We'd": 'We would',
     "What'll": 'What will',
     "weren't": 'were not',
     "Weren't": 'Were not',
     "what's": 'what is',
     "What's": 'What is',
     "When's": 'When is',
     "Where's": 'Where is',
     "where's": 'where is',
     "Where'd": 'Where would',
     "who're": 'who are',
     "who've": 'who have',
     "who's": 'who is',
     "Who's": 'Who is',
     "who'll": 'who will',
     "who'd": 'Who would',
     "Who'd": 'Who would',
     "won't": 'will not',
     "Won't": 'will not',
     "WON'T": 'WILL NOT',
     "would've": 'would have',
     "wouldn't": 'would not',
     "Wouldn't": 'Would not',
     "would't": 'would not',
     "Would't": 'Would not',
     "y'all": 'you all',
     "Y'all": 'You all',
     "you're": 'you are',
     "You're": 'You are',
     "YOU'RE": 'YOU ARE',
     "you've": 'you have',
     "You've": 'You have',
     "y'know": 'you know',
     "Y'know": 'You know',
     "ya'll": 'you will',
     "you'll": 'you will',
     "You'll": 'You will',
     "you'd": 'you would',
     "You'd": 'You would',
     "Y'got": 'You got',
     'cause': 'because',
     "had'nt": 'had not',
     "Had'nt": 'Had not',
     "how'd": 'how did',
     "how'd'y": 'how do you',
     "how'll": 'how will',
     "how's": 'how is',
     "I'd've": 'I would have',
     "I'll've": 'I will have',
     "i'd've": 'i would have',
     "i'll've": 'i will have',
     "it'd've": 'it would have',
     "it'll've": 'it will have',
     "mayn't": 'may not',
     "might've": 'might have',
     "mightn't": 'might not',
     "mightn't've": 'might not have',
     "must've": 'must have',
     "mustn't": 'must not',
     "mustn't've": 'must not have',
     "needn't": 'need not',
     "needn't've": 'need not have',
     "o'clock": 'of the clock',
     "oughtn't": 'ought not',
     "oughtn't've": 'ought not have',
     "shan't": 'shall not',
     "sha'n't": 'shall not',
     "shan't've": 'shall not have',
     "she'd've": 'she would have',
     "she'll've": 'she will have',
     "should've": 'should have',
     "shouldn't've": 'should not have',
     "so've": 'so have',
     "so's": 'so as',
     "this's": 'this is',
     "that'd": 'that would',
     "that'd've": 'that would have',
     "there'd've": 'there would have',
     "they'd've": 'they would have',
     "they'll've": 'they will have',
     "to've": 'to have',
     "we'd've": 'we would have',
     "we'll've": 'we will have',
     "what'll": 'what will',
     "what'll've": 'what will have',
     "what're": 'what are',
     "what've": 'what have',
     "when's": 'when is',
     "when've": 'when have',
     "where'd": 'where did',
     "where've": 'where have',
     "who'll've": 'who will have',
     "why's": 'why is',
     "why've": 'why have',
     "will've": 'will have',
     "won't've": 'will not have',
     "wouldn't've": 'would not have',
     "y'all'd": 'you all would',
     "y'all'd've": 'you all would have',
     "y'all're": 'you all are',
     "y'all've": 'you all have',
     "you'd've": 'you would have',
     "you'll've": 'you will have'}
    
    if verbose: print('#' * 10, 'Step - Contractions:')
    # Apply spellchecker for contractions
    # Local (only unknown words)
    local_vocab = {}
    temp_vocab = _check_vocab(data, local_vocab, response='unknown_list')
    temp_vocab = [k for k in temp_vocab if (_check_replace(k)) and ("'" in k)]
    temp_dict = {}
    for word in temp_vocab:
        if word in helper_contractions:
            temp_dict[word] = helper_contractions[word]
    data = list(map(lambda x: ' '.join([_make_dict_cleaning(i,temp_dict) for i in x.split()]), data))
    if verbose: _print_dict(temp_dict) 
    return data
