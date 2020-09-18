import sys
import pprint as pp
import os
from os import path


def mykwargs(argv):
    args = []
    kargs = {}
    for arg in argv:
        if '=' in arg:
            key,val = arg.split('=')
            kargs[key] = val
        else:
            args.append(arg)
    return args, kargs


class AdfgxLookup:
    def __init__(self, k=None):
        # Gets rid of duplicate characters in key1
        self.key = self.remove_duplicates(k)
        # Declares all letters in alphabet to check with later
        self.alphabet = [chr(x+97) for x in range(26)]
        # 
        self.adfgx = ['A', 'D', 'F', 'G', 'X']
        
        self.keylen = 0     # Initialize length of key

        if self.key:        # Changes key length if we have key
            self.keylen = len(self.key)
                            
        self.polybius = None    # 
        self.lookup = None      # 

    def remove_duplicates(self, key):
        """ Removes duplicate letters from a given key, since they
            will break the encryption.

            Example: 
                key = 'helloworldhowareyou'
                returns 'helowrdayu'

        """
        newkey = []             # create a list for letters
        for i in key:           # loop through key
            if not i in newkey:  # skip duplicates
                newkey.append(i)
        
        # create a string by joining the newkey list as a string
        return ''.join(str(x) for x in newkey)

    def build_polybius_string(self,key=None):
        """Builds a string consisting of a keyword + the remaining
           letters of the alphabet. 
           Example:
                key = 'superbatzy'
                polybius = 'superbatzycdfghiklmnoqvwx'
        """
        # no key passed in, used one from constructor
        if key:
            self.key = self.remove_duplicates(key)
        else:
            print("Error: There is NO key defined to assist with building of the matrix")
            sys.exit(0)

        # key exists ... continue
        self.keylen = len(self.key)

        # prime polybius_string variable with key
        self.polybius = self.key

        for l in self.alphabet:
            if l == 'j':        # no j needed!
                continue
            if not l in self.key:    # if letter not in key, add it
                self.polybius += l
        return self.polybius

    def build_polybius_lookup(self,key=None):
        if key != None:
            self.key = self.remove_duplicates(key)

        # NO key!
        if not self.key:
            print("Error: There is NO key defined to assist with building of the matrix")
            sys.exit(0)

        # no polybius built, make one!
        if self.polybius == None:
            self.build_polybius_string()

        # init our dictionary
        self.lookup = {}            # dict as our adfgx reverse lookup
        for l in self.polybius:     # loop through the 1D matrix we created
            self.lookup[l] = ''     # init keys in the dictionary

        row = 0 
        col = 0

        # loop through the polybius 1D string and get the 2 letter pairs
        # needed to do the initial encryption
        for row in range(5):
            for col in range(5):
                i = (5 * row) + col
                self.lookup[self.polybius[i]] = self.adfgx[row]+self.adfgx[col]

        return self.lookup


    def sanity_check(self):

        if not self.key:
            print("Error: There is NO key defined to assist with building of the matrix")
            sys.exit(0)

        # no polybius built, make one!
        if self.polybius == None:
            self.build_polybius_string()

        row = 0
        col = 0
       
        sys.stdout.write('\n  ')
        for l in self.adfgx:
            sys.stdout.write(l+' ')
        sys.stdout.write('\n')
        for l in self.adfgx:
            sys.stdout.write(l+' ')
            for ll in self.adfgx:
                i = (5 * row) + col
                sys.stdout.write(self.polybius[i]+' ')
                col += 1
            row += 1
            col = 0
            sys.stdout.write("\n")


if __name__ == '__main__':
    argv = sys.argv[1:]  # Command Parameter arguments stored
    args, kwargs = mykwargs(argv)     # Command parameters placed into a dictionary
    input_file = kwargs.get('input', None)   # Gets inputfile
    output_file = kwargs.get('output', None)  # Gets outputfile
    task = kwargs.get('task',None)          # Encrypt or Decrypt
    key1 = kwargs.get('key1',None)            # Gets First Key
    key2 = kwargs.get('key2',None)            # Gets First Key
    if input_file:  # Gets plain text from input file
        input_file = path.join(path.dirname(__file__), input_file)
        with open(input_file) as f:
            plaintext = f.read()
    else:
        plaintext = "therewasnoplaintextspecified"
        
    if task == "encrypt":
        A = AdfgxLookup(key1)
        
        # build my lookup table 
        lookup = A.build_polybius_lookup()
        print(A.polybius)
        pp.pprint(lookup)
        ALPHABET = [chr(x+97) for x in range(26)]
        ciphertext = ""
        for c in plaintext:
            if c in ALPHABET:
                ciphertext += lookup[c]
        print(ciphertext)
