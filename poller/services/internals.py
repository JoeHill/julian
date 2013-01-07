import re
import sys
import time
import datetime

from bs4 import BeautifulSoup
from bs4 import Comment
from bs4 import Declaration
from bs4 import CData
from bs4 import Doctype

import pycurl
import StringIO

from poller.services.exceptions import EmptyDOM
from poller.services.exceptions import NoDate

from discourse.api import note

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
        """
        A generator which fetches pages from an RSS feed one by one.
        
        :rtype <generator>: Returns a tuple of the link to the feed and the text of the feed.
        """
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
    
    def entries(self):
        """
        Returns the list of entries for the page
        
        :rtype list(element):
        """
        if not self.DOM:
            self.parse()
        return [ item for item in self.DOM.findAll( 'entry' ) ]
    
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

    def process_as_rss(self, document):
        """
        Processes a document assuming RSS format. It follows the links to the articles 
        and saves them with the appropriate priority for the tag text is found under.
        
        :param unicode document: The RSS source code
        
        :rtype None:
        """
        self.document = document
        self.parse()
        items = self.items()
        for item in items:
            pubdate = item.findAll('pubdate')
            published_at = self.get_datetime( pubdate.pop().get_text() )
            links = [ link.next_sibling for link in item.findAll( 'link' ) ]
            for link in links:
                if not link or note.exists( link ):
                    continue
                try:
                    self.fetch_and_clean_dom( link )
                except EmptyDOM: # Server returned an empty response.
                    continue
                prioritya = ".  ".join( self.h1s() )
                priorityb = ".  ".join( self.h2s() )
                priorityc = ".  ".join( self.h3s() )
                priorityd = ".  ".join( [ a[0] for a in self.as_() ] )
                prioritye = " ".join( self.ps() )
                
                n, errors = note.get_or_create( link, prioritya, priorityb, priorityc, priorityd, prioritye, published_at )
                if errors[0]:
                    sys.stderr.write( str( errors ) + "\n" )
                    
    def get_datetime(self, published_at):
        """
        Takes a 'pubdate' tag content and attempts to convert it to a datetime.datetime object.
        
        :param unicode published_at: The <pubdate> tag contents. Ideally format will be in ( "%a, %d %b %Y %H:%M:%S +0000", "%a, %d %b %Y %H:%M:%S %Z" )
        
        :rtype datetime.datetime:
        """
        # Sat, 05 Jan 2013 03:55:54 +0000
        if not published_at:
            return datetime.datetime.now()
        if '+' in published_at:
            t = time.strptime( published_at, "%a, %d %b %Y %H:%M:%S +0000" )
        elif 'MT' in published_at:
            t = time.strptime( published_at, "%a, %d %b %Y %H:%M:%S %Z" )
        else:
            raise NoDate( "No date could be discerned from <" + str( published_at ) + ">")

        year = t.tm_year
        month = t.tm_mon
        day = t.tm_mday
        hour = t.tm_hour
        minute = t.tm_min
        second = t.tm_sec
        return datetime.datetime( year=year, month=month, day=day, hour=hour, minute=minute, second=second )
    
    def __exit(self):
        pass
