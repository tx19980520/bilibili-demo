import spynner
import pyquery
import time
import BeautifulSoup
import sys
from scrapy.http import HtmlResponse
class WebkitDownloaderTest( object ):
    def process_request( self, request, spider ):
        browser = spynner.Browser()
        browser.create_webview()
        browser.set_html_parser(pyquery.PyQuery)
        browser.load(request.url, 20)
        try:
                browser.wait_load(10)
        except:
                pass
        string = browser.html
        string=string.encode('utf-8')
        renderedBody = str(string)
        return HtmlResponse( request.url, body=renderedBody )
