import Lib.re as re
import logic
from dictionary import * 

#TODO: instruction set
#TODO: a way to handle verbose without making the code cluttered

def setSignal(dotSignalFunc = None, dashSignalFunc = None, shortPauseSignalFunc = None, longPauseSignalFunc = None):
    logic.dotSignal = dotSignalFunc
    logic.dashSignal = dashSignalFunc
    logic.shortPauseSignal = shortPauseSignalFunc
    logic.longPauseSignal = longPauseSignalFunc

def setGuide(inputMode = None, outputMode = 'auto', outputDumpFunction = None):
    if inputMode is 'classic': print('Warning: \'flash()\' starts parsing as soon as a letter delimiter for the selected input type is encountered, therefore all letters in classic mode must end with \'\\s\'')
    logic.inputMode = inputMode
    logic.outputMode = outputMode
    logic.outputDump = outputDumpFunction
    
def translate(string, outputMode = 'auto', guidedMode = False):
    intext, inputMode = logic.processInput(string.strip().lower(), guidedMode)
    outtext =''

    if outputMode is 'auto':
        outputMode = 'classic' if inputMode is 'typed' else 'typed'
    if outputMode not in modeParse:
        raise ValueError("Invalid mode. Try \'classic\', \'binary\', \'typed\' or \'signal\'.", logic.outputMode)
    if outputMode is 'signal':
        if logic.dotSignal==None or logic.dashSignal==None or logic.shortPauseSignal==None or logic.longPauseSignal==None:
            raise RuntimeError("Please assign output functions with 'morse.signalConfig(,,,)' before using the 'signal' argument.")
        sendSignals = True
        outputMode = 'classic'
    else:
        sendSignals = False

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
    if sendSignals: logic.sendSignal(outtext)
    if logic.outputDump: logic.outputDump(outtext)
    return outtext

def clearQueue():
    logic.queue = ''
    
def flash(string):
    if logic.outputDump == None or logic.inputMode ==None:
        raise RuntimeError('Please assign a function for output dumping and the input mode through \'morse.setGuide(,,,)\' before calling \'morse.flash()\'. The parsed output will be transmitted as a str argument to the given function.')
    logic.queue+= string
    if letterDelimiterParse[logic.inputMode] in logic.queue:
        translate(logic.queue, logic.outputMode, True)
        clearQueue()

#TODO: test how big can the input be
#TODO: translate spaces too idk if they work
if __name__ == '__main__':
    print(translate('.... . .-.. .-.. ---    .-- --- .-. .-.. -..'))