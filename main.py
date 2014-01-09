#!/usr/bin/env python
from flask import Flask, request
from ansi2html import Ansi2HTMLConverter
from pyfiglet import Figlet, FigletFont
from textwrap import dedent
from random import choice, shuffle
app = Flask(__name__)

def convert2HTML(ansi):
    conv = Ansi2HTMLConverter()
    html  = conv.convert(ansi)
    return html

def clean_string_literal(text):
    """
    String literals in python contain lots of extra whitespace that isn't needed.
    For example leading tabs so that the literal matches the function's tab level.
    In addition leading and trailing newlines
    """
    return dedent(text).strip()

@app.route('/')
def index():
    usage = clean_string_literal("""
    Use the api: /text/<url encoded text>
    Example:

    /text/hello%20bob
    /text/nope
    """)

    browser = request.user_agent.browser
    if browser:
        return convert2HTML(usage)
    else:
        return usage + "\n"

@app.route('/text/<text>')
def textApi(text=None):
    user_requested_font = request.args.get('font')
    font = getFont(user_requested_font)

    text = text or "Send us text!"
    fig = Figlet(font=font)
    ansi = fig.renderText(text)

    if request.user_agent.browser:
        return convert2HTML(ansi)
    else:
        return ansi

def getFont(font):
    """
    The font selection logic.

    There are several possible results.

    1. If random is selected a random font will be returned.
    2. If multiple (comma seperated) fonts are given a random one will be used
    3. If a font is selected it will be verified and then returned
    4. If no font is selected or the font doesn't exist the default font will be returned
    """
    default_font = "slant"
    fonts = FigletFont().getFonts()

    if font == None:
        return default_font
    elif font == "random":
        return choice(fonts)
    elif "," in font:
        # Build a random list of possible fonts
        user_fonts = font.split(',')
        shuffle(user_fonts)

        # For each font validate it exists or move to the next font
        for current_font in user_fonts:
            if current_font in fonts:
                return current_font

        # If none of the potential fonts exists return the default
        return default_font
    elif font in fonts:
        # Verify that the selected font exists
        return font
    else:
        # Catchall default font
        return default_font

def main(debug=False):
    app.run(host="0.0.0.0", debug=debug)

if __name__ == '__main__':
    main(debug=True)
