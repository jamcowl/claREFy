#! /usr/bin/env python
import urllib2, ntpath, re
import sys

journal_database = {
                        
                    'Accounts of Chemical Research' : ['Acc.Chem.Res'],
                    'ACS Nano' : ['ACSNano'],
                    'Annual Review of Biophysics and Biomolecular Structure' : ['Annu.Rev.Biophys.Biomol.Struct.'],
                    'Angewandte Chemie' : [ 'Angew.Chem.Int.Edit.'],
                    'ArXiV' : ['arXiv'],
                    'Biophysical Journal' : ['Biophys.J.'],
                    'Biopolymers' : ['Biopolymers'],
                    'Faraday Discussions' : ['FaradayDiscuss'],
                    'Interdisciplinary Reviews: Computational Molecular Science' : ['Interdisc.Rev.Comput.Mol.Sc.'],
                    'Journal of Chemical Theory and Computation': ['J.Chem.TheoryComput.'],
                    'Journal of Molecular Biology' : ['J.Mol.Biol.'],
                    'Journal of the American Chemical Society' : ['J.Am.Chem.Soc.'],
                    'Journal of Computational Chemistry' : ['J.Comput.Chem.'],
                    'Journal of Physical Chemistry' : ['J.Phys.Chem.'],
                    'Journal of Physics: Condensed Matter' : ['J.Phys.:Condens.Matter','JournalofPhysics:CondensedMatter'],
                    'The Journal of Chemical Physics' : ['J.Chem.Phys.'],
                    'Langmuir' : ['Langmuir'],
                    'Methods' : ['Methods'],
                    'Nano Letters' : ['NanoLett.'],
                    'Natural Computing' : ['NaturalComputing'],
                    'Nature' : ['Nature'],
                    'Nature Communications' : ['Nat.Comm.'],
                    'Nature Nano' : ['Nat.Nano'],
                    'Nucleic Acids Research' : ['NucleicAcidRes','NucleicAcidsRes.'],
                    'Physical Chemistry and Chemical Physics': ['Phys.Chem.Chem.Phys.'],
                    'Physical Review Letters' : ['Phys.Rev.Lett.'],
                    'Polymers' : ['Polymers'],
                    'Proceedings of the national academy of sciences' : ['Proc.Nat.Acad.Sci.','Proc.Natl.Acad.Sci.USA'],
                    'Science' : ['Science'],
                    'Scientific Reports' : ['Sci.Rep'],
                    'Soft Matter' : ['SoftMatter'],
                    'WIREs Computational Molecular Science ' : ['WIREsComput.Mol.Sci']}
class Ref:
    '''
    A reference, with the journal (plus pages/volumes etc.), authors, year.
    '''
    def __init__(self, i_string):
        self.string = str(i_string)
        inner_string = str(self.string)
        year = re.search('\(.*(\d\d\d\d)\).', inner_string)
        if year:
            self.year = year.group(1)
        else:
            print "Warning: don't know the year in string",inner_string
        inner_string = re.sub('\('+self.year+'\)\.','', inner_string)
        self.journal = Ref.get_journal(inner_string)
        self.set_authors_ids(inner_string)
    @staticmethod
    def get_journal(inner_string):
        for j in journal_database:
            for jj in journal_database[j]:
                if jj in inner_string.replace(' ',''):
                    return j
        print "Warning: don't know the journal in string",inner_string
        return None
    def set_authors_ids(self,inner_string):
        self.ids = []
        inner_string = inner_string.replace(r'\ufb00','ff')
        authors = str(inner_string)
        if 'and' in authors:
#            print 'starting with',authors
            authors = [a.strip() for a in inner_string.split('and')]
#            print 'now have',authors
            other_things = [a.strip() for a in authors[-1].split(',')[1:]]
            authors = [a.strip() for a in authors[0].split(',')] + [authors[-1].split(',')[0].strip()]
            if '' in authors: authors.remove('')
#            print 'and finally',authors
        else:
            other_things = inner_string.split(',')
            other_things = [ b.strip() for b in other_things]
            authors = [other_things.pop(0)]
        for b in other_things:
            if b.isdigit(): self.ids += [b]
        self.authors = authors
#        print authors





def get_pdf_from_url(url):
    download_file( url)

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open(ntpath.basename(download_url), 'wb')
    file.write(response.read())
    file.close()
    if verbose: print "pdf downloaded"

def extract_references(paper_txt):
    '''
    Extract the references from the paper text file.
    '''
    in_bib = False
    curr_ref_id = 1
    refs = {}
    i = -1
    with open(paper_txt, 'r') as f:
        for line in f.readlines():
            if 'REFERENCES' in line: in_bib = True
            elif not in_bib: continue
            if 'Appendix' in line: break
            m = re.search('^(\d+)[A-Z]\. ',line)
            if m:
                #if i >= 0: print i,refs[i]
                if i >= 0: refs[i] = Ref(refs[i])
                i = int(m.group(1))
                if i in refs.keys():
                    print 'conflict between line',line,' and previous entry',refs[i]
                else: refs[i] = re.sub('^'+str(i),'',line.rstrip())
            elif refs != {}:
                refs[i] += line.rstrip()

    return refs
                




'''
Citation project - given a pdf, look up the references and provide:
    1) link
    2) citations
    3) points at which it's cited
'''

if __name__ == '__main__':
    paper_id = '1504.00821'
    paper_pdf = paper_id+'.pdf'
    paper_txt = paper_id+'.txt'
    # fetch paper from the arxiv
    #get_pdf_from_url('https://arxiv.org/pdf/'+ paper_pdf)
    # extract the text
    # pdfx paper_pdf -t > paper_txt
    # extract the references
    refs = extract_references(paper_txt)
    for i in range(1,10):
        print refs[i].authors, refs[i].ids, refs[i].string
    
    

    # for each reference, look it up on google scholar to get the citation
    # find where it's cited
    # pretty print it


