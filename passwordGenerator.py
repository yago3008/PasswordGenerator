import argparse
import itertools
import datetime
from itertools import product

def args_parser():
    parser = argparse.ArgumentParser(description="Gerador de padrões de senha.")
    parser.add_argument("-d", "--domain", help="Domínio para incluir no padrão da senha.")
    parser.add_argument("-SD", "--subdomain", action="store_true", help="Subdomínio para incluir no padrão da senha.")
    parser.add_argument("-y", "--year", type=int, help="Inclui o year atual no padrão da senha.")
    parser.add_argument("-S", "--special", action="store_true", help="Inclui caracteres especiais no padrão da senha.")
    parser.add_argument("-U", "--maiuscula", action="store_true", help="Inclui letras maiúsculas no padrão da senha.")
    parser.add_argument("-Sw","--swap", type=str, help="Swap some caracteres, Exemple: s=$;e=&")
    parser.add_argument("-SA", "--swap-all", type=str, help="Swap all caracteres by default dictionary")
    return parser.parse_args()
def get_rules(subdomain, domain, year=False, special=False, maiuscula=False, subdomain_included=False):
    passwords = []
    years = []
    special_chars = []
    if not subdomain_included: subdomain = ''
    
    if maiuscula:
        subdomain = upper_case(subdomain)
        domain = upper_case(domain)
    if year:
        years = get_years(year)
    if special:
        special_chars = ['!', '#', '$', '@', '*']
    passwords = get_password(subdomain, domain, years, special_chars)

    return passwords

def get_password(subdomain, domain, years=None, special=None):
    passwords = []

    # Garante que sejam listas, e se vazio vira lista com string vazia para iterar
    if not subdomain:
        subdomain = ['']
    elif isinstance(subdomain, str):
        subdomain = [subdomain]

    if not domain:
        domain = ['']
    elif isinstance(domain, str):
        domain = [domain]

    # Se None, inicializa com lista vazia
    if years is None:
        years = []
    if special is None:
        special = []

    for sub_part in subdomain:
        for dom_part in domain:
            if years and special:
                for y in years:
                    for s in special:
                        password_parts = [sub_part, dom_part]
                        if y:
                            password_parts.append(str(y))
                        if s:
                            password_parts.append(s)
                        for perm in itertools.permutations(password_parts):
                            passwords.append("".join(perm))
            elif years:
                for y in years:
                    password_parts = [sub_part, dom_part]
                    if y:
                        password_parts.append(str(y))
                    for perm in itertools.permutations(password_parts):
                        passwords.append("".join(perm))
            elif special:
                for s in special:
                    password_parts = [sub_part, dom_part]
                    if s:
                        password_parts.append(s)
                    for perm in itertools.permutations(password_parts):
                        passwords.append("".join(perm))
            else:
                # Nenhum year nem special, só subdomain e domain
                password_parts = [sub_part, dom_part]
                for perm in itertools.permutations(password_parts):
                    passwords.append("".join(perm))

    return passwords

def strip_word(word):
    return list(word)

def split_domain(domain):
    if domain.count('.') == 1:
        domain = domain.split('.')[0]
        subdomain = ''
        return subdomain, domain
    subdomain = domain.split('.')[0]
    domain = domain.split('.')[1]
    return subdomain, domain

def upper_case(word, all=False):
    if all:
        return word.upper()
    variants = product(*[(c.lower(), c.upper()) for c in word])
    return [''.join(p) for p in variants]


def get_years(iterator):
    years = []
    current_year = datetime.datetime.now().year
    for i in range(iterator+1):
        years.append(current_year-i)
    return years

def split_swap(to_split):
    parts = to_split.split(';')
    dictionary = {}

    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            dictionary[key] = value
    return dictionary

def swap_characters(char_to_swap, word):

    default_dictionary = {
        "a": "@",
        "e": "3",
        "i": "!",
        "o": "0",
        "s": "$",
        "t": "7",
    }

    new_word = ""
    dict_with_char_to_swap = default_dictionary if char_to_swap == "all"  else char_to_swap

    for char in word:
        if char in dict_with_char_to_swap:
            new_word += dict_with_char_to_swap[char]
        else:
            new_word += char
    return new_word

def print_array(array):
    print(f"Total passwords: {len(array)}")
    for password in array:
        print(password)

def main():


    args = args_parser()

    if args.domain:
        subdomain, domain = split_domain(args.domain)
        if args.swap:
            char_to_swap = split_swap(args.swap)
            subdomain = swap_characters(char_to_swap, subdomain)
            domain = swap_characters(char_to_swap, domain)
        if args.swap_all:
            subdomain = swap_characters("all", subdomain)
            domain = swap_characters("all", domain)
        passwords = get_rules(subdomain, domain, args.year, args.special, args.maiuscula, args.subdomain)
        print_array(set(passwords))
    else:
        print('Usage: PassGenerator.py -d <domain>')

if __name__ == "__main__":
    main()