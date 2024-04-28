import argparse
import os
import lrparsing
from build_utils import getDCSPath, getRepoDirectory, replace_file_content, load_file_into_string
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

# parse_tree consists of tuples.
# each tuple:
#   - 0: the rule
#   - 1+: matched elements

class LuaTable:
    def __init__(self, parse_tree):
        self.name = parse_tree[1][1]     
        self.table = self.get_dict_from_table_constructor(parse_tree[3]) 
    
    def get_dict_from_table_constructor(self, table_constructor):
        assert table_constructor[0].name == "table_constructor"
        table = {}
        for x in range(2, len(table_constructor)):
            field = table_constructor[x]
            if field[0].name == "field":
                self.add_field(table, field)    
        return table

    def add_field(self, dict, field_node):
        assert field_node[0].name == "field"
        key = field_node[2][1][1]
        if field_node[5][0].name == "table_constructor":
            value = self.get_dict_from_table_constructor(field_node[5])
        else:
            value = field_node[5][1][1]
        dict[key] = value

    def serialize_dict(self, table, indent):
        if indent == 0:
            indentation = ''
        else:
            indentation = ' '.ljust(indent)
        inner_indentation = ' '.ljust(indent+4)
        result = f"{indentation}{{\n"
        for key, value in sorted(table.items()):
            if isinstance(value, dict):
                result += f"{inner_indentation}[{key}] = \n{self.serialize_dict(value, indent+4)}, -- end of {key}\n"
            else:
                result += f"{inner_indentation}[{key}] = {value},\n"
        result += f"{indentation}}}"
        return result

    def serialize(self):
        result = f"{self.name} = \n{self.serialize_dict(self.table, 0)} -- end of {self.name}\n"
        return result

def normalize_table(filename):
    content = load_file_into_string(filename)
    parse_tree = LuaTableParser.parse(content)
    table = LuaTable(parse_tree)
    return table.serialize()
    
def normalize_str(filename):
    table = normalize_table(filename)
    normalized = replace_script_file_locations(table)
    return normalized

def replace_script_file_locations(content):
    scripts_dir = os.path.join(getRepoDirectory(), "scripts")
    scripts_dir = scripts_dir.replace("\\", "\\\\\\\\")
    content = content.replace(scripts_dir, "{git_repo_scripts_location_text}")
    scripts_dir = scripts_dir.replace("\\", "\\\\")
    content = content.replace(scripts_dir, "{git_repo_scripts_location}")
    return content

def normalize(filename):
    normalized = normalize_str(filename)
    replace_file_content(filename, normalized)

def main(filename):
    normalized = normalize_str(filename)
    print(normalized)

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument("filename", help="The name of the file to process")
    #args = parser.parse_args()
    #filename = args.filename
    filename = "mission/syria/mission"
    main(filename)  # execute only if run as a script