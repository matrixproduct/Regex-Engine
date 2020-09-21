import sys
sys.setrecursionlimit(10000)
regex_list = []


def comp_begin(text, regex):  # check if the beginning of text matches with regex
    if not regex:
        return True
    if not text:
        return False
    if regex[0] == '.' or regex[0] == text[0]:
        return comp_begin(text[1:], regex[1:])
    return False


#  generates all possible regex from a given one using ?, *, +.
#  l is the maximum length of the generated regex
def generate_regex(regex, l):
    global regex_list
    ind = 0
    while regex[ind:] != '':
        char = regex[ind]
        if char == '\\':
            ind += 1
        if char == '?':
            replicate_regex(regex, ind, 0, 1, l)
            return
        if char == '*':
            replicate_regex(regex, ind, 0, l, l)
            return
        if char == '+':
            replicate_regex(regex, ind, 1, l, l)
            return
        ind += 1
    if len(regex) <= l:
        if len(regex) > 1: # remove all "\\" apart from "\\\\"
            for ind in range(len(regex[:-1])):
                if regex[ind] == '\\':
                    regex = regex[:ind] + regex[ind + 1:]
        regex_list.append(regex)


def replicate_regex(regex, ind, rep_min, rep_max, l): # remove regex[ind] and replicate regex[ind - 1]
    for i in range(rep_min, rep_max + 1):
        generate_regex(regex[:ind - 1] + regex[ind - 1] * i + regex[ind + 1:], l)


def comp(text, regex):  # check if text contains regex and handle $ and ^
    if not regex:
        return True
    if not text:
        return False
    if regex[0] == '^' and regex[-1] == '$':
        return comp_begin(text, regex[1: -1]) and comp_begin(text[-len(regex) + 2:], regex[1:-1])
    elif regex[0] == '^':
        return comp_begin(text, regex[1:])
    elif regex[-1] == '$':
        return comp_begin(text[-len(regex) + 1:], regex[:-1])
    elif comp_begin(text, regex):
        return True
    else:
        return comp(text[1:], regex)


def comp_meta(text, regex):  # check if text contains regex which may contain metacharacters $, ^, ?, *, +
    # first generate all possible regex with the length < len(text)+2 to take into account $ and ^
    generate_regex(regex, len(text) + 2)
    for new_regex in regex_list:
        if comp(text, new_regex):
            return True
    return False


_regex, _text = input().split('|')
print(comp_meta(_text, _regex))

