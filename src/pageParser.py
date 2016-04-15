# -*- coding: utf8 -*-
import argparse
import urllib2
import unicodedata

from BeautifulSoup import BeautifulSoup

class PageParser:
    def __init__(self, argsparser):
        argsparser.add_argument('-u', '--url',
                                help='url to the creator main page',
                                default="http://benyehuda.org/tuvya/",
                                required=False)
        self.args = argsparser.parse_args()
        self.url = self.args.url

    def parseMainPage(self):
        html = urllib2.urlopen(self.url)
        parsed_html = BeautifulSoup(html)
        all_a=parsed_html.findAll("a",href=True)
        creations=dict()
        for a in all_a:
            if a['href'].startswith("http") | a['href'].startswith("mail") | a['href'].startswith('aximan'):
                print 'skipping ' +a['href']
                continue
            title = a.text
            text=self.parseSubPage(self.url+a['href'])
            creations[title]=text
            print title
            print creations[title]

        f = open('output.txt', 'w')
        for key, value in creations.iteritems():
            f.write(value)
        return

    def parseSubPage(self,url):
        print 'parsing '+url
        html = urllib2.urlopen(url)
        parsed_html = BeautifulSoup(html)
        text=""
        for span in parsed_html.findAll("span"):
            spanText=span.text.encode('utf8')
            if ("לתוכן הענינים" in spanText) | ("פרויקט בן-יהודה" in spanText):
                print 'skipping '+span.text
                continue
            spanText=spanText.replace('\r\n',' ')
            print spanText
            text+=spanText+'\n'
        print text
        return text




def main():
    argsParser = argparse.ArgumentParser()
    pageParser = PageParser(argsParser)

    pageParser.parseMainPage()


if __name__ == '__main__':
    main()
