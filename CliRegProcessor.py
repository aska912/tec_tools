
import re

class CliRegProcessor(object):
    
    def __init__(self):
        # filter [ ...more? y=[yes] q=[quit] > ]
        self.REG_SHOW_MORE   = re.compile(r"\.{3}\w+\?\s(\w+=\[\w+\]\s+){2}\>")
        self.CONTINUE_WORD   = r"\.+\w+\?"
        self.REG_MATCH_ERROR = re.compile(r"(Error)\:")
    
        self.REG_LINE_BREAK   = re.compile(r'\r+')
        self.REG_SPACE        = re.compile(r"\s+")
        self.REG_ENTER        = re.compile(r'\n+')
        self.REG_SPLIT_LINE   = re.compile(r"\-{6,}")
        self.REG_BEGIN_SPACE  = re.compile(r"^\s+")
        self.REG_END_SPACE    = re.compile(r"\s+$")
        self.REG_COLON_SPLIT  = re.compile(r"\s*:\s+")
        self.REG_BEGIN_END_SPACE    = re.compile(r"^\s+$")
        self.REG_BEGIN_OR_END_SPACE = re.compile(r"^\s+|\s+$")
        self.REG_BEGIN_OR_END_ENTER = re.compile(r"^\n+|\n+$")
    
    def filter_line_break(self, string):
        return re.sub(self.REG_LINE_BREAK, '', string)
    
    def filter_space(self, string):
        return re.sub(self.REG_SPACE, '', string)
    
    def filter_split_line(self, string):
        return re.sub(self.REG_SPLIT_LINE, '', string)
    
    def filter_begin_or_end_space(self, string):
        return re.sub(self.REG_BEGIN_OR_END_SPACE, '', string)
    
    def filter_begin_or_end_enter(self, string):
        return re.sub(self.REG_BEGIN_OR_END_ENTER, '', string)
    
    def process_raw_string(self, string):
        return self.filter_split_line(self.filter_line_break(string))
    
    def shelf_slot_port(self, shelf, slot, port):
        return "%d/%d/%s"%(shelf, slot, port)
        
    def shelf_slot(self, shelf, slot):
        return "%d/%d"%(shelf, slot)
    
    
