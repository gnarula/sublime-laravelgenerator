## sublime-laravelgenerator

A Sublime Text plugin that allows you to make use of the [Laravel 4
Generators](https://github.com/JeffreyWay/Laravel-4-Generators) by [Jeffrey
Way](https://github.com/JeffreyWay) directly within Sublime Text.

## Installation

* Install the  [Laravel 4
generator commands](https://github.com/JeffreyWay/Laravel-4-Generators) through Composer.
* Install the ST plugin through Package Control: *Sublime Laravel Generator*
* If you are on Windows or php executable is not in PATH, please specify the path to it in `laravelgenerator.sublime-settings`. To do so, copy `laravelgenerator.sublime-settings` from this
plugin to `<Packages_Directory>/Users/` and make the edits to that file.

## Usage

* Open a Laravel Project
* Open the command palette (Ctrl+Shift+P)
* Execute any of the available Generate commands
* See here for a basic workflow [video](http://tutsplus.s3.amazonaws.com/tutspremium/courses_$folder$/WhatsNewInLaravel4/Laravel-Generators-and-Sublime-Text-Workflow.mp4)

*Note*: `artisan` needs to be in the project root.

## Customization

The plugin is quite extensible. Interested users can extend the plugin for more
artisan commands by adding the appropriate entries in
`Default.sublime-commands`.

## Credits

* [Jeffrey Way](https://github.com/JeffreyWay): for the idea and testing this
  plugin throughout the development.

***

*This is a work in progress. Feedback is appreciated. Feel free to report any
issues you come across*
