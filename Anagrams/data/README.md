# README data directory

The data directory contains word lists that can be used to form 
anagrams.  The number of anagrams that can be produced, as well as 
their quality, depends partly on the word list.

All of the word lists here, with the exception of dict.txt, suffer from
lack of affixes.  For example, the stem "arm" may be included, but not
the forms "arms" or "armed".  Affixes affect not only that particular
word, but also the other words that can complete a phrase that uses
all and only words in the anagram seed.  

## Dictionary words

`dict.txt` is the most complete word list here. Unfortunately this means
that it often produces very large lists of anagrams with lots of obscure
words that are unlikely to make good anagrams.  

## Common word lists

A short word list 
like `1-1000.txt` (1000 very common English words) tends to produce 
very few anagrams, but any it produces will consist of common words. 
`wordlist.10000.txt` contains 10,000 words, including many uncommon 
short words.  It tends to build anagrams from those uncommon 
two-letter words.   

File `ngsl.csv`, taken from a "new general 
service list" for second language learners of English, seems to strike a 
reasonable balance between comprehensiveness and quality. `ngsl.csv` is taken from the 
[New General Service List](http://www.newgeneralservicelist.org/) 
and reused under an Attribution-ShareAlike (CC BY-SA) license.  

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

## Nifty-1,2,3.txt

These word lists are adapted from Stuart Reges's 
[Anagram Solver entry](http://nifty.stanford.edu/2006/reges-anagrams/) in the Stanford "Nifty Projects" collection. 

## Test case sample
`cs_sample.txt` is a special word list used
just for test cases using "computer science"
as the phrase to be anagrammed.  It should produce
two anagrams, "secret income cup" and "eccentric mop use".


## Synthesize a word list?

Here's an idea for producing a better word list.  You could take word roots
from one of the smaller lists (say, `ngsl.csv`) and choose from `dict.txt`
all the words that _include_ any of those words (thus picking up many affixes),
or using another approach to affixing roots (so that, for example,
"study" would generate "studies" even though it lacks the "y").
Producing this hybrid word list would be a nice project in itself.  

