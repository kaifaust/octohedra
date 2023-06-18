from collections import Counter, defaultdict
from itertools import chain, combinations
from random import sample
from string import ascii_lowercase

LEXICON = "wiki-samples-lexicon.txt"

lex = {}

with open(LEXICON) as lex_file:
    for line in lex_file:
        word = line.split()[2]
        # print(word)
        if all([letter in ascii_lowercase for letter in word]):
            lex[tuple(sorted(word))] = word
            if len(lex) > 1000:
                break

# print(lex)

trie = defaultdict(dict)


# for word in lex:
#     node = trie
#     for i, letter in word:
#         if letter not in node:
#             if i == len(word):
#                 node[letter] =
#         node[letter]


def counter_to_key(c: Counter):
    return ''.join(sorted(c.elements()))


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))


letters = Counter()
words = []

in_play = {}

# print(in_play.__class__)

turn = 0

while turn < 100:
    turn += 1
    new_letter = sample(ascii_lowercase, 1)[0]
    # print(f"Drew: '{new_letter}'   Available Letters are now: {counter_to_key(letters)}")
    letters.update(new_letter)
    # print(counter_to_key(letters))

    # See if we can steal anything
    for existing_words in reversed(powerset(words)):
        for possible in powerset(letters):
            steal_letters = "".join(existing_words) + "".join(possible)
            possible_key = tuple(sorted(steal_letters))
            if possible_key in lex:
                new_word = lex[possible_key]
                if len(existing_words) > 1:
                    print("DOUBLE STEAL!!!!!!!!!!!!!!")
                print(f"Stole {existing_words} with {possible} to make {new_word}")
                for word in existing_words:
                    words.remove(word)
                letters -= Counter(possible)
                words.append(new_word)

    # print(existing)

    # See if we can make anything from the letters
    for possible in powerset(letters):  # Reverse to grab the longest word
        possible_key = tuple(sorted(possible))
        # print(possible_key)
        if len(possible) < 3:
            continue
        if possible_key in lex:
            new_word = lex[possible_key]
            words.append(new_word)
            letters -= Counter(new_word)
            print(f"Made the word {new_word}   Words are now: {words}")
            break
        # print(possible)
