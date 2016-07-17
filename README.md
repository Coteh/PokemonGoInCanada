# Pokémon Go in Canada

[![Build Status](https://travis-ci.org/Coteh/PokemonGoInCanada.svg?branch=master)](https://travis-ci.org/Coteh/PokemonGoInCanada)

**It's been a wild ride! Pokemon Go is now officially released in Canada! Thanks for tuning in to this project!**

Out of my frustration over Pokemon Go not released in Canada yet, I whipped up this small terminal app in Python 3 that will tell you if it's out in Canada yet or not.

There are currently two methods that can be used to determine availability.

## Method 1: Title Method
Figures it out by making a HTML request to the region's iTunes page for the game (an app has the same ID for all regions) and checking the content attributes on meta tags.
If there's a content attribute that contains the substring "Pokémon GO", then that means there's a page on the region's iTunes store for the game.

## Method 2: Robots Method
Assumes that Pokemon Go is available until it reads a meta tag's name that says "robots". This means that the page is an iTunes redirect,
and not an actual App Store page for the game. If there's no App Store page for the game yet, then it is not available in the region yet.
