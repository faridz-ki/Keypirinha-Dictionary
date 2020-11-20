# Keypirinha Dictionary
# A dictionary plugin for Keypirinha
This plugin uses the unofficial [Google Dictionary API](https://dictionaryapi.dev/) to find definitions in [Keypirinha](https://keypirinha.com/).

## Usage
To use the plugin, first enter its menu by typing ``dictionary`` into Keypirinha, then enter the word you need the definition for.

In order to get definitions in another language, the plugin uses a similar syntax to the [Translate Package](http://keypirinha.com/packages/googletranslate.html), where you type ``:[language code]`` before the word which you're finding the definition for. You can also change your default language in the config file. A list of supported languages can be found on the [API website](https://dictionaryapi.dev/).

All definitions provided by the dictionary will pop up, so simply select the one you need and press enter to copy it to your clipboard.

## Installation
Seeing as this package is, as of yet, not part of Keypirinha's convenient [PackageControl](https://github.com/ueffel/Keypirinha-PackageControl) plugin, you're going to have to download the ``Dictionary.keypirinha-package`` file from the Releases page of this repository into
- ``Keypirinha\portable\Profile\InstalledPackages`` if you're using Portable mode, or
- ``AppData\Roaming\Keypirinha\InstalledPackages`` if you're using Installed mode.

## Credits
- Thanks, first and foremost to the developers of the Google Dictionary API for the great API.
- Thanks Joe for the idea.

## Release Notes
v0.1.0
- Added initial working package
v0.1.1
- Added support for multiple languages
- Added rudimentary file handling
- Added config file for defaults