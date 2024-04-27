import argparse
import lrparsing
from lrparsing import Keyword, List, Prio, Ref, THIS, Token, Tokens

class LuaTableParser(lrparsing.Grammar):
    #
    # Put Tokens we don't want to re-type in a TokenRegistry.
    #
    class T(lrparsing.TokenRegistry):
        name = Token(re='[a-zA-Z_0-9-\.]+')
        string = Token(re=r'"(?:[^"\\]|\\.)*"')
        line_comment = Token(re='--(?:\n|(?:[^[\n]|\\[=*[^[=])[^\n]*\n)')
        block_comment = Token(re=r'--\[(=*)\[.*?\]\1\]')
    #
    # Grammar rules.
    #
    table_constructor = Ref("table_constructor")
    #
    # Table constructor.
    #
    value = T.name | T.string
    field = '[' + value + ']' + '=' + (value | table_constructor)
    table_constructor = '{' + List(field, Tokens(", ;"), opt=True) + '}'

    START = T.name + '=' + table_constructor
    COMMENTS = T.line_comment | T.block_comment

def main(filename):
    content = load_file_into_string(filename)
    parse_tree = LuaTableParser.parse(content)
    print(LuaTableParser.repr_parse_tree(parse_tree))

def load_file_into_string(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument("filename", help="The name of the file to process")
    #args = parser.parse_args()
    #filename = args.filename
    filename = "mission/syria/mission"
    main(filename)  # execute only if run as a script