#! /usr/bin/env python
import urllib2, ntpath, re

journal_database = {
                    'ACS Nano' : ['ACSNano'],
                    'Angewandte Chemie' : [ 'Angew.Chem.Int.Edit.'],
                    'Biophysical Journal' : ['Biophys.J.'],
                    'Biopolymers' : ['Biopolymers'],
                    'Nano Letters' : ['NanoLett.'],
                    'Nature' : ['Nature'],
                    'Nature Communications' : ['Nat.Comm.'],
                    'Nucleic Acids Research' : ['NucleicAcidRes'],
                    'Journal of Molecular Biology' : ['J.Mol.Biol.'],
                    'Journal of the American Chemical Society' : ['J.Am.Chem.Soc.'],
                    'Journal of Computational Chemistry' : ['J.Comput.Chem.'],
                    'Journal of Physical Chemistry' : ['J.Phys.Chem.'],
                    'Journal of Physics: Condensed Matter' : ['J.Phys.:Condens.Matter','Journal of Physics: Condensed Matter'],
                    'The Journal of Chemical Physics' : ['J.Chem.Phys.'],
                    'Physical Chemistry and Chemical Physics': ['Phys.Chem.Chem.Phys.'],
                    'Physical Review Letters' : ['Phys.Rev.Lett.'],
                    'Polymers' : ['Polymers'],
                    'Proceedings of the national academy of sciences' : ['Proc.Nat.Acad.Sci.','Proc.Natl.Acad.Sci.USA'],
                    'Science' : ['Science'],
                    'Scientific Reports' : ['Sci.Rep'],
                    'Soft Matter' : ['SoftMatter']}
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
    @staticmethod
    def get_journal(inner_string):
        for j in journal_database:
            for jj in journal_database[j]:
                if jj in inner_string.replace(' ',''):
                    return j
        print "Warning: don't know the journal in string",inner_string
        return None




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
                    sys.exit()
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
    
    

    # for each reference, look it up on google scholar to get the citation
    # find where it's cited
    # pretty print it


