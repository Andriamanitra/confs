# CONFiguration file Simplified

A (very) simple markup language meant for configuration files.
The entire language syntax is defined in about 30 lines of [Lark](https://github.com/lark-parser/lark) in the `confs.lark` file.

If you want to learn more you may take a look at `example.confs`



I made this because

* YAML is a convoluted mess armed with footguns

* Although [JSON5](https://json5.org/) fixes most of the issues I have with JSON, it is still annoying to edit by hand

* [TOML](https://toml.io/en/) is not terrible but the syntax for lists/maps is just as annoying to edit as JSON

* Executable configuration files (like `config.py` with a bunch of constants) are pretty nice but a little bit scary in practice

* INI is actually quite alright

* I thought having an enum type built-in would be a cool feature to have
