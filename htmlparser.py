from enum import Enum
import string
from dic import *
gramm = grammer()
# print(gramm.events)
class Token():
    # token type
    eof = 'END-OF-FILE'
    tag = 'TAG'
    number = 'NUMBER'
    xss = 'Malicous'
    attribut = 'ATTRIBUTE'
    end_tag = 'END_TAG'
    event = "EVENT"


    def __init__(self, type, value, line, line_no, line_pos):
        self.type = type
        self.value = value
        self.line = line
        self.line_pos = line_pos - len(value)
        self.line_no = line_no + 1

    def __str__(self):
        return '{0}:{1}'.format(self.line_no, self.line_pos).ljust(10) + self.type.ljust(15) + self.value
    
class Lexer(object):
    # indentable_keywords = ['']
    end_tag= ['>','">',"'>","/"]
    qout_str = "\'\""
    xss_char="\'\"\:()"
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
        while self.cursor < len(self.code)+1:
            # .................................... MAin Loop
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
                elif char in Lexer.whitespace+Lexer.qout_str:
                    char = self.get_next_char()
                    self.state=0
                else:
                    # print("other")
                    self.state = 99
            #
            # ---------- state = 1 ----------# tag recongitioan
            if self.state == 1:
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
                    print (token)
                self.state=0
                # print(char,self.state)
                if char in Lexer.end_tag:
                    self.state=4
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
                while char in (string.ascii_letters + string.digits):
                    match += char
                    char = self.get_next_char()
                    flag_t = True
                if flag_t:
                    if match+char in gramm.events:
                        token = Token(Token.event, match+char, self.lines[self.line_no], self.line_no, self.line_pos)
                    else:
                        token = Token(Token.attribut, match+char, self.lines[self.line_no], self.line_no, self.line_pos)

                    self.tokens.append(token)
                    print (token)
                self.state=0
            # ........................xss malicous code.........
            if self.state == 3:
                match = ''
                char = self.get_next_char()
                flag_t = False
                while char in (string.ascii_letters + string.digits+Lexer.xss_char):
                    match += char
                    char = self.get_next_char()
                    flag_t = True
                if flag_t:
                    token = Token(Token.xss, match, self.lines[self.line_no], self.line_no, self.line_pos)
                    self.tokens.append(token)
                    print (token)
                self.state=0

            #.........................end Tag........ 
            if self.state == 4:
                match=char
                # print("s4")
                token = Token(Token.end_tag, match, self.lines[self.line_no], self.line_no, self.line_pos)
                self.tokens.append(token)
                print (token)
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
                # if flag_t:
                #     token = Token(Token.xss, match, self.lines[self.line_no], self.line_no, self.line_pos)
                #     self.tokens.append(token)
                #     print (token)
                self.state=0
            if self.state ==99:
                print("errorrr")
                return 0
                

lex = Lexer('<iframe onload iframe onload="javascript:javascript:alert(1)">')
print(lex.tokenise())