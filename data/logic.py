import Lib.re as re
from data.dictionary import *

#inputMode = None
#outputMode = None

queue = ''

dotSignal = None
dashSignal = None
shortPauseSignal = None
longPauseSignal = None
signalsSet = False

outputFunc = None

def imDetect(passedString):
    if re.match(r'([.-]|\s)+$', passedString):
        return 'classic'
    if re.match(r'[01]+$', passedString):
        return 'binary'
    return 'typed'

def processInput(passedString):
    #global inputMode
    #if not guidedMode:
    _inputMode = imDetect(passedString)
    #else:
    #    if inputMode is None: raise RuntimeError("While using guidedMode, you must use \'Set()\' to specify the inputMode.")
    #    _inputMode = inputMode

    if _inputMode == 'classic':
        #replace new word indicators (tab) with ' !newWord& '
        passedString = str(re.sub(r'((\s){2,}|\t)', ' !newWord& ', passedString))
        return passedString.split(), _inputMode

    elif _inputMode == 'binary':
        #replace new word delimiter (0{4,}) with '!newWord&'
        #replace new letter delimiter (0{3}) with 's' for splitting
        passedString = str(re.sub(r'(0){4,}', '0s!newWord&s', passedString))
        passedString = str(re.sub(r'(0){3}','0s',passedString))
        passedString = passedString.split('s')
        return passedString, _inputMode

    elif _inputMode == 'typed':
        #replace new word delimiter (\s|\t)+ with '!newWord&'
        #split passedString into words
        #compile each letter into list
        passedString = str(re.sub(r'(\s|\t)+', ' !newWord& ', passedString))
        passedString = passedString.split()
        newpassedString = []
        for word in passedString:
            if word != '!newWord&':
                for letter in word:
                    newpassedString.extend(letter)
            else:
                newpassedString.append('!newWord&')
        return newpassedString, _inputMode

def sendSignal(classicString):
    for char in classicString:
        if char is '.':
            dotSignal()
        elif char is '-':
            dashSignal()
        elif char is ' ':
            shortPauseSignal()
        elif char is '\t':
            longPauseSignal()
        else:
            raise RuntimeError('Couldn\'t parse \'{}\' as signal.'.format(char))

def parse(string, inputMode = 'auto', outputMode = 'auto'):
    intext, inputMode = processInput(string.strip().lower())
    outtext =''

    if outputMode is 'auto':
        outputMode = 'classic' if inputMode is 'typed' else 'typed'
    if outputMode is 'signal':
        if signalsSet is False:
            raise RuntimeError("Please assign output functions with 'morse.setSignal(,,,)' before trying to output as signal.")
        else:
            _doSignals = True
            outputMode = 'classic'
    else:
        _doSignals = False
    if outputMode not in modeParse:
        raise ValueError("Invalid mode. Try \'classic\', \'binary\', \'typed\' or \'signal\'.", outputMode)

    for index, letter in enumerate(intext):
        if letter == '!newWord&':
            outtext += wordDelimiterParse[outputMode]
        else:
            snatcher = None
            snatcher = list(filter(lambda x: letter in x, valueDict))#why cant you unpack
            if snatcher:
                print('-> snatched ',snatcher, 'for', letter)
                outtext += snatcher[0][modeParse[outputMode]]  #fix nestednessesesees sometime
                if index + 1 != len(intext):
                    outtext += letterDelimiterParse[outputMode]
            else:
                raise ValueError("Cannot parse \"" + letter + "\" through the "+ inputMode +" input mode." )
    if _doSignals: sendSignal(outtext)
    return outtext