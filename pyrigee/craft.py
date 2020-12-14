'''
File containing definition of Craft class and relevant constants
'''

'''
Class used for defining spacecraft to orbit a body
'''
class Craft:
    '''
    Init function takes craft's name and the craft's color
    '''
    def __init__(self, n, c):
        self.name = n
        self.color = c