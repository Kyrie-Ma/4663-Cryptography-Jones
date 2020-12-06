'''
Landen Jones
Program 5 - Vigenere Cracking
CMPS 4662 - Cryptography
'''
import sys
import os
from frequency import Frequency
from math import log

# Build a cost dictionary, assuming Zipf's law
# cost = -math.log(probability)
freqWords = open("Assignments/A05/words-by-frequency.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(freqWords)))) for i,k in enumerate(freqWords))
maxword = max(len(x) for x in freqWords)


def mykwargs(argv):
    '''
    Processes argv list into plain args (list) and kwargs (dict).
    Just easier than using a library like argparse for small things.
    '''
    args = []
    kargs = {}

    for arg in argv:
        if '=' in arg:
            key,val = arg.split('=')
            kargs[key] = val
        else:
            args.append(arg)
    return args,kargs


def usage(message=None):
    '''
    Display descriptive error messages if the keywords from .replit are incorrect
    '''
    
    if message:
        print(message)
    name = os.path.basename(__file__)
    print(f"Usage: python {name} [input=string filename] [output=string filename]")
    print(f"Example:\n\t python {name} input=in1 output=out1 \n")
    sys.exit()

  
# https://gist.github.com/enigmaticape/4254054 
# https://www.dcode.fr/index-coincidence
# Used both of these for reference and help in constructing this function
def incidence_of_coincidence(sequence):
    '''
    Processes and return the incidence of coincidence of a given substring of the ciphertext
    '''
    if (len(sequence) > 1):
      F = Frequency()
      F.count(sequence)
      IncOfCoinc = 0
      FreqNum = 0
      length = len(sequence)
      for i in range(0,26):
        FreqNum = F.getNthNum(i)
        IncOfCoinc = IncOfCoinc + (FreqNum*(FreqNum - 1))
      IncOfCoinc = (IncOfCoinc / (length*(length - 1)))
      return IncOfCoinc
    else:
      return 0

# https://inventwithpython.com/hacking/chapter21.html
# https://github.com/drewp41/Vigenere-Cipher-Breaker
# https://gist.github.com/akonradi/a9637c17fc6452d868ee
def get_key_length(ciphertext):
    ic_table=[]
    for guess_len in range(16):
      ic_sum=0.0
      avg_ic=0.0
      for i in range(guess_len):
        sequence=""
        # breaks the ciphertext into sequences
        for j in range(0, len(ciphertext[i:]), guess_len):
          sequence += ciphertext[i+j]
        
        # calls incidence_of_coincidence function for each sequence
        ic_sum+=incidence_of_coincidence(sequence)
      # don't want to divide by zero
      if (guess_len != 0):
        avg_ic=ic_sum/guess_len
      ic_table.append(avg_ic)

    # returns the index of most probable key length (highest IC)
    best_guess = ic_table.index(sorted(ic_table, reverse = True)[0])
    second_best_guess = ic_table.index(sorted(ic_table, reverse = True)[1])
    
    if best_guess % second_best_guess == 0:
      return second_best_guess
    else:
      return best_guess   


def get_key(keylength, check_Attempt,words):
    '''
    Search the dictionary for all words of length keylength.
    Put into an array with check_Attempt as the index of the key you return.
    Return one by one potential keys
    '''
    #key = "fortification" for input1

    for i in range(len(words)):
        words[i] = words[i].strip()
    rightLength = []
    count = 0

    for word in words:
        if len(word) == keyLength:
            count += 1
            rightLength.append(word)

    key = rightLength[check_Attempt]
    return key


def check_english(message, words):
    '''
    Check to see if the plaintext received from the potential key is a valid, english statement which could be the encrypted message. Return the probability ratio of likliness for English.
    '''
    tokens = message.split()
    score = 0
    for tok in tokens:
        if tok.upper() in words:
            score += 1

    return score / len(tokens)


def decrypt(ciphertext, key, plaintext):
    # Decrypt using the key and return the plaintext
    plaintext = ""
    ciphertext = ciphertext.lower()
    key = key.lower()

    i = 0
    for letter in ciphertext:
        #check table 
        a = ord(letter)-97
        b = ord(key[i])-97
        plaintext += chr(((a-b)%26) + 97)

        i = (i + 1) % len(key)
    return plaintext


def infer_spaces(s):
    """
    Uses dynamic programming to infer the location 
    of spaces in a string without spaces.
    https://controlc.com/c1666a6b
    """
    # Find the best match for the i first characters, assuming cost hasbeen built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))


if __name__=='__main__':
    # get processed command line arguments 
    _,params = mykwargs(sys.argv[1:])

    infile = params.get('input',None)
    outfile = params.get('output',None)

    if not infile and not outfile:
      usage()
    
    with open("Assignments/A05/words","r") as f:
      words = f.readlines()
    
    for i in range(len(words)):
        words[i] = words[i].strip()

    with open(infile) as f:
        ciphertext = f.read()
    #strip ciphertext of its spaces
    plaintext = ""

    keyLength = get_key_length(ciphertext)
    print("Key length is", keyLength)

    check_Again = 1
    check_Attempt = 0
    
    while (check_Again == 1):
      check_Attempt = check_Attempt + 1
      # get a different key, decrypt, and check if it's english
      key = get_key(keyLength, check_Attempt, words)
      plaintext = decrypt(ciphertext, key, plaintext)
      plaintext = infer_spaces(plaintext)
      ratio = check_english(plaintext,words)

      # if you find the correct message, break out of the check_Again
      if (ratio >= 0.8):
        check_Again = 0
      
    print("The plaintext is " + plaintext)