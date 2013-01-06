import re

from bs4 import BeautifulSoup
from bs4 import Comment
from bs4 import Declaration
from bs4 import CData
from bs4 import Doctype

import pycurl
import StringIO

from poller.services.exceptions import EmptyDOM

class Poller:

    document = ""
    DOM      = None

    def __unicode_strip( self, unicode_string ):
        """
        Strips whitespace characters from unicode strings.
    
        :param unicode unicode_string: The string to strip
    
        :rtype unicode: The string with whitespace stripped from the beginning and end
        """
        left = re.compile( "^\s*" )
        right = re.compile( "\s*$" )
        return right.sub( "", left.sub( "", unicode_string ) )
  
    def get( self, url, params={}, retries=3 ):
        """
        Fetches a url using GET. Passes params as a query string.
    
        :param str url: The url to fetch.
        :param dict params: The parameters to pass as a query string (currently not implemented)
    
        :rtype str: The document as a string.
        """
        self.document = ""
        if not self.document and retries > 0:
            try:
                html = StringIO.StringIO( )
                curl = pycurl.Curl( )
                curl.setopt( pycurl.URL, str(url) )
                curl.setopt( pycurl.FOLLOWLOCATION, True )
                curl.setopt( pycurl.MAXREDIRS, 20 )
                curl.setopt( pycurl.CONNECTTIMEOUT, 30 )
                curl.setopt( pycurl.TIMEOUT, 100 )
                curl.setopt( pycurl.NOSIGNAL, True )
                curl.setopt( pycurl.WRITEFUNCTION, html.write )
                curl.perform()
                self.document = html.getvalue()
            except:
                retries = retries - 1       
                self.get( url, params, retries )
                
        if not self.document:
            raise EmptyDOM( "Failed to get a DOM in get" )
        
        return self.document  

    def fetch_pages(self):
        for feed in self.rss_feeds:
            retries = 3
            feed_text = None 
            while not feed_text and retries > 0:
                try:
                    feed_text = self.get( feed )
                    yield feed, feed_text
                except:
                    retries = retries - 1

    def parse( self ):
        """
        Parses the internally stored document to provide an interface to the DOM
    
        :rtype instance: An instance of the BeautifulSoup object
        """
        if not self.document:
            raise Exception( "No document set in poller" )
        self.DOM = BeautifulSoup( self.document )
        return self.DOM

    def h1s( self ):
        """
        Returns the list of text contents of h1 tags for the page, stipped.
    
        :rtype list(unicode):
        """
        if not self.DOM:
            self.parse()
        return [ self.__unicode_strip( h1.get_text() ) for h1 in self.DOM.findAll( 'h1' ) ] 

    def h2s( self ):
        """
        Returns the list of text contents of h2 tags for the page, stipped.
    
        :rtype list(unicode):
        """
        if not self.DOM:
            self.parse()
        return [ self.__unicode_strip( h2.get_text() ) for h2 in self.DOM.findAll( 'h2' ) ]

    def h3s(self):
        """
        Returns the list of text contents of h3 tags for the page, stipped.
    
        :rtype list(unicode):
        """
        if not self.DOM:
            self.parse()
        return [ self.__unicode_strip( h3.get_text() ) for h3 in self.DOM.findAll( 'h3' ) ]

    def as_(self):
        """
        Returns the list of text contents of a tags for the page, with their link address, stipped.
    
        :rtype list(tuple(<string>,<string>)): A list of tuples of ( text, address )
        """
        if not self.DOM:
            self.parse()
        return [ ( self.__unicode_strip( a.get_text() ), a.get('href') ) for a in self.DOM.findAll( 'a' ) ]

    def ps(self):
        """
        Returns the list of text contents of h1 tags for the page, stipped.
    
        :rtype list(unicode):
        """
        if not self.DOM:
            self.parse()
        return [ self.__unicode_strip( p.get_text() ) for p in self.DOM.findAll( 'p' ) ]
    
    def items(self):
        """
        Returns the list of items for the page
        
        :rtype list(element):
        """
        if not self.DOM:
            self.parse()
        return [ item for item in self.DOM.findAll( 'item' ) ]
    
    def walk_dom(self, dom):
        """
        Walks the elements of a DOM recursively and returns a flattened list of all the elements.
        
        :param BeautifulSoup.BeautifulSoup dom: The DOM to traverse
        
        :rtype list(Element): A list of the elements of the DOM
        """
        elements = []
        for element in dom.contents:
            elements.append(element)
            if hasattr( element, 'contents' ):
                elements += self.walk_dom(element)
        return elements
    
    def fetch_and_clean_dom(self, link):
        """
        Sets the internal DOM to whatever is at 'link' and removes comments, dtds, and cdata
        
        :param str link: The link to fetch a DOM for
        """
        self.get(link)
        self.parse()
        
        flattened_elements = self.walk_dom(self.DOM)
        for element in flattened_elements:
            if isinstance( element, ( Doctype, Declaration ) ):
                element.extract()
            elif isinstance( element, Comment ):
                element.extract()
            elif isinstance( element, CData ):
                element.extract()
            elif hasattr( element, 'name' ) and element.name in ( 'SCRIPT', 'script' ):
                element.extract()
        
    def __exit(self):
        pass
