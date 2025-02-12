"""Test cases for anagram.py"""

import unittest
import anagram
import letter_bag


class Test_Read(unittest.TestCase):
    """Test reading and sorting the word list"""
    def test_read(self):
        """Just reading the word list"""
        with open("data/cs_sample.txt") as f:
            words = anagram.read_word_list(f)
        expect = ["transform", "mop", "income", "secret",
                   "cup", "use", "eccentric"]
        self.assertListEqual(words, expect)

    def test_search_simple(self):
        """Search should automatically ignore non-letter characters"""
        with open("data/cs_sample.txt") as f:
            words = anagram.read_word_list(f)
        candidates = [letter_bag.LetterBag(word) for word in words]
        target = letter_bag.LetterBag("Computer science!")
        anagrams = anagram.search(target, candidates)
        self.assertListEqual(anagrams, ["mop use eccentric", "income secret cup"])


if __name__ == "__main__":
    unittest.main()