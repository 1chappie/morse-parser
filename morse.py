import Lib.re as re
import data.logic as logic
from data.dictionary import * 

#hello
#TODO: instruction sets
#TODO: a way to handle verbose without making the code cluttered

def signalOutputs(dotSignalFunc = None, dashSignalFunc = None, shortPauseSignalFunc = None, longPauseSignalFunc = None):
    logic.dotSignal = dotSignalFunc
    logic.dashSignal = dashSignalFunc
    logic.shortPauseSignal = shortPauseSignalFunc
    logic.longPauseSignal = longPauseSignalFunc
    if None in (dotSignalFunc, dashSignalFunc, shortPauseSignalFunc, longPauseSignalFunc):
        raise ValueError('All signals must be assigned a function.')
    else:
        logic.signalsSet = True

def translatorArgs(inputMode = None, outputMode = 'auto', outputFunc = None):
    if inputMode is 'classic': print('Warning: \'flash()\' starts parsing as soon as a letter delimiter for the selected input type is encountered, therefore all letters in classic mode must end with \'\\s\'')
    if None in (inputMode, outputFunc):
        raise RuntimeError('Please assign a function for output dumping and the input mode through \'morse.setParser(,,)\' before calling \'morse.signal()\'. The parsed output will be transmitted as a str argument to the given function.')
    logic.inputMode = inputMode #TODO: insignificant atm
    logic.outputMode = outputMode
    logic.outputFunc = outputFunc
#TODO: remake user interface so it easier

def translate(string, outputMode='auto'):
    return logic.parse(string, 'auto', outputMode)
    
def clearMemory():
    logic.queue = ''
    
def signal(string):
    logic.queue+= string
    if letterDelimiterParse[logic.inputMode] in logic.queue: #TODO: translate just till the space
        logic.outputFunc(logic.parse(logic.queue,logic.inputMode, logic.outputMode))
        clearMemory()

#TODO: test how big can the input be
#TODO: translate spaces too idk if they work
if __name__ == '__main__':
    def dot():
        print('dot')
    def dash():
        print('dash')
    def sp():
        print('sp')
    def lp():
        print('lp')
    translatorArgs('classic', 'auto', print)
    for char in '.... . .-.. .-.. ---    -.. ..- -.. . ':
        signal(char)
    signalOutputs(dot,dash,sp,lp)
    print(translate('.... . .-.. .-.. ---    -.. ..- -.. .'))