import os
class PeomToXmlConverter:
    def __init__(self, poemFile):
        self.xmlwriter = XMLWriter()
        self.poemFile = poemFile
        self.foundTitle = False
        self.foundLinePurpose = False
        self.inStanza = False
        self.stanzaNum = 0
        self.lineNum = 0
        self.rhymingPrevLetter = ''
        
    def _checkTitle(self,line):
        strippedLine = ''.join(line.split())
        if (len(strippedLine)>0 and self.foundTitle==False and self.foundLinePurpose==False):
            self.foundLinePurpose = True
            self.foundTitle = True
            self.xmlwriter.new_tag_without_closing_bracket('title')
            self.xmlwriter.insertFreeText(line)
            self.xmlwriter.close_last_open_tag()
            
    def _checkStanza(self,line):
        strippedLine = ''.join(line.split())
        if (len(strippedLine)>0 and self.foundTitle==True and self.foundLinePurpose==False and self.inStanza==False):
            self.inStanza= True
            rhymingPrevLetter = ''
            self.stanzaNum += 1
            
            stanzaAttr = {'number':str(self.stanzaNum)}
            
            self.xmlwriter.new_tag_without_closing_bracket('stanza',**stanzaAttr)
            
            
    def _checkStanzaLine(self,line):
        if (self.foundTitle==True and self.foundLinePurpose==False and self.inStanza==True):
            #if in stanza, the line isn't empty
            self.foundLinePurpose = True
            self.lineNum += 1
            
            stanzaLineAttr = {'number':str(self.lineNum)}
            self.xmlwriter.new_tag_without_closing_bracket('line',**stanzaLineAttr)
            
#             lastLetter = _checkLastLetter(line) #self.rhymingPrevLetter
#             if(lastLetter == self.rhymingPrevLetter)
            
            self.xmlwriter.insertFreeText(line)
            self.xmlwriter.close_last_open_tag()
            
    def _checkEndOfStanza(self,line):
        strippedLine = ''.join(line.split())
        if (len(strippedLine)==0 and self.foundTitle==True and self.foundLinePurpose==False and self.inStanza==True):
            self.foundLinePurpose=True
            self.inStanza= False
            self.xmlwriter.close_last_open_tag() #assuming the last still opened tag is a stanza
            
    def _checkLastLetter(self,line):
        if (self.foundTitle==True and self.foundLinePurpose==False and self.inStanza==True):
            #if in stanza, the line isn't empty
            lastLetter = ''
            for character in line[::-1]:
                unicodeVal = ord(character)
                if unicodeVal >=1488 and unicodeVal<=1514:#hebrew letters unicode values
                    lastLetter = character
                    break
            return lastLetter
            
                
        
    def convert(self): #returns XMLWriter object
        foundTitle = False
        with open(self.poemFile,'r') as f:
            for line in f:
                self.foundLinePurpose = False
                self._checkTitle(line)
                self._checkEndOfStanza(line)
                self._checkStanza(line)
                self._checkStanzaLine(line)
        
        
        return self.xmlwriter
    
    
        
        

def main():
    POEMS_DIR     = 'poems_parsed_by_Ilay_and_Raz'
    POEMS_XML_DIR = 'poems_xml_by_Ilay_and_Raz'

    if os.path.isdir(POEMS_XML_DIR):
        shutil.rmtree(POEMS_XML_DIR)
    try:
        os.makedirs(POEMS_XML_DIR)
    except:
        print('ERROR CREATING FOLDER "'+POEMS_XML_DIR+'". MAKE SURE THERE IS NO INSTANCE OF THIS FOLDER OPEN BEFORE RUNNING THIS SCRIPT.')
        traceback.print_exc()
        sys.exit(1)
    
    
#     xmlwriter = XMLWriter()

#     someDict = {'afa':'g5g','k5g9gk':'aaag1'}
#     xmlwriter.new_tag_without_closing_bracket('lala',**someDict)
#     xmlwriter.new_tag_without_closing_bracket('paca')

#     xmlwriter.insertFreeText('&amp;&amp;&lt;&hki;&quot;')
    
    allPoems = glob.glob(POEMS_DIR+'/*.txt')

    for poem in allPoems:
        converter = PeomToXmlConverter(poem)
        xmlwriter = converter.convert()
                
#         print(xmlwriter.getFinalXmlStr())
        poemFileBaseName = os.path.splitext(os.path.basename(poem))[0]
        poemXmlFileName  = POEMS_XML_DIR+'/'+poemFileBaseName+'.xml'
        with open(poemXmlFileName,'w') as f:
            f.write(xmlwriter.getFinalXmlStr())
    
if __name__ == '__main__':
    print('starting...')
    main()
    print('Done!!!')