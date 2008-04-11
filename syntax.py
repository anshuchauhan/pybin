class Syntax(object):
    """
    Abstracing from pygments in case we want to change syntax highlighting later
    And for cleaner code.
    """

    @classmethod
    def get_syntax_css(cls):
        """returns css styles from pygments for syntax highlighting"""

        from pygments.formatters import HtmlFormatter
        return HtmlFormatter().get_style_defs('.highlight')

    @classmethod
    def get_type_list(cls):
        """returns a list of languages supported"""

        from pygments.lexers import get_all_lexers
        return [(name, aliases) for name, aliases, filetypes, mimetypes in get_all_lexers()]


    @classmethod
    def get_highlighted_code(cls, code, type):

        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter

        lexer = get_lexer_by_name(type.encode().lower())
        #lexer = get_lexer_by_name("python")
        formatter = HtmlFormatter(linenos=True)
        return highlight(code, lexer, formatter)
        

