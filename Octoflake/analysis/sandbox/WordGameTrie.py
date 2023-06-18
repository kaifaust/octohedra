import random
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from string import ascii_lowercase
from typing import List


#######################################################################################################################
"""
First thing, we gotta get some words to play with! I downloaded a corpus from https://www.corpusdata.org/
This doesn't really do anything interesting. Just data munging.

The 
"""

LEXICON = "wiki-samples-lexicon.txt"

lex = defaultdict(list)
max_words = 1000
letter_freq = Counter()

start_read = time.time()
with open(LEXICON) as lex_file:
    for line in lex_file:
        word = line.split()[2]
        # print(word)
        if all([letter in ascii_lowercase for letter in word]) and len(word) >= 3:
            lex["".join(sorted(word))].append(word)
            letter_freq.update(word)
            if len(lex) >= max_words:
                break
end_read = time.time()
# print(letter_freq)

lookup = {}
all_letters = list(letter_freq.elements())


# print(lex)
# lex = {"123": ["321", "123"]}
# print(all_letters)


#### Node structure is node['letter'] = {next_letter : next_node, ... , '-' : word (if terminal)}

@dataclass
class WordNode:
    letters: str
    is_word: bool = False
    words: list[str] = field(default_factory=list)
    next_words: dict = field(default_factory=dict)


def insert(lookup, letters, parent=None, parent_letter=None, word=""):
    key = "".join(sorted(letters))
    if key in lookup:
        if word:
            lookup[key].is_word = True
            lookup[key].words.append(word)
        if parent is not None:
            lookup[key].next_words[parent_letter] = parent
        return

    if key not in lookup:
        lookup[key] = WordNode(key)
        # print(f"Adding {key}")
    if word:
        lookup[key].is_word = True
        lookup[key].words.append(word)
        # print(lookup[key].words)
    if parent is not None:
        lookup[key].next_words[parent_letter] = parent

    letter_list = list(key)
    for i, letter in enumerate(letter_list):
        head, tail = letter_list[:i], letter_list[i + 1:]
        prev_key = "".join(sorted(head + tail))
        insert(lookup, prev_key, parent=key, parent_letter=letter)

        # print(head, letter, tail, prev_key)
        if prev_key not in lookup:
            lookup[prev_key] = WordNode(prev_key)
        lookup[prev_key].next_words[letter] = key


start_build = time.time()
for key, words in lex.items():
    for word in words:
        insert(lookup, key, word=word)
end_build = time.time()

turn = 0

letters_in_play = Counter()  #: List[str] = []
words_in_play = Counter()  # : List[str] = []


def counter_to_key(c: Counter):
    return ''.join(sorted(c.elements()))


def make_key(*strings):
    return "".join(sorted("".join(strings)))


@dataclass
class Stem:
    key: str = field(init=False)
    letters: Counter = field(default_factory=Counter)
    words: Counter = field(default_factory=Counter)

    def __post_init__(self):
        # print("".join(self.letters.elements()), "".join(self.words.elements()))
        self.key = make_key("".join(self.letters.elements()) + "".join(self.words.elements()))

print(Stem(Counter("butts"), Counter(["fart"])))

@dataclass
class Game:
    lookup: dict
    turn : int = field(init=False, default=0)
    number_of_turns: int = 5

    max_stems = 0

    letters_in_play: Counter = field(default_factory=Counter)
    words_in_play: Counter = field(default_factory=Counter)
    stems_in_play: dict[str, Stem] = field(default_factory=dict)

    def purge_stems(self):
        stems_to_remove = []

        for key, stem in self.stems_in_play.items():
            if not stem.letters <= self.letters_in_play:
                stems_to_remove.append(key)
            elif not stem.words <= self.words_in_play:
                stems_to_remove.append(key)
            elif key not in lookup:
                stems_to_remove.append(key)
            elif not lookup[key].next_words:
                stems_to_remove.append(key)

        for key in stems_to_remove:
            self.stems_in_play.pop(key)

    def add_letter(self, new_letter):
        self.letters_in_play.update(new_letter)
        stems_to_add = [Stem(Counter(new_letter))]
        for key, stem in self.stems_in_play.items():
            possible_new_stem = Stem(stem.letters + Counter(new_letter), stem.words)
            # stem_node = lookup[key]
            if possible_new_stem.key in lookup:
                stems_to_add.append(possible_new_stem)

        for stem in stems_to_add:
            self.stems_in_play[stem.key] = stem



    def add_word(self, new_word):
        self.words_in_play.update([new_word])
        stems_to_add = []
        for key, stem in self.stems_in_play.items():
            stems_to_add.append(Stem(stem.letters, stem.words + Counter([new_word])))

        for stem in stems_to_add:
            self.stems_in_play[stem.key] = stem

        self.max_stems = max(self.max_stems, len(self.stems_in_play))

    def check_for_new_words(self):
        new_word = None
        for key, stem in self.stems_in_play.items():
            stem_node = lookup[key]
            if stem_node.is_word:
                new_word = stem_node.words[0]
                # print("Found a word!", new_word, stem)
                # if stem.words:
                #     print("Steal!", new_word, stem)
                if len(stem.words) > 1:
                    print(f"MMMMMMMMulti Steal!!!! Made '{new_word}' from {list(stem.letters.elements())} and {list(stem.words.elements())}")
                self.words_in_play.subtract(stem.words)
                self.letters_in_play.subtract(stem.letters)
                self.add_word(new_word)
                break


    def take_turn(self):
        self.turn += 1
        new_letter = random.choice(all_letters)
        self.add_letter(new_letter)
        self.check_for_new_words()
        self.purge_stems()

    def print(self):

        print(f"Turn: {self.turn} Stems in play: {len(self.stems_in_play)}")
        print(f"\tLetters: '{counter_to_key(self.letters_in_play)}' Words: {list(self.words_in_play.elements())}")

    def play(self):
        while self.turn < self.number_of_turns:
            game.take_turn()
            # game.print()


start_play = time.time()
game = Game(lookup,number_of_turns=1000)
game.play()
end_play = time.time()

print(set(game.words_in_play))
print(f"{len(game.words_in_play)=}")
print(f"{game.max_stems=}")


print("Time to read in words:", end_read-start_read)
print("Time to build lookup:", end_build-start_build)
print("Time to play::", end_play-start_play)
