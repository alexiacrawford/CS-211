'''
Alexia Crawford
CS 211
A bag of letters for finding anagrams.
Associates a cardinality (count) with each character in the bag.
Credits: Worked with Sam
'''

def normalize(phrase: str) -> list[str]:
    """Normalize word or phrase to the
    sequence of letters we will try to match, discarding
    anything else, such as blanks and apostrophes.
    Return as a list of individual letters.
    """
    new_li = []
    for el in phrase:
        if el.isalpha():
            lower = el.lower()
            new_li.append(lower)
    return new_li

class LetterBag:


    def __init__(self, word=""):
        '''Create a LetterBag'''
        self.word = word.strip()
        normal = normalize(self.word)
        self.length = len(normal)
        self.letters = {letter: normal.count(letter) for letter in normal}

    def __len__(self):
        return self.length


    def contains(self, other: "LetterBag") -> bool:
        """Determine whether enough of each letter in other LetterBag
        are contained in this LetterBag"""
        for letter, count in other.letters.items():
            if letter not in self.letters or self.letters[letter] < count:
                return False
        return True

    def copy(self) -> "LetterBag":
        """Make a copy before mutating."""
        copy_ = LetterBag()
        copy_.word = self.word
        copy_.letters = self.letters.copy()  # Copied to avoid aliasing
        copy_.length = self.length
        return copy_

    def take(self, other: "LetterBag") -> "LetterBag":
        """Return a LetterBag after removing
        the letters in other.  Raises exception
        if any letters are not present.
        """
        bag = self.copy()
        for letter, count in other.letters.items():
            assert letter in bag.letters and bag.letters[letter] >= count
            bag.letters[letter] -= count
            bag.length -= count
        return bag

    def __str__(self):
        return self.word

    def __repr__(self):
        counts = [f"{ch}:{n}" for ch, n in self.letters.items() if n > 0]
        return f'LetterBag({self.word}/[{", ".join(counts)}])'