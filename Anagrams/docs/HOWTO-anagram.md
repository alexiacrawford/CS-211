# HOWTO find multi-word anagrams

In this project we want to find possible anagrams of
words and phrases, including phrases of more than
one word.  For example, if we search for anagrams
of "computer science", we should find that
"eccentric mop use" and "secret income cup" are
among the possible anagrams.

In a [prior project](https://github.com/UO-CS210/jumbler)
we used a trick to find single word anagrams:  A word and
each of its anagrams are identical when _normalized_ by
listing its letters in alphabetical order.  This made it
possible to compare a normalized version of a jumbled word
with the normalized version of each word in a word list. 

This normalization trick is not sufficient for finding
anagrams that are made of multiple words.  In this project
we will build a multi-word anagram finder using
a recursive algorithm and
a Python class for a _bag_ (also called a _multiset_) of
letters. 

## Learning objectives

The primary learning objectives of this project are
advancing your grasp of

- Python classes and objects. You will construct a moderately
  complex class (`LetterBag`) that records the letters that
  are available and must be used to complete an anagram. 
- Recursive search. Each time we find a word that _could_ be
  included in an anagram, we will consider two possibilities:
  We could include that word, or we could omit it and use the
  letters in a different way.  One of these possibilities will
  be explored with a recursive call. 

## The basic idea

  Consider the phrase "computer science".  If we ignore the space, we can count 3 occurrences of the letter `c`, 2 `e`,
  and 1 occurrence each of `o`, `m`, `p`, `u`, `t`, `r`, `s`,
  `i`, `e`, and `n`.  If we check the word "eccentric", we will see that it can use all 3 `c`s and both `e`s, as well as an `n`, `t`, `r`, and `i`.  If we use "eccentric" in an
  anagram for "computer science", it will leave the letters
  `o`, `m`, `p`, `u`, `s`, and `e`.   We may later find that
  the word "mop" can be built from these remaining letters,
  leaving `u`, `s`, and `e`.  Then we may find that the word
  "use" can be built from these remaining letters.  At this
  point the collection of letters is empty, indicating that we
  have successfully found the anagram "eccentric mop use". 

  We might alternatively choose not to use "eccentric".  We might instead find that the words "income", "secret", and
  "cup" are another way to create an anagram of "computer science".  

## The Plan

The key components of our anagram finder will be 

- A class representing a _bag_ of letters.  In math, a _bag_ is also called a _multiset_.
Whereas a set either contains an element or does not contain it, a _bag_ may
contain zero or more of a given element.  For example, a _bag_ will allow
us to record that "computer science" contains 3 `c` but only one `p`.
We will construct a class `LetterBag` in Python module `letter_bag.py` to
represent bags of letters.  Since this module does not depend on other
modules in our project, we will construct and test it first. 

- A recursive algorithm for finding all the ways that words from a word
list (each represented by a `LetterBag`) can be combined to exactly use
the letters in a phrase (also represented by a `LetterBag`).  We will
express this algorithm as a Python function `search` in the main module of our
program, called `anagram.py`.  Since this algorithm depends heavily on
the `LetterBag` class, we will construct `anagram.py` after constructing
and testing `letter_bag.py`. 

In addition to these two modules that you will construct, you will use
several supporting modules that I have provided.

- `config.py` will contain configuration choices like the location of the
word list file.  I have provided a starter version of this file for you,
along with several possible word lists in the `data` directory. 
- `columns.py` provides a function that arranges a list of strings
in columns.  This can be helpful because the number of anagrams discovered
by our program is often large.  
- `word_heuristic.py` provides a "scoring" function that we can use to
sort the word list, so that longer words and words containing less
common letters (e.g., `q` and `z`) are tried before short words containing
only the most common letter.  This can make the search a little faster,
and make interesting anagrams more likely to appear near the beginning
of a long list of anagrams.  
- `filters.py` provides a set of functions for reducing the size of a
list of discovered anagrams, _after_ we have found all possible anagrams.


## Step 1:  The `LetterBag` class. 

A bag (multiset) of letters can be represented by a Python `dict`
with strings (individual letters) as keys and integers as values.  Encapsulating
this `dict` in a class will allow us to give it some useful operations and
properties, viz, 
- We will define a method `x.contains(y)` that determines whether
`x` has the letters needed to form `y`, that is, whether the value associated
with each letter in `x` is at least as much as the value associated with the
same letter in `y`.  For example, suppose the `dict` in object `x` is 
`{'a': 3, 'b': 2}` and the `dict` in object `y` is `{'a': 2, 'b': 2}`, then 
`x.contains(y)` should be `True` but `y.contains(x)` should be `False`. 
- We will define a method `x.take(y)` that removes letters of `y` from `x`.
`x.take(y)` is allowed only if `x.contains(y)`.  
Suppose the `dict` in object `x` is 
`{'a': 3, 'b': 2}` and the `dict` in object `y` is `{'a': 2, 'b': 2}`, then 
`x.take(y)` should return a LetterBag object containing
`{'a': 1, 'b': 0}` (or equivalently, just `{'a': 1}`).  `y.take(x)` should
raise an exception because 3 `a` is more than 2 `a`. 

Note that `take` returns a value (a `LetterBag` object). It is essential that
it _must not_ have an effect, i.e., `x.take(y)` must not change either `x` or `y`. 

We will construct `LetterBag` objects from words or phrases. We will represent
upper case letters by lower case, and will ignore any character that is not a
letter.  Thus, `LetterBag("Space Ship")` will be identical to
`LetterBag("spaceship")`.  (In other words, we will _normalize_ words and
phrases as we construct their `LetterBag` representations.)

### Normalization

To simplify the `LetterBag` class itself, we'll begin the `letter_bag.py`
module with a separate function for normalization.  

```python
"""A bag of letters for finding anagrams.
Associates a cardinality (count) with each character
in the bag.
"""

def normalize(phrase: str) -> list[str]:
    """Normalize word or phrase to the
    sequence of letters we will try to match, discarding
    anything else, such as blanks and apostrophes.
    Return as a list of individual letters.
    """
```
You can write the `normalize` function as a loop (about 4-5 lines of code).
If you prefer, it is possible express it as a list comprehension in a single
line of code.  Whichever way you choose to write it, you will likely want
to use the `isalpha` method of the `str` class to determine whether a
character in `phrase` is a letter, and the `lower` method of the `str` class
to ensure that any upper case letters are represented by their lower case equivalents.

As soon as you have started the `letter_bag.py` module by writing the `normalize`
function, you should also start another module `test_letter_bag.py` with the
following code: 

```python
"""Test cases for module letter_bag.py."""
import unittest
from letter_bag import normalize

class Test_Normalize(unittest.TestCase):
    """Normalization selects only letters and lowercases them.
    It returns a list of characters, rather than a string."""

    def test_01_normalize_plain_word(self):
        """Simplest case, input is already in normal form"""
        self.assertEqual(normalize("normal"), list("normal"))

    def test_02_skip_punc(self):
        """Omit non-letters"""
        self.assertEqual(normalize("no way! can't be"), list("nowaycantbe"))

    def test_03_lettercase(self):
        """Normalization also lower-cases everything"""
        self.assertEqual(normalize("Make It So"), list("makeitso"))

if __name__ == "__main__":
    unittest.main()
```

These test classes use _inheritance_, an object-oriented feature we haven't
introduced yet, so I will provide all the test code in this project.  However,
you should be able to make sense of the test cases.  For example, the purpose
of `test_02_skip_punc` should be fairly obvious (it makes sure the normalized
version of a string includes only letters) even if `self.assertEqual` is still
a little mysterious. 

### Begin the LetterBag class

For the sake of testing, we will begin the `LetterBag` class (in `letter_bag.py`)
with a constructor along with the magic methods `__len__` (for the `len` function),
`__str__` (for the `str` function, how we want a `LetterBag`
represented to a user), and `__repr__` (for the `repr` function, how
we want a `LetterBag` represented when debugging).  I will provide the
class declaration and the beginning of its constructor: 

```python
class LetterBag:
    """A bag (also known as a multiset) is
    a map from keys to non-negative integers.
    A LetterBag is a bag of single character
    strings.
    """
    def __init__(self, word=""):
        """Create a LetterBag"""
        self.word = word.strip()
        normal = normalize(self.word)
        self.length = len(normal)  # Counts letters only!
```
You must add the part of the constructor that creates `self.letters`,
a dict that contains a count of each letter in `normal`.

Here are `__len__`, `__str__`, and `__repr__` methods consistent with the
part of the constructor I have provided and with the test
cases we'll add in a moment. 

```python
    def __len__(self):
        return self.length

    def __str__(self):
        return self.word

    def __repr__(self):
        counts = [f"{ch}:{n}" for ch, n in self.letters.items() if n > 0]
        return f'LetterBag({self.word}/[{", ".join(counts)}])'
```

Note that the length (`len`) of a `LetterBag` will be the
total number of letters in the bag.
For example, the length of a `LetterBag` containing the `{'a': 3, 'b': 2}` will
be 5.  This may differ from length of the word or phrase from which the
`LetterBag` was constructed, due to the _normalization_ mentioned above).  Also
`len(x.take(y))` should be `len(x) - len(y)`.  This is important because we
will use the remaining length of a `LetterBag` becoming zero 
to determine when we have
used all the letters in a word or phrase to complete an anagram.

This is enough to add a few simple test cases to `test_letter_bag.py`.
Start by importing the class, so that we can write `LetterBag` rather
than `letter_bag.LetterBag` each time we use it: 

```python
from letter_bag import LetterBag
```
Then begin the `Test_LetterBag` class this way: 

```python
class Test_LetterBag(unittest.TestCase):
    """Test cases for the LetterBag class itself"""

    def test_01_construct_observe(self):
        """Basic smoke test of constructor"""
        bag = LetterBag("kooky!")
        # Magic observer methods
        self.assertEqual(len(bag), 5)
        self.assertEqual(str(bag), "kooky!")
        self.assertEqual(repr(bag),
                         f"LetterBag(kooky!/[k:2, o:2, y:1])")
```

Note this test case doesn't even test the value of the instance variable
`letters`, the `dict` structure that is most fundamental to the `LetterBag` class.
We'll test that shortly through the behaviors of the `contains` and `take` methods!

### The `contains` method

`contains` (determining whether the letters in one `LetterBag`
include at least all the letters in another) and `take`
(removing letters in one `LetterBag` from another) are the heart
of the `LetterBag` class, and closely related:
`x.take(y)` is possible only if `x.contains(y)` is true. Our
anagram search will use the `contains` method to determine if
a word from the word list can be included in an anagram, and
if it can, it will use the `take` method to try completing an anagram.

The header of the `contains` method in the `LetterBag` class
should be 

```python
    def contains(self, other: "LetterBag") -> bool:
        """Determine whether enough of each letter in
        other LetterBag are contained in this LetterBag.
        """
```

Be sure it always returns a `bool`, rather than `None`. It
should pass these test cases, which you should add to
class `Test_LetterBag` in
`test_letterbag.py`:

```python
    def test_02_containment(self):
        """Basic containment without modification"""
        bag = LetterBag("total")
        self.assertTrue(bag.contains(LetterBag("tat")))
        self.assertTrue(bag.contains(LetterBag("alt")))
        self.assertFalse(bag.contains(LetterBag("toll")))
        self.assertFalse(bag.contains(LetterBag("talk")))
```

### Watch out for aliases! 

It seems like the `take` method should be almost like the
`contains` method, except that instead of _comparing_ the
value of `self.letters` for each element of `other.letters`,
it should _subtract_ the value of each element in `other.letters`
from the corresponding element in `self.letters`.

But there's a catch!  The `take` method should return a
value (a `LetterBag`) and should not have an effect.
In particular, it should _not_ modify the `dict` `self.letters`.
This is crucial since we want to use it in a recursive search
that tries forming an anagram _with_ and _without_ a word.
If the `take` method had a _side effect_ of modifying the `self`
object (or any of its components, such as `self.letters`),
it would create tricky bugs in our search algorithm. 

How can we return a modified `LetterBag` without actually
changing the `self` object?   We can do so by modifying a
_copy_ of the `self` object instead, and returning that
modified copy. 

Before we write the `take` method, we will write a
`copy` method that the `take` method can use to clone
itself.  Our `copy` method will in turn use the `copy`
method of class `dict` to clone `self.letters`.  I will
provide that for you: 

```python
   def copy(self) -> "LetterBag":
        """Make a copy before mutating."""
        copy_ = LetterBag()
        copy_.word = self.word
        copy_.letters = self.letters.copy()  # Copied to avoid aliasing
        copy_.length = self.length
        return copy_
```
We didn't have to call `copy` on `self.word` (a `str`)
or on `self.length` (an `int`), because `str` and `int`
are _immutable_:  A value of type `int` or `str`
can never change.  But a `dict` is _mutable_.  If we have
two or more references to a single `dict` object, they
are _aliases_.  Changing that one object through either
reference will affect the value seen through both.  You can
see this with the Python console: 

```pycon
>>> d1 = { 'a': 13, 'b': 15 }
>>> d2 = d1
>>> d2['b'] = 0
>>> d2
{'a': 13, 'b': 0}
>>> d1
{'a': 13, 'b': 0}
```
We avoid aliasing by copying:

```pycon
>>> d1 = { 'a': 13, 'b': 15 }
>>> d2 = d1.copy()
>>> d2['b'] = 0
>>> d2
{'a': 13, 'b': 0}
>>> d1
{'a': 13, 'b': 15}
```

We will write the `take` method next, and test `take` and `copy`
together. 

### Build the `take` method

The `take` method of the `LetterBag` class should
have the following header: 

```python
    def take(self, other: "LetterBag") -> "LetterBag":
        """Return a LetterBag after removing
        the letters in other.  Raises exception
        if any letters are not present.
        """
```

The first thing it should do is make a copy of itself, like
this: 

```python
        bag = self.copy()
```

It should then modify `bag`, subtracting the values of
`other.letters` from `self.letters` (i.e., loop through
`other.letters.items()`).  At each adjustment, you should
also write an `assert` statement to be sure the value
in `bag.letters` is sufficient.  You should also adjust
`bag.length` to indicate how many letters are left after
removing those from `other.letters`. 

When you have written `LetterBag.take`, you should add these
test methods to class `Test_LetterBag` in module
`test_letter_bag.py`:

```python
    def test_03_take_result(self):
        """Containment before and after taking letters from bag.
        Note value semantics:  'take' has a result, not an effect.
        """
        bag = LetterBag("fluffy")
        fly = LetterBag("fly")
        self.assertTrue(bag.contains(fly))
        depleted = bag.take(fly)
        self.assertEqual(len(bag), 6)
        self.assertEqual(len(depleted), 3)
        self.assertFalse(depleted.contains(fly))
        self.assertTrue(bag.contains(fly))
        self.assertTrue(bag.contains(LetterBag("uff")))
        self.assertTrue(depleted.contains(LetterBag("uff")))


    def test_04_copy(self):
        """Copying a LetterBag allows us to explore with and
        without taking letters that make a candidate word.
        This is a modified version of test_03_take_effect.
        """
        bag = LetterBag("fluffy")
        fly = LetterBag("fly")
        self.assertTrue(bag.contains(fly))
        dup = bag.copy()
        bag = bag.take(fly)
        self.assertFalse(bag.contains(fly))
        self.assertTrue(bag.contains(LetterBag("uff")))
        self.assertTrue(dup.contains(fly))
        dup2 = bag.copy()  # Copy AFTER removing fly
        self.assertEqual(len(dup2), 3)
        self.assertEqual(len(bag), 3)
        self.assertEqual(len(dup), 6)
        self.assertFalse(dup2.contains(fly))
        self.assertTrue(dup2.contains(LetterBag("uff")))
```

### Checkpoint

At this point you should have: 

- A source file  `letter_bag.py` with a
function `normalize` and a class `LetterBag`. 

- Within class `LetterBag`, methods `__init__` (the construtor),
`__len__`, `__str__`, `__repr__`, `contains`,
`copy`, and `take`.

- A second source file, `test_letter_bag.py`, with
class `Test_Normalize` (3 methods)
and class `Test_LetterBag` (4 methods).

## Searching for anagrams

With the `LetterBag` class in hand, we are
ready to create our main application module
in `anagram.py`. 



### Obtaining the list

The anagrams we can find depend on the word list we use.  There
is no perfect word list that gives us all and only fun or
interesting anagrams.  The more comprehensive word lists
(like the `dict.txt` file we used for single word anagrams)
may drown us a long list of anagrams made of obscure words,
while a more selective list may not contain a word that would
use _just_ the right set of letters to build some more interesting
anagrams.  So, instead of one word list, we have several to
choose from in the `data` directory.  The choice is governed
by a provided configration file, `config.py`.

```python
""Configuration options for multi-word anagram finder"""

# Which word list to use.  You may want longer or shorter word lists depending
# on whether you are getting a flood or anagrams or a trickle.
# DICT =   "data/ngsl.csv"           # Pretty good for more common words
# DICT = "data/wordlist.10000.txt"   # Lousy --- lots of abbreviations
# DICT = "data/1-1000.txt"           # Limited
# DICT = "data/dict.txt"               # The 40,000 word list we used for single word anagrams in CS 210
# DICT = "data/nifty-3.txt"            # From Stuart Reges' entry in Nifty Projects database
DICT = "data/cs_sample.txt"            # Tiny list for test cases
```

We can start our `anagram.py` module with a function that
simply constructs a list of words from the selected word list.

```python
"""Find anagrams (potentially multi-word) for a word or phrase."""

import config
import io

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def read_word_list(f: io.TextIOBase) -> list[str]:
    """Reads list of words, exactly as-is except
    for stripping off leading and trailing whitespace
    including newlines.
    """
    # You fill this in
```

Note that the argument to `read_word_list` is an open file,
not the name of a file or a file path.  The usual way of
calling `read_word_list` would be

```python
with open(path, "r") as f: 
     words = read_word_list(f)
```

We choose to do it this way because our command line interface,
which we will introduce shortly, will open the file for us
or provide an error message. 

We will not bother to normalize words in the word list,
leaving that to our `LetterBag` module, but we will
use the `strip()` method to remove leading and trailing
white space including the newline at the end of each
line of text. 

Although the `read_word_list` function is simple, it is a good
idea to get started with our `test_anagram` module in `test_anagram.py`.

```python
"""Test cases for anagram.py"""

import unittest
import anagram
from letter_bag import LetterBag


class Test_Read(unittest.TestCase):
    """Test reading and sorting the word list"""

    def test_read(self):
        """Just reading the word list"""
        with open("data/cs_sample.txt") as f:
            words = anagram.read_word_list(f)
        expect = ["transform", "mop", "income", "secret",
                  "cup", "use", "eccentric"]
        self.assertListEqual(words, expect)

        
if __name__ == "__main__":
    unittest.main()
```

### Anagram search algorithm

Take a deep breath, because it's time to write the search
function at the very heart of the anagram finder.  The header
of this function will be 

```python
def search(letters: LetterBag,
           candidates: list[LetterBag],
           limit: int=500,
           seed: str="") -> list[str]:
    """Returns a list of anagrams for letters, where
     each anagram is constructed from entries in the
     candidates list.
     """
```

The `limit` and `seed` arguments of search are _keyword arguments_ with
default values, so we can omit them when we call
the `search` function if the defaults are acceptable. 

Note that the `candidates` argument for `search` is a
list of `LetterBag` objects, rather than a list of strings. 
Also we made the `take` method in class `LetterBag` operate
on a pair of `LetterBags` (`self` and `other`) rather than
a `LetterBag` and a `str`.  
Because this recursive search may
consider the same word many times, in different
combinations with others, it is worthwhile to
convert the whole word list to `LetterBag` objects just
once before searching.  


Once we've got the basic algorithm working, we will find that
our biggest problem is often producing _too many_ boring combinations of
short words.  
We'll use the `seed` argument in a refinement
shortly, and use `limit` to prevent it from spewing thousands
and thousands of anagrams.  But first, we need to make
the basic algorithm work.

To test our algorithm before we have put various spew-limiting
measures in place, we will initially test with a tiny
list of candidate words.  In `data/cs_sample.txt` we find this
tiny word list: 

```text
transform
mop
income
secret
cup
use
eccentric
```

This list was chosen to produce exactly two anagrams for "Computer Science!":
"eccentric mop use" (or "mop use eccentric") and "secret income cup"
(or "income secret cup").  The word "transform" does not appear in
either anagram.  The capitalization and punctuation in "Computer Science!"
should be ignored.

Here's a test case (in `test_anagram.py`)
that we will want our search function to pass.  

```python
class Test_Anagram_Search(unittest.TestCase):
    """Tests for the anagram search per se"""
    
    def test_search_simple(self):
        """Search should automatically ignore non-letter characters"""
        with open("data/cs_sample.txt") as f:
            words = anagram.read_word_list(f)
        candidates = [letter_bag.LetterBag(word) for word in words]
        target = letter_bag.LetterBag("Computer science!")
        anagrams = anagram.search(target, candidates)
        self.assertListEqual(anagrams, ["mop use eccentric", "income secret cup"])
```
Note that we have omitted the `limit` and `seed` arguments and
accepted their default values. 

As we often find with recursive algorithms, the header of the `search` function
isn't quite suitable for recursive calls.  We'll place the real recursive
function inside it: 

```python
def search(letters: LetterBag,
           candidates: list[LetterBag],
           limit: int=500,
           seed: str="") -> list[str]:
    """Returns a list of anagrams for letters, where
     each anagram is constructed from entries in the
     candidates list.
     """

    result = []

    # List of candidates, limit, and result list are visible to the
    # nexted function, and need not be passed to it.

    def _search(letters: LetterBag,  # The letters we can draw from
                pos: int,            # Position in list of word list letterbags
                phrase: list[str]    # The phrase we are building
                ):
        """Recursive function has the effect of adding phrases to result"""
        ### Your code for body of _search goes here
        
    # Initiate a single search at position 0 with an empty phrase,
    # after seeding if appropriate
    phrase = []
    _search(letters,  0, phrase)
    return result
```

Note that `search` has a _result_, but `_search` has an _effect_.  

Recall that our list `candidates` will contain the `LetterBag` representations
of "transform", "mop", "income", "secret", "cup", "use", and "eccentric".  Let's
trace through the logic of searching for all anagrams of "Computer Science!" that
can be constructed from this list.  The `LetterBag` representation of 
"Computer Science!" is passed as `letters`.  In the first call to `_search`,
`pos` is 0 and `phrase` is an empty list. 

We'll begin by considering `_search` as a recursive function.
What are the basis cases and recursives cases we need to consider?

- We might be at the end of the `candidates` list, without a complete anagram.
  This is a basis case:  We should return without adding anything to `result`.
- Otherwise we are not at the end of the `candidates` list.  Then there are two
  possibilities. 
  - One possibility is that we cannot build the current candidate using the letters
    in variable `letters`.  In other words, `letters.contains(c)` may return `False`.
    Then the only possibility is that we can complete an anagram with words in the
    rest of the list.  (This is a recursive case, but as I'll explain below, we
    will check the "don't use this word" cases with a loop instead of a recursive
    call.)
  - The other possibility is that the candidate we are looking at (the one at positon `pos`)
    can be constructed from the letters in `letters`.  Call that
    candidate `c`.  Then one case we must consider is that we do not use `c`
    even though we could.  (Again, this is a recursive case, but we're going to
    use a loop instead.)  We _also_ need to consider the case that we do use
    the candidate word.  For this case we add the string representation of the
    candidate to `phrase`.  If this candidate would use _all_ the remaining
    letters in variable `letters`, then we can add `phrase` to `result` and
    return.  Otherwise we must try to complete the anagram with the remainder
    of the candidate list.  And this time we really _do_ need to make a recursive
    call, because we cannot handle both possibilities (using the candidate and
    not using the candidate) in a loop.  

We could code this whole algorithm using only recursion, and not explicit loops.
It might even be clearer if we did.  However, there's a problem:  Each recursive
call uses some space on the _call stack_, and the size of the call stack is limited.
(Python implements this with an explicit limit on how many recursive calls can be
in progress at once.)  If we implemented the "don't use this word" cases as recursive
calls, the depth of recursion would sometimes be as great as the length of the word
list we used.  For long word lists, Python would raise a "recursion limit exceeded"
exception.  

While a recursive call for each word we _don't_ use could exceed Python limits,
we are unlikely to construct anagrams of more than five or ten words, so a recursive
call each time we consider _including_ a candidate does not present problems.  This
is why we choose to _loop_ over the candidate list (this covers the
"don't use this word" recursive cases) and make recursive calls for "do use this word".

Thus in outline your `_search` function should follow pseudocode like this: 

```text
for candidates in position `pos` .. length of candidates list: 
    if this candidate can be constructed from `letters`:
        extended phrase = phrase with word added
        if using it would leave `letters` empty (length 0): 
            add the extended phrase to `result`
        else: 
            make a recursive call to try using this word,  
              with the extended phrase, the remaining letters,
              and searching from `pos + 1`   
```
Note that we create an extended phrase, rather than appending the
word to the phrase that was passed as an argument.  This again is to
avoid side effects through aliasing:  We don't want to change the
phrase that was passed as an argument!  We can use the same tactic we
used in the `take` method of `LetterBag`, making a copy of `phrase`
and appending to the copy. 


In my sample solution, this pseudocode expands to about
12 lines of Python code (excluding logging statements I 
added for debugging). 
I convert the list of `str` values into a single `str`
using the `join` method.  Before the loop, I include a couple
lines to implement the limit on number of anagrams we will produce: 

```python
        if len(result) >= limit:
            return
```

Remember that `LetterBag.contains` and `LetterBag.take` are methods that
return results.  We went to some trouble to avoid side effects
in `LetterBag.take`, which returns a new `LetterBag` object.
You will need this to make the recursive call work
without messing up the next iteration of the loop! 

Use the test case above `test_search_simple` to check your work on `_search`.
It is very important that this test case uses the tiny example word list
`cs_sample.txt`, with predictable results.  It would be nearly impossible to
debug problems with a large word list, especially if we didn't know precisely
what list of anagrams we should expect (but even if we did). 

The behavior we expect when searching for anagrams of `Computer Science!`
with that tiny word list is: 
  - The  representation of the `LetterBag` for `Computer Science!` should contain
    the following counts of letters: 
    `[c:3, o:1, m:1, p:1, u:1, t:1, e:3, r:1, s:1, i:1, n:1]`.
  - The first candidate word, `transform`, cannot be constructed from this
    bag of letters.  Our first iteration through the `_search` loop should
    check it, then go on without doing anything else. 
  - The second candidate word, `mop`, can be built from this letter bag. Here
    we must make a recursive call to consider anagrams that include the word `mop`.
    The recursive call will start with a letter bag that still contains 
    `[c:3, u:1, t:1, e:3, r:1, s:1, i:1, n:1]`
    The recursive call
    should start at position 2 (the position of "income"), because we don't
    want to consider the same word twice.  In the recursive call: 
      - The word "income" cannot be built from the remaining letters, because
        the "o" and "m" have been used up.  We continue past this word. 
      - The word "secret" can be made form the remaining letters.  We will
        start another recursive call with the remaining letters, starting from
        candidate word "cup".  After taking the letters from "mop" and "secret",
        none of the remaining words can be built, so recursive call will return
        after looping through the remaining candidates without adding any new
        words to the phrase. 
      - After returning from the unsuccessful attempt to build an anagram
        containing both "mop" and "secret", we are back to trying to build
        other anagrams with just "mop", beginning with "cup". 
      - The word "cup" cannot be made, because we've used the only letter "p". 
      - The word "use" can be made.  This triggers another recursive call, this
        time starting with candidate word "eccentric" and the remaining letters
        `[c:3, t:1, e:2, r:1, i:1, n:1]`.  
      - The word "eccentric" can be made from `[c:3, t:1, e:2, r:1, i:1, n:1]`,
        and it uses up all of those letters, so we successfully add
        anagram "mop use eccentric" in `result`, and return to look for more. 

You can see why we wanted to use a small example for testing!  In debugging my own
sample solution, I had to trace through several loop iterations with and without
recursive calls to find the "this can't happen!" moment.  It would have been impossible
to find that bug with a large example.  (It was a bug in calculating the length
of a `LetterBag`;  I was mistakenly counting punctuation that was present before
normalization.)

## Breathe out

There is more code to write, but if you have gotten this far successfully, you are
over the hard part.  Everything else is refinement to make the application more
usable.  I'll provide quite a bit of it, but leave a bit to you. 

## Making it an application

So far we have a search _function_, but we don't really have a search _program_
yet.  We need at least to obtain a word or phrase from the user, search for
anagrams, and print the results.  We'll write this as a _command line_ application
that can be run with a command like this (depending on your operating system):

```shell
python3 anagram.py 'Computer Science!'
``` 

We can use a module called `argparse` to parse this command line
and return its parts to our main program. 

```python
import argparse
```

To save a few steps, I'll provide a function that does the command line
processing not only to read the phrase but to additionally parse some
options that we haven't implemented yet.  Don't worry about understanding
every line of this code ... it's mostly boilerplate following recipes in
the Python library documentation.  Suffice it to say that each call to
`ArgumentParser.add_argument` defines one thing you _could_ specify on the
command line, but only the phrase we will find anagrams for is required.

```python
def cli() -> argparse.Namespace:
    """Command line interface"""
    parser = argparse.ArgumentParser("Search for multi-word anagrams")
    parser.add_argument("phrase", type=str)
    parser.add_argument("--words",
                        action='store_true',
                        help="List of words that could appear in a multi-word anagram")
    parser.add_argument("--seed", type=str, default="",
                        help="Just anagrams that include this seed word or phrase",
                        nargs="?")
    parser.add_argument("--cover",
                        action='store_true',
                        help="Just anagrams with at least one distinct word")
    parser.add_argument("--disjoint",
                        action='store_true',
                        help="Just anagrams that have no words in common")
    parser.add_argument("--limit", type=int, default=1000,
                        help="Stop after discovering this many anagrams (before filtering)",
                        nargs="?")
    args = parser.parse_args()
    return args
```

The most straightforward version of your main program (ignoring the many optional
arguments) would look like this: 

```python
def main():
    """Search for multi-word anagrams."""
    args = cli()  
    bag = LetterBag(args.phrase)
    words = read_word_list(open(config.DICT, "r"))
    candidates = [LetterBag(word) for word in words]
    anagrams = search(bag, candidates, limit=args.limit)
    print(anagrams)


if __name__ == "__main__":
    main()
```

I suggest you try a few words and phrases, varying the word list selection
in `config.py`, to get a feel for how the algorithm performs.   Do you find
that any interesting or fun anagrams are buried in a vast pile of boring
combinations, especially of short words, except when it cannot find many (sometimes any)
anagrams?  The remainder of this project is a set of small refinements that
make it a little easier (still not easy) to pick the few good ones out of the pile.

### Denser display

The long list of anagrams is a little easier to read if we place more than
one anagram on each line of the output.  I have provided a little module
`columns.py` for doing that.  You can import it into `anagrams.py` and improve the
display a bit by replacing `print(anagrams)` with the following: 

```python
    columnized = columns.columns(anagrams, col_width=len(args.phrase)+5)
    print(columnized)
```

### Stop list

Some of the word lists contain many very short words (or supposed words) that are
very unlikely to be part of an interesting anagram.  
This is especially a problem with the list `data/wordlist.10000.txt`. 
For example, some of the word lists
include an entry for each letter of the alphabet.  I am not interested in anagrams that
use the letter "t" as a word.  I am especially not interested in learning that "cat food" can
be rearranged to form the anagram "f do o c at".  

A common tactic in similar applications, and especially in applications that "scrape"
data from available sources like web sites, is to employ a "stop list" of text that
should be excluded.  One such stop list is included in `config.py`.  My sample
solution uses it in the `read_word_list` function, adding a word to the list
it returns only if it is not in the stop list.  This is a simple addition: 

```python
        if word in config.STOP_LIST:
            continue
```

### Better words first

If my list of anagrams will contain many short, boring words, I'd like longer
and more interesting words to at least appear earlier in the list.  Also, matching
longer words and words with less common letters first might speed up the search,
because they eliminate more of the words that can be matched later.  For both of
those reasons, I might prefer the word lists to be in an order that is not alphabetical.
I do not have a good objective way of measuring "interestingness", but the scoring
function from the game _Scrabble_ is a pretty good combination of length and
infrequency.  We can use _Scrabble_ scoring as a key for sorting the word list.

I have provided `word_heuristic.py` with a _Scrabble_-based function `score`.
You can use it in the `main` function of your anagram application by sorting
the list of words just before you convert them to `LetterBag` objects.  You'll
need to import `word_heuristic`, then add 

```python
words.sort(key=word_heuristic.score,reverse=True)
```

With the stop list and sorting, you should be able to pass this additional
test case, which can be added to class `Test_Anagram_Search` in
source file `test_anagram.py`.  (Add the appropriate `import` statement
there, too.)

```python
        def test_search_sorted(self):
        """Without constraints on the search"""
        with open("data/cs_sample.txt") as f:
            words = anagram.read_word_list(f)
        words.sort(key=word_heuristic.score, reverse=True)
        candidates = [LetterBag(word) for word in words]
        target = LetterBag("computer science")
        anagrams = anagram.search(target, candidates)
        self.assertListEqual(anagrams, ["eccentric mop use", "income secret cup"])
```


### Filtering the input

We can make the program faster, although no less verbose,
by eliminating words that cannot possibly be part of anagrams for
an input phrase just once, rather than over and over as we search.
This can be done in a single line after we have converted the
(sorted) word list into a list of `LetterBag` objects: 

```python
candidates = [cand for cand in candidates if bag.contains(cand)]
```

Is the speed difference notable?  It's more likely to be significant when
you are using long word lists, like `data/dict.txt`.

### Filtering the output

With these changes, it is still too hard to find a good anagram in the
flood of bad anagrams.  The provided `filters.py` module can help your search. 
The idea is that you can run the application once with the `--words`
command-line option to find just interesting
words that appear in at least one anagram, then run it again with the
`--seed` argument to generate only anagrams that include a word you have
identified as potentially interesting.  Our `main` function will now make use
of those command-line options we added to the `cli` function earlier.

The way we access those command-line arguments is idiosyncratic, because
`argparse` is an old library module from before type annotations became
commonplace.  Since it is odd, I will just provide the revised code for `main` with
the option processing and filtering in place: 

```python
def main():
    """Search for multi-word anagrams.
    """
    args = cli()  # Command line interface
    bag = LetterBag(args.phrase)
    words = read_word_list(open(config.DICT, "r"))
    # Preferably explore long candidate words with infrequent letters.
    words.sort(key=word_heuristic.score,reverse=True)
    candidates = [LetterBag(word) for word in words]
    # Filter words that can't be built
    candidates = [cand for cand in candidates if bag.contains(cand)]
    seed = args.seed
    anagrams = search(bag, candidates, seed=seed, limit=args.limit)
    if args.words:
        ### Only distinct words found in the anagrams
        filtered = filters.filter_unique_words(anagrams)
    elif args.disjoint:
        ### Only phrases that don't repeat any words from seen phrases
        filtered = filters.filter_only_unique(anagrams)
    elif args.cover:
        ### Only phrases that introduce at least one new word
        filtered = filters.filter_some_unique(anagrams)
    else:
        filtered = anagrams
    columnized = columns.columns(filtered, col_width=len(args.phrase)+5)
    print(columnized)
```

### What's missing? 

We are almost there, but we have not yet implemented the `seed` argument to
our `search` function.  If we use the `ngsl` word list and run 

```shell
 python3 anagram.py --words 'Computer Science!'
```

we can find the following list of words that appear in at least
one anagram: 

```text
computer              science               concept               crime
use                   concert               piece                 sum
cup                   seem                  i                     income
secret                scene                 to                    once
set                   music                 center                cope
recent                occur                 stem                  ice
pen                   come                  screen                it
in                    cent                  rise                  nice
rest                  since                 cut                   per
rice                  crop                  some                  core
cost                  mere
```

We might decide we'd like to see anagrams that include the word "crime", but so far
our `search` function is not doing anything when we pass "crime" as the `seed`
argument.  It's time to fix that. 

Recall that our `main` function calls `search`, which in turn calls the
recursive function `_search`.  One of the arguments to `_search` is `letters`, 
a `LetterBag` for the input word or phrase.  Another argument, which 
so far we have always initialized with an empty list, is `phrase`, 
a list of the words that have been found and added to the potential anagram
so far.  It is fairly easy in function `search` to simulate having already
found (and taken from `letters`) some text that is added to `phrase` before
the real search begins.  If a non-empty string is passed as the `seed` argument
to `search`, it can: 

- Add (append) the `seed` argument to the initial phrase
- Convert the `seed` argument to a `LetterBag`.
- Take that `LetterBag` from `letters` before calling `_search` with
  `letters` and `phrase`. 

After you have added code to do that, you should be able to generate only
anagrams of "Computer Science" that contain the word "crime".

```shell
python3 anagram.py --seed crime "Computer Science"
```

This should yield output (again, using the ngsl word list) like this: 

```text
crime concept use    crime cup scene to   crime cup once set
```
So, we see that "computer science" can be rearranged to form "use crime concept",
which might be appropriate if you major in computer science and
select the cybersecurity track. 

## Done! 

That's it.  We will primarily test and review your `search` function and your
`LetterBag` class.  We might look at other code you submit, but primarily
we will be looking at those two units. 

