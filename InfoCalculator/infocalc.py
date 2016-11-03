#!/usr/bin/python
import sys, os, math

"""
    Script that calculates the information content of a text file of words,
    as well as the entropy of an alphabet and each letter's probability of occurence
"""

def main(argv):
    """

    """
    alphabet = None
    if len(argv) < 2 or argv[1] == "help" or argv[1] == "-h":
        print("Usage:\n\t./infocalc.py <flag> <argument>")
        print("Valid flags:\n")
        print("\t-a\tSpecify an alphabet file to use. Defaults to English.")
        print("\t-i\tCalculate information content of a single string passed as the argument")
        print("\t-I\tCalculate information content of a list of strings in a file passed as the argument")
        print("\t-e\tCalculate the entropy of the alphabet specified with the -a flag. Defaults to English.")
        print("\t-L\tCalculate average code word length of a code.")
        print("\t-v\tVerbose printouts.")
    else:
        alphaname = None
        verbose = False

        # check for flags
        if "-v" in argv:
            verbose = True

        if "-a" in argv:
            # get the alphabet file from the argv index right after the -a flag
            alphaname = argv[argv.index("-a") + 1]
            alphabet = readAlphabet(alphaname, verbose = verbose)
        else:
            defaultAlpha = "EnglishAlphabet.txt"
            alphaname = defaultAlpha
            alphabet = readAlphabet(defaultAlpha, verbose = verbose)

        if "-i" in argv:
            word = argv[argv.index("-i") + 1]
            info = calcInfo(word, alphabet, verbose = verbose)
            print("Information of %s using %s: %f" %(word, alphaname, info))

        if "-I" in argv:
            wordfile = argv[argv.index("-I") + 1]
            wordlist = readWords(wordfile)
            print("Information of %s using %s:" %(wordfile, alphaname))
            for word in wordlist:
                info = calcInfo(word, alphabet, verbose = verbose)
                print("%s: %f" %(word, info))

        if "-e" in argv:
            alphaEntropy = alphabetEntropy(alphabet, verbose = verbose)
            print("Entropy of %s: %f" %(alphaname, alphaEntropy))

        if "-L" in argv:
            codeFile = argv[argv.index("-L") + 1]
            code = readCode(codeFile, verbose)
            acwl = calculate_acwl(code, verbose)

            print("ACWL of %s: %f" %(codeFile.rstrip("."), acwl))
        

def readAlphabet(alphaFileString, verbose = False):
    if verbose:
        print("Reading alphabet from %s" %alphaFileString)
    with open(alphaFileString, "r") as alphaFile:
        alphabet = dict(line.rstrip('\n').split(',') for line in alphaFile)

    for key in alphabet:
        alphabet[key] = float(alphabet[key])

    return alphabet

def readCode(codeFileString, verbose = False):
    if verbose:
        print("Reading code from %s" %codeFileString)
    with open(codeFileString, "r") as codeFile:
        code = dict(line.rstrip('\n').split(',') for line in codeFile)

    return code

def readWords(wordFileString, verbose = False):
    if verbose:
        print("Reading words from %s" %wordFileString)

    with open(wordFileString, "r") as wordFile:
        wordlist = [line.rstrip('\n') for line in wordFile]

    return wordlist

def calcEntropy(messageString, alphabet, verbose = False):
    """
        Calculate the entropy (information content) of the given message
        using the probabilities of each character in the given alphabet.
    """
    if verbose:
        print("Calculating entropy of %s" %alphabet)

    entropy = 0.0

    for ch in messageString:
        p = alphabet[ch]
        entropy += -p*math.log2(p)

        if verbose:
            print(ch, p)
            print("Entropy: %f" %entropy)

    return entropy

def calcInfo(messageString, alphabet, verbose = False):

    information = 0.0

    for ch in messageString:
        try:
            p = alphabet[ch]
            information += - math.log2(p)
        except KeyError as ke:
            print("Letter %c not in alphabet" %ch)
            information = 0
            break

        

    return information

def alphabetEntropy(alphabet, verbose = False):

    entropy = 0.0
    for letter in alphabet:
        p = alphabet[letter]
        if p == 0.0:
            continue
        else:
            entropy += -p*math.log2(p)

    return entropy

def calculate_acwl(code, verbose = False):
    """
        Calculate the average code word length of a code passed
        in as a csv with the symbols in column 0 and codewords in col 1.
    """
    cwlsum = 0
    for symbol in code:
        cwlsum += len(code[symbol])
    code_size = len(code)

    if verbose:
        print("CWL Sum: %d" %cwlsum)
        print("Code Size: %d" %code_size)

    return (float(cwlsum)/float(code_size))

if __name__ == "__main__":
    main(sys.argv[0:])