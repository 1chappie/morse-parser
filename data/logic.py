import Lib.re as re
from data.dictionary import *

tArgs = {
    "inputMode": None,
    "outputMode": None,
}
outputFunc = None

queue = ''

dotSignal = None
dashSignal = None
shortPauseSignal = None
longPauseSignal = None
signalsSet = False

def imDetect(passedString):
    if re.match(r'([.-]|\s)+$', passedString):
        return 'classic'
    if re.match(r'[01]+$', passedString):
        return 'binary'
    return 'typed'

def processInput(passedString, knownInput = 'auto'):
    if knownInput is 'auto':
        inputMode = imDetect(passedString)
    else:
        inputMode = knownInput

    if inputMode == 'classic':
        #replace new word indicators (tab) with ' !newWord& '
        passedString = str(re.sub(r'((\s){2,}|\t)', ' !newWord& ', passedString))
        return passedString.split(), inputMode

    elif inputMode == 'binary':
        #replace new word delimiter (0{4,}) with '!newWord&'
        #replace new letter delimiter (0{3}) with 's' for splitting
        passedString = str(re.sub(r'(0){4,}', '0s!newWord&s', passedString))
        passedString = str(re.sub(r'(0){3}','0s',passedString))
        passedString = passedString.split('s')
        return passedString, inputMode

    elif inputMode == 'typed':
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
        return newpassedString, inputMode

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
    intext, inputMode = processInput(string.strip().lower(), inputMode)
    outtext =''

    if outputMode is 'auto':
        outputMode = 'classic' if inputMode is 'typed' else 'typed'
    if outputMode is 'signal':
        if signalsSet is False:
            raise RuntimeError("Please assign output functions with 'morse.signalOutputs(,,,)' before trying to output as signal.")
        else:
            _doSignals = True
            outputMode = 'classic'
    else:
        _doSignals = False
    if outputMode not in modeParse:
        raise ValueError("Invalid mode. Try \'classic\', \'binary\', \'typed\' or \'signal\'.", outputMode)

    print('input mode: {}; output mode: {}'.format(inputMode,outputMode))
    for index, letter in enumerate(intext):
        if letter == '!newWord&':
            outtext += wordDelimiterParse[outputMode]
        else:
            if thereIsAFuckingPeriod(inputMode, letter): #HOW DO I MAKE THIS STOP CHECKING EVERYTIME WITOUT ADDING 323782893 LINES FOR SPECIAL CASES TO THIS FFS
                outtext += period[modeParse[outputMode]]
            else:
                snatcher = None
                snatcher = list(filter(lambda x: letter in x, valueDict))#why cant you unpack
                if snatcher:
                    print('-> snatched ',snatcher, 'for', letter)
                    outtext += snatcher[0][modeParse[outputMode]]  #fix nestednessesesees sometime
                else:
                    raise ValueError("Cannot parse \"" + letter + "\" through the " + inputMode + " input mode.")
            if index + 1 != len(intext):
                    outtext += letterDelimiterParse[outputMode]
    if _doSignals: sendSignal(outtext)
    return outtext