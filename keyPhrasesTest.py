#!/usr/bin/env python
import keyPhrases

key1 = "7e97a4dcce2a42d08978545f1a2c77bb"
key2 = "7fae8fc1feb540e4bc24bd0ea357e836"
teststring = "The LHC is a big particle accelerator that makes particles go very fast at high energies. This is useful for probing new physics regimes and understanding the universe."

#teststring = "Bioinformatics is both an umbrella term for the body of biological studies that use computer programming as part of their methodology, as well as a reference to specific analysis that are repeatedly used, particularly in the field of genomics. Common uses of bioinformatics include the identification of candidate genes and single nucleotide polymorphisms (SNPs). Often, such identification is made with the aim of better understanding the genetic basis of disease, unique adaptations, desirable properties (esp. in agricultural species), or differences between populations. In a less formal way, bioinformatics also tries to understand the organisational principles within nucleic acid and protein sequences, called proteomics."

importants = keyPhrases.getKeyWords(teststring)#,access_key="7e97a4dcce2a42d08978545f1a2c77bb")
print " > Test string:"
print teststring
print " > Important keywords:"
print importants
