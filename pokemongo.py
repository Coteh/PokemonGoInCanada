# coding=utf-8
import urllib.request
import urllib.error
import sys
from html.parser import HTMLParser

entryToFind = "Pokémon GO"
entryToFind2 = "robots"

class PokemonHTMLParser(HTMLParser):
    """
    Title Method

    Searches for content attributes on all meta tags.
    If it finds one, it will check to see if the substring "Pokémon GO" is contained in
    the attribute's entry.

    If this substring is found, then surely there is an entry for the game on the region's
    App Store and it isn't a redirect or any other type of iTunes page.

    This method may not work for some regions such as Japan where the game may be named
    differently.
    """
    def __init__(self):
        self.foundGo = False
        if (sys.version_info.minor < 4):
            HTMLParser.__init__(self)
        else:
            self.html_parser_init_kwargs = { 'convert_charrefs' : True }
            HTMLParser.__init__(self, **self.html_parser_init_kwargs)
    def handle_starttag(self, tag, attrs):
        if (self.foundGo == False and tag == "meta"):
            for i in range(0,len(attrs)):
                if (attrs[i][0] == "content"):
                    encoded = attrs[i][1].encode(sys.stdout.encoding)
                    if (entryToFind in encoded.decode('utf-8')):
                        # we found it, leave the loop
                        self.foundGo = True
                        break
    def didFindGo(self):
        return self.foundGo

class RobotsHTMLParser(HTMLParser):
    """
    Robots Method

    Searchs for the name attribute on all meta tags.
    If it finds one, it will check to see if the name is "robots".
    If there's such a name, then this is an iTunes redirect page, meaning the Pokemon Go
    app does not exist on that region's App Store yet.

    This occurance ususally happens towards the beginning of the HTML data, so
    for this method to work properly, it is necessary to pass in at least enough
    bytes of text such that the appropriate tag and name are on it.
    """
    def __init__(self):
        self.foundGo = True
        if (sys.version_info.minor < 4):
            HTMLParser.__init__(self)
        else:
            self.html_parser_init_kwargs = { 'convert_charrefs' : True }
            HTMLParser.__init__(self, **self.html_parser_init_kwargs)
    def handle_starttag(self, tag, attrs):
        if (self.foundGo == True and tag == "meta"):
            for i in range(0,len(attrs)):
                if (attrs[i][0] == "name"):
                    encoded = attrs[i][1].encode(sys.stdout.encoding)
                    if (encoded.decode('utf-8') == entryToFind2):
                        # this is an iTunes redirect page, therefore no Pokemon Go
                        self.foundGo = False
                        break
    def didFindGo(self):
        return self.foundGo

class PokemonGoError(Exception):
    """
    PokemonGoError

    Error that is thrown when an error occurs during the checking process.
    """
    pass

def checkForPokemonGo(region):
    """
    checkForPokemonGo

    Checks for Pokemon Go availability for iTunes store of supplied region ID.

    Args:
        region: The iTunes region ID. Usually a two letter string.
    Returns:
        True if it's available, False otherwise.
    Raises:
        PokemonGoError: If an error occured while opening the URL.
    """
    try:
        content = urllib.request.urlopen("https://itunes.apple.com/" + region + "/app/pokemon-go/id1094591345?mt=8")
    except urllib.error.URLError as e:
        raise PokemonGoError("Error loading iTunes URL")
    resultStr = content.read().decode(sys.stdout.encoding) # read the results, which returns as a bytes object, then convert to string object using terminal's encoding
    htmlParser = RobotsHTMLParser()
    htmlParser.feed(resultStr)
    return htmlParser.didFindGo()

def isPokemonGoInCanada():
    """
    isPokemonGoInCanada

    Checks for Pokemon Go availability in Canada.

    Will print an appropriate message that indicates
    whether it is available in Canada or not.

    If an error occured during the process, it will
    print the error instead.
    """
    try:
        if (checkForPokemonGo("ca")):
            print("Pokemon Go is now in Canada!")
        else:
            print("Pokemon Go is not in Canada yet.")
    except PokemonGoError as e:
        print(e)
