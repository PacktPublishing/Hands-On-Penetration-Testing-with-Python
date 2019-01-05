"""A String generator class"""

import exrex
import base64
import os

class StringGenerator(object):

    def __init__(self):
        pass

    def get_alpha_only_string(self, limit = 12, min_length = 10):
        regex = '[a-zA-Z]+'

        # if min_length == limit, then?
        if min_length == limit:
            limit = min_length + 1

        if min_length > limit:
            limit, min_length = min_length, limit

        while True:
            gen = exrex.getone(regex)
            if len(gen) in range(min_length, limit):
                return gen


    def get_alpha_numeric_string(self, limit = 16, min_length = 8):
        regex = '[a-zA-Z]*[0-9]+[a-zA-Z]*'

        # if min_length == limit, then?
        if min_length == limit:
            limit = min_length + 1

        if min_length > limit:
            limit, min_length = min_length, limit

        while True:
            gen = exrex.getone(regex)
            if len(gen) in range(min_length, limit):
                return gen


    def get_strong_password(self):
        return base64.urlsafe_b64encode(os.urandom(9))[:-1]


    def get_email_address(self):
        regex = '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)$'
        gen = exrex.getone(regex)
        return gen.lower()


    def get_tautology_string(self, alpha_only = True, QUOTE = 'SINGLE'):
        if alpha_only:
            string = self.get_alpha_only_string()
        else:
            string = self.get_alpha_numeric_string()

        if QUOTE == 'SINGLE':
            quote = "'"
        elif QUOTE == 'DOUBLE':
            quote = '"'
        else:
            quote = ''

        regex = '%s%s  (or \'1\' = \'1\'|or 1 = 1|or \'a\' = \'a\'|or "1" = "1") or %s' %(
                        string, quote, quote)
        gen = exrex.getone(regex)
        return string, gen


    def get_xml_meta_character_string(self, limit = 16, min_length = 8):
        regex = '[a-zA-Z]* (\'|"|<|>|<!--)&[a-zA-Z]*'

        # if min_length == limit, then?
        if min_length == limit:
            limit = min_length + 1

        if min_length > limit:
            limit, min_length = min_length, limit

        while True:
            gen = exrex.getone(regex)
            if len(gen) in range(min_length, limit):
                return gen

    def get_new_attacks(self):
        pass

if __name__ == "__main__":
    a = StringGenerator()
    print a.get_alpha_only_string()
    print a.get_alpha_numeric_string()
    print a.get_strong_password()
    print a.get_email_address()
    print a.get_tautology_string()
    print a.get_tautology_string(QUOTE = '"')
    print a.get_xml_meta_character_string()