from enum import Enum
import string
from dic import *
gramm = grammer()
# print(gramm.events)

class Token():
    # .....token type

    event = 3
    tag = 1
    text = 4
    xss = 4
    attribut = 2
    end_tag = 5
    eof = 'END-OF-FILE'

    # ........
    
    # event = 'EVENT'
    # tag = "TAG"
    # text = "TEXT"
    # xss = "XSS"
    # attribut = "ATTRIBUTE"
    # end_tag = "ENDTAG"
    # eof = 'END-OF-FILE'


    def __init__(self, type, value, line, line_no, line_pos):
        self.type = type
        self.value = value
        self.line = line
        self.line_pos = line_pos - len(value)
        self.line_no = line_no + 1

    def __str__(self):
        return '{0}:{1}'.format(self.line_no, self.line_pos).ljust(10) + self.type.ljust(15) + self.value
        # return f'{self.type} :\t{self.value}'
    
    
class Lexer(object):
    # indentable_keywords = ['']
    end_tag= ['>','">',"'>"]
    contune = [' ','=']
    qout_str = "\'\""
    xss_char="\'\"\:()/.@"
    other_Symbol = '\,\:\;'
    eof_sign = '$'
    whitespace = ' \t\n'
    newline = '\n'
    comment_sign = '#'
    str_sign = '\"\''
    start_braket = '[({'
    end_braket = '])}'
    state = 0

    def __init__(self, code):

        self.code = code
        self.cursor = 0
        self.tokens = []
        self.lines = code.split(Lexer.newline)
        self.line_no = 0
        self.line_pos = 0

    def get_next_char(self):
        self.cursor += 1
        self.line_pos += 1
        if self.cursor > len(self.code):
            return Lexer.eof_sign

        return self.code[self.cursor - 1]

    def this_is_Error(self, charre):
        raise ValueError('\n!!! Error Unexpected character found :Line {0}:{1} -> {2}\n{3}'.format(self.line_no + 1,
                                                                                                   self.line_pos,
                                                                                                   charre,
                                                                                                   self.lines[
                                                                                                       self.line_no]))


    def tokenise(self):
        char = self.get_next_char()
        # while char != Lexer.eof_sign:
        of =0
        while self.cursor < len(self.code)+1 and of <100:
            # .................................... MAin Loop
            of += 1
            # print(self.state)
            flag = True
            if char in Lexer.whitespace:
                if char == '\t':
                    self.line_pos += 4
                if char in Lexer.newline:
                    self.line_no += 1
                    self.line_pos = 0
                char = self.get_next_char()
            #
            # ------------------------------states--------------------------#

            if self.state == 0:
                if char == '<':
                    self.state = 1
                elif char in string.digits:
                    self.state = 0
                elif char in string.ascii_letters:
                    self.state = 2
                elif char == '=':
                    self.state = 3
                elif char in Lexer.end_tag:
                    self.state = 4
                elif char =="\:":
                    self.state = 3
                elif char in Lexer.whitespace+Lexer.qout_str:
                    char = self.get_next_char()
                    self.state=0
                else:
                    # print("other")
                    self.state = 0
            #
            # ---------- state = 1 ----------# tag recongitioan
            if self.state == 1:
                # print(char)
                match = char
                flag_tag = False
                char = self.get_next_char()
                while char in (string.ascii_letters + string.digits):
                    match += char
                    char = self.get_next_char()
                    flag_tag = True
                # flag_tag=False
                if flag_tag:
                    token = Token(Token.tag, match, self.lines[self.line_no], self.line_no, self.line_pos)
                    self.tokens.append(token)
                    self.prt_token(token)
                self.state=0
                if char=='/':
                    self.state=4
                # print(char,self.state)
                # if char in Lexer.end_tag:
                    # self.state=4
                # if match in Token.keywords:
                #     token.type = Token.keyword

                # if char in self.invalid_str:
                #     if self.cursor < len(self.code):
                #         self.this_is_Error(char)

            #................................attribute.. and event
            if self.state == 2:
                match = ''
                # char = self.get_next_char()
                flag_t = False
                while char in (string.ascii_letters + string.digits+':'):
                    match += char
                    char = self.get_next_char()
                    flag_t = True
                if flag_t:
                    if match+char in gramm.events:
                        token = Token(Token.event, match+char, self.lines[self.line_no], self.line_no, self.line_pos)
                    else:
                        token = Token(Token.attribut, match+char, self.lines[self.line_no], self.line_no, self.line_pos)

                    self.tokens.append(token)
                    self.prt_token(token)
                self.state=0
            # ........................xss malicous code.(after =)........
            if self.state == 3:
                match = ''
                flag_t = False
                char = self.get_next_char()
                # while char in (string.ascii_letters + string.digits+Lexer.xss_char):
                while char not in (Lexer.whitespace +'$>/'):
                    match += char
                    char = self.get_next_char()
                    flag_t = True
                if flag_t:
                    token = Token(Token.xss, match, self.lines[self.line_no], self.line_no, self.line_pos)
                    self.tokens.append(token)
                    self.prt_token(token)
                self.state=0

            #.........................end Tag........ 
            if self.state == 4:
                match=char
                # print("s4")
                if char =='/':
                    match= '<'+char
                    char = self.get_next_char()
                    while char in Lexer.whitespace:
                        char =self.get_next_char()
                    while char in string.ascii_letters:
                        match += char
                        char = self.get_next_char()
                    if char=='>':
                        match += char
                token = Token(Token.end_tag, match, self.lines[self.line_no], self.line_no, self.line_pos)
                self.tokens.append(token)
                self.prt_token(token)
                char = self.get_next_char()
                self.state =0
                # print(self.tokens[-1])
                while char ==' ':
                    char =self.get_next_char()
                if char in (string.ascii_letters+string.digits):
                    self.state=5
            #........................other........ 
            if self.state==5:
                match=''
                # char = self.get_next_char()
                flag_t = False
                while char in (string.ascii_letters + string.digits+Lexer.xss_char):
                    match += char
                    char = self.get_next_char()
                    flag_t = True
                if flag_t:
                    if match.__contains__('alert') or match.__contains__('prompt') or match.__contains__('console.log') or match.__contains__('cookie'):
                        token = Token(Token.xss, match, self.lines[self.line_no], self.line_no, self.line_pos)
                    else:
                        token = Token(Token.text, match, self.lines[self.line_no], self.line_no, self.line_pos)
                    self.tokens.append(token)
                    self.prt_token(token)
                self.state=0

            if self.state ==99:
                print("errorrr")
                self.this_is_Error(char)
        # return self.tokens
        
    def get_tokens_type(self):
        temp = []
        for i in self.tokens:
            temp.append(i.type)
        return temp
    
    def get_tokens_value(self):
        temp = []
        for i in self.tokens:
            temp.append(i.value)
        return temp
    
    def prt_token(self,tokem):
        x=tokem
        # print (x)

# lex = Lexer('"><img src=xxx:x onerror=javascript:alert(1)>')
# # lex = Lexer('<script > alert(1) </script>')
# lex.tokenise()
# toktype = lex.get_tokens_type()
# tokValue = lex.get_tokens_value()

# print(toktype)
# print(tokValue)