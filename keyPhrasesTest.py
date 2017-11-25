#!/usr/bin/env python
import keyPhrases

key1 = "7e97a4dcce2a42d08978545f1a2c77bb"
key2 = "7fae8fc1feb540e4bc24bd0ea357e836"
teststring = "The LHC is a big particle accelerator that makes particles go very fast at high energies. This is useful for probing new physics regimes and understanding the universe."

importants = keyPhrases.getKeyWords(teststring,access_key="7e97a4dcce2a42d08978545f1a2c77bb")
print " > Test string:"
print teststring
print " > Important keywords:"
print importants
