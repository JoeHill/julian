import urllib
import re
from bs4 import BeautifulSoup

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
  
  def get( self, url, params={} ):
    """
    Fetches a url using GET. Passes params as a query string.

    :param str url: The url to fetch.
    :param dict params: The parameters to pass as a query string

    :rtype str: The document as a string.
    """
    params = urllib.urlencode( params )
    handle = urllib.urlopen( url, params )
    self.document = handle.read()
    handle.close()
    return self.document  

  def parse( self ):
    """
    Parses the internally stored document to provide an interface to the DOM

    :rtype instance: An instance of the BeautifulSoup object
    """
    if not self.document:
      raise Exception( "No document set in poller" )
    self.DOM = BeautifulSoup( self.document )
    return self.DOM

  def __h1s( self ):
    """
    Returns the list of text contents of h1 tags for the page, stipped.

    :rtype list(unicode):
    """
    if not self.DOM:
      self.__parse()
    return [ self.__unicode_strip( h1.text ) for h1 in self.DOM.findAll( 'h1' ) ] 

  def __h2s( self ):
    """
    Returns the list of text contents of h2 tags for the page, stipped.

    :rtype list(unicode):
    """
    if not self.DOM:
      self.__parse()
    return [ self.__unicode_strip( h2.string ) for h2 in self.DOM.findAll( 'h2' ) ]

  def __h3s(self):
    """
    Returns the list of text contents of h3 tags for the page, stipped.

    :rtype list(unicode):
    """
    if not self.DOM:
      self.__parse()
    return [ self.__unicode_strip( h3.string ) for h3 in self.DOM.findAll( 'h3' ) ]

  def __as(self):
    """
    Returns the list of text contents of a tags for the page, with their link address, stipped.

    :rtype list(tuple(<string>,<string>)): A list of tuples of ( text, address )
    """
    if not self.DOM:
      self.__parse()
    return [ ( self.__unicode_strip( a.string ), a.get('href') ) for a in self.DOM.findAll( 'a' ) ]

  def __ps(self):
    """
    Returns the list of text contents of h1 tags for the page, stipped.

    :rtype list(unicode):
    """
    if not self.DOM:
      self.__parse()
    return [ self.__unicode_strip( p.string ) for p in self.DOM.findAll( 'p' ) ]

  def exit(self):
    pass

  def parse_rss( self, document ):
    print "parse rss called."
    page = BeautifulSoup( document )
    items = page.findAll( 'item' )
    print "FOUND " + str( len( items ) ) + " items"
    for item in items:
      print "================================================"
      print "Title:"
      print [ title.text for title in item.findAll( 'title' ) ]
      print "Link:"
      print [ link.text for link in item.findAll( 'link' ) ]
      print "Comments:"
      print [ comment.text for comment in item.findAll('comment') ]
      print "pubdate: "
      print [ pubdate.text for pubdate in item.findAll('pubdate')]
      print "================================================"
