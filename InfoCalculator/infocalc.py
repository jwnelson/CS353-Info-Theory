#!/usr/bin/python3
import sys, os, math

"""
    Script that calculates the information content of a text file of words,
    as well as the entropy of an alphabet and each letter's probability of occurence
"""

def main(argv):
    """

    """
    alphabet = None
    if len(argv) < 2:
        print("Usage:\n\t./infocalc.py -w wordfile [alphabet file]")

    else:
        alphaname = None
        if len(argv) > 2:
            alphabet = readAlphabet(argv[2])
            alphaname = argv[2]
        else:
            defaultAlpha = "EnglishAlphabet.txt"
            alphaname = defaultAlpha
            alphabet = readAlphabet(defaultAlpha)

        wordlist = readWords(argv[1])

        """
        for word in wordlist:
            entropy = calcEntropy(word, alphabet)
            print("Entropy of %s: %f" %(word, entropy))
            """

        alphaEntropy = alphabetEntropy(alphabet)
        print("Entropy of %s: %f" %(alphaname, alphaEntropy))

def readAlphabet(alphaFileString):
    print("Reading alphabet from %s" %alphaFileString)
    with open(alphaFileString, "r") as alphaFile:
        alphabet = dict(line.rstrip('\n').split(',') for line in alphaFile)

    for key in alphabet:
        alphabet[key] = float(alphabet[key])

    return alphabet

def readWords(wordFileString):
    print("Reading words from %s" %wordFileString)

    with open(wordFileString, "r") as wordFile:
        wordlist = [line.rstrip('\n') for line in wordFile]

    return wordlist

def calcEntropy(messageString, alphabet):
    """
        Calculate the entropy (information content) of the given message
        using the probabilities of each character in the given alphabet.
    """
    entropy = 0.0

    for ch in messageString:
        p = alphabet[ch]
        print(ch, p)

        #print(p * math.log(p,2))
        entropy += -p*math.log2(p)
        #print("Entropy: %f" %entropy)

    return entropy

def CalcInfo(messageString, alphabet):

    information = 0.0

    for ch in messageString:
        p = alphabet[ch]

        information += - math.log2(1/p)

    return information

def alphabetEntropy(alphabet):

    entropy = 0.0
    for letter in alphabet:
        p = alphabet[letter]
        print(p)
        if p == 0.0:
            continue
        else:
            entropy += -p*math.log2(p)

    return entropy

if __name__ == "__main__":
    main(sys.argv[0:])