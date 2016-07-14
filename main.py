from pokemongo import *
from argparse import ArgumentParser, RawTextHelpFormatter

def main():
    # Initialize parser
    parser = ArgumentParser(prog="PokemonGoInCanada", description="Checks if Pokemon Go is available in Canada.", formatter_class=RawTextHelpFormatter)
    # Initialize sub-parsers
    subparsers = parser.add_subparsers(dest="subCommand", help="PokemonGoInCanada commands")
    # Initialize region sub-parser
    regionParser = subparsers.add_parser("region", help="Check a region. (besides just Canada)")
    regionParser.add_argument("region_id", help="iTunes region ID. Should usually be a two letter abbreviation.")
    # Parse arguments
    args = parser.parse_args()
    # Handle args
    if (args.subCommand == "region"):
        try:
            if (checkForPokemonGo(args.region_id)):
                print("Pokemon Go is available in this region.")
            else:
                print("Pokemon Go is not available in this region yet.")
        except PokemonGoError as e:
            print(e)
    else:
        isPokemonGoInCanada()

if __name__ == "__main__":
    main()
