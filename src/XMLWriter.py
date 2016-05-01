import os
import shutil
import traceback
import sys
import glob

ENABLE_PRINTS = False

class XMLWriter:
    
    
    def __init__(self):
        self.xmlStr = '<?xml version="1.0" encoding="utf-8"?>\n' #header
        self.openTags = []
        pass
    
    def new_tag_without_closing_bracket(self,tag,**kwargs):
        tag = str(tag)
        self.openTags.append(tag)
        self.xmlStr+='<'+tag
        
        for key in kwargs.keys():
            self.xmlStr+=' '+key+'="'+kwargs[key]+'"'
    
        self.xmlStr+='>\n'
    
    def new_tag_with_closing_bracket(self,tag,**kwargs):
        tag = str(tag)
        self.xmlStr+='<'+tag
        for key in kwargs.keys():
            self.xmlStr+=' '+key+'="'+kwargs[key]+'"'
            
        self.xmlStr+='/>\n'
    
    def close_last_open_tag(self):
        
        if not len(self.openTags)>0:
            raise Exception('No open tag to close')
        self.xmlStr+='</'+self.openTags[-1]+'>\n'
        del self.openTags[-1]
    
    def insertFreeText(self,text):
        
        #save xml unique characters
        textWithoutAmpersands = text.split('&amp;')
        if ENABLE_PRINTS:
            print('free text - without amps: '+ str(textWithoutAmpersands))
        validTextAmpParts = []
        for textPartAmp in textWithoutAmpersands:
            textWithoutLt = textPartAmp.split('&lt;')
            if ENABLE_PRINTS:
                print('  free text - without lt: '+ str(textWithoutLt))
            validTextLtParts = []
            for textPartLt in textWithoutLt:
                textWithoutGt = textPartLt.split('&gt;')
                if ENABLE_PRINTS:
                    print('    free text - without gt: '+ str(textWithoutGt))
                validTextGtParts = []
                for textPartGt in textWithoutGt:
                    textWithoutApos = textPartGt.split('&apos;')
                    if ENABLE_PRINTS:
                        print('      free text - without apos: '+ str(textWithoutApos))
                    validTextAposParts = []
                    for textPartApos in textWithoutApos:
                        textWithoutAmpLtGtAposQuot = textPartApos.split('&quot;')
                        if ENABLE_PRINTS:
                            print('        free text - without quot: '+ str(textWithoutAmpLtGtAposQuot))
                        
                        validTextQuotParts = []
                        for textPartQuot in textWithoutAmpLtGtAposQuot:
                        
                            #check for invalid characters in xml
                            validAmpText = '&amp;'.join(textPartQuot.split('&'))
                            validAmpLtText = '&lt;'.join(validAmpText.split('<'))
                            validAmpLtGtText = '&gt;'.join(validAmpLtText.split('>'))
                            validAmpLtGtAposText = '&apos;'.join(validAmpLtGtText.split('\''))
                            validAmpLtGtAposQuotText = '&quot;'.join(validAmpLtGtAposText.split('"'))
                            
                            validTextQuotParts.append(validAmpLtGtAposQuotText)
                        validTextAposParts.append('&quot;'.join(validTextQuotParts))
                    validTextGtParts.append('&apos;'.join(validTextAposParts))
                validTextLtParts.append('&gt;'.join(validTextGtParts))
            validTextAmpParts.append('&lt;'.join(validTextLtParts))
        validText = '&amp;'.join(validTextAmpParts)
        
        self.xmlStr+=validText+'\n'
                                  
        
    
    
    def getFinalXmlStr(self):
        for openTag in reversed(self.openTags):#the reverse isn't important
            self.close_last_open_tag()
        return self.xmlStr
    
    