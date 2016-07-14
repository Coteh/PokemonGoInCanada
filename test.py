import sys
import unittest
from unittest.mock import patch, Mock
import urllib.request
import urllib.error
import http.client
import pokemongo

# Pokemon Go in Canada Test Suite
# --------------------------------
# For the HTML Parser tests, unicode strings
# are encoded to utf-8 in bytes, then passed into
# the feed methods as string decoded into the system's
# default encoding. This is done because the parser expects
# a string that is formatted to the system's default encoding
# so it can then encode that to the system's default encoding
# in bytes, then decode to utf-8.

class TestingPokemonGoMethods(unittest.TestCase):

    def test_pokemonHTMLParser(self):
        parser = pokemongo.PokemonHTMLParser()
        myBytes = "<html><meta content=\"Pokémon GO on the App Store\"></meta></html>".encode("utf-8")
        parser.feed(myBytes.decode(sys.stdout.encoding))
        self.assertEqual(parser.didFindGo(), True)

    def test_pokemonHTMLParser_pokemonGoFind(self):
        parser = pokemongo.PokemonHTMLParser()
        myBytes = "<html><meta content=\"fgfdsdfgsdfgdfsgdfPokémon GOsdfgdsfgfdgdfsgdfg\"></meta></html>".encode("utf-8")
        parser.feed(myBytes.decode(sys.stdout.encoding))
        self.assertEqual(parser.didFindGo(), True)

    def test_pokemonHTMLParser_noContent(self):
        parser = pokemongo.PokemonHTMLParser()
        myBytes = "<html></html>".encode("utf-8")
        parser.feed(myBytes.decode(sys.stdout.encoding))
        self.assertEqual(parser.didFindGo(), False)

    def test_pokemonHTMLParser_noPokemonGo(self):
        parser = pokemongo.PokemonHTMLParser()
        parser.feed("<html><meta content=\"Digimon NO\"></meta></html>")
        self.assertEqual(parser.didFindGo(), False)

    def test_robotsHTMLParser(self):
        parser = pokemongo.RobotsHTMLParser()
        myBytes = "<HTML><HEAD><meta name=\"robots\" content=\"noindex,nofollow\"></HEAD></HTML>".encode("utf-8")
        parser.feed(myBytes.decode(sys.stdout.encoding))
        self.assertEqual(parser.didFindGo(), False)

    def test_robotsHTMLParser_noRobots(self):
        parser = pokemongo.RobotsHTMLParser()
        myBytes = "<HTML><HEAD><meta name=\"somethingelse\" content=\"noindex,nofollow\"></HEAD></HTML>".encode("utf-8")
        parser.feed(myBytes.decode(sys.stdout.encoding))
        self.assertEqual(parser.didFindGo(), True)

    def test_robotsHTMLParser_noName(self):
        parser = pokemongo.RobotsHTMLParser()
        myBytes = "<HTML><HEAD><meta content=\"noindex,nofollow\"></HEAD></HTML>".encode("utf-8")
        parser.feed(myBytes.decode(sys.stdout.encoding))
        self.assertEqual(parser.didFindGo(), True)

    @patch("urllib.request.urlopen")
    def test_checkForPokemonGo(self, urlopen_mock):
        urlopen_mock.return_value = Mock(spec=http.client.HTTPResponse)
        urlopen_mock.return_value.read.return_value = "<html><meta content=\"Pokémon GO on the App Store\"></meta></html>".encode("utf-8")
        self.assertEqual(pokemongo.checkForPokemonGo("us"), True) # those bastards!

    @patch("urllib.request.urlopen")
    def test_checkForPokemonGoErrorHandling(self, urlopen_mock):
        urlopen_mock.side_effect = urllib.error.URLError("Error retrieving webpage")
        with self.assertRaises(pokemongo.PokemonGoError):
            pokemongo.checkForPokemonGo("us")

    @patch("pokemongo.checkForPokemonGo")
    def test_PokemonGoCanadaCall(self, checkForPokemonGo_mock):
        pokemongo.isPokemonGoInCanada()
        pokemongo.checkForPokemonGo.assert_called_once_with("ca")

if __name__ == "__main__":
    unittest.main()
