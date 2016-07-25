======
# Fasta_BLAST_SQLite


##Description of the Program##
Script performs a web BLAST query against nr using one or more DNA sequences read from a file in fasta-format, takes 2 alignments if 2 alignments exist for each blast record, makes sure that  e-value is above E_VALUE_THRESH  and that % id is > 95 and stores those
results in the sqlite database, queries the database and displays results of the screen of the terminal. 

<a href="http://sqlitebrowser.org/"> GUI tool for SQLite3</a>

The following infromation is entered into the SQLite batabase for 2 alignments for each blast record that meets criteria specified above after BLAST query:
+ ID of the record in the SQLite table [autoincremented]
+ alignment.title - name of the sequence
+ hsp.align_length -  Length of the alignment
+ hsp.score - score of alignment, the higher the better
+ hsp.expect
<pre><code>The Expectation value or Expect value represents the number of different alignments with scores equivalent 
to or better than S that is expected to occur in a database search by chance. The lower the E value, the more 
significant the score and the alignment.</pre></code> 
+ hsp.identities 
+ query_record - this information comes from the sequence provided in the fasta file 
+ % ID which is calculated using the following formular: hsp.identities/hsp.align_length*100

##Instruction how to run the program on the command line [Windows OS]
<pre><code>python BLAST_query_sqlite.py NAME_OF_FASTA_SEQUENCE_FILE.fasta NAME_OF_DATABASE.db</code></pre>


The following sequences are saved in the <b>sequences.fasta file</b>, so you can use that file to test the program:
<pre><code>
>NC_009085_A1S_r15 NC_009085.1 Acinetobacter baumannii ATCC 17978 chromosome, complete genome.
ATTGAACGCTGGCGGCAGGCTTAACACATGCAAGTCGAGCGGGGGAAGGTAGCTTGCTAC
TGGACCTAGCGGCGGACGGGTGAGTAATGCTTAGGAATCTGCCTATTAGTGGGGGACAAC
ATCTCGAAAGGGATGCTAATACCGCATACGTCCTACGGGAGAAAGCAGGGGATCTTCGGA
CCTTGCGCTAATAGATGAGCCTAAGTCGGATTAGCTAGTTGGTGGGGTAAAGGCCTACCA
AGGCGACGATCTGTAGCGGGTCTGAGAGGATGATCCGCCACACTGGGACTGAGACACGGC
CCAGA
>NC_003909_BCE_5738 NC_003909.8 Bacillus cereus ATCC 10987, complete genome.
GATGAACGCTGGCGGCGTGCCTAATACATGCAAGTCGAGCGAATGGATTAAGAGCTTGCT
CTTATGAAGTTAGCGGCGGACGGGTGAGTAACACGTGGGTAACCTGCCCATAAGACTGGG
ATAACTCCGGGAAACCGGGGCTAATACCGGATAACATTTTGAACCGCATGGTTCGAAATT
GAAAGGCGGCTTCGGCTGTCACTTATGGATGGACCCGCGTCGCATTAGCTAGTTGGTGAG
GTAACGGCTCACCAAGGCAACGATGCGTAGCCGACCTGAGAGGGTGATCGGCCACACTGG
GACTGAGACACGGCCCAGA
</code></pre>
##Example###
<pre><code>python BLAST_query_sqlite.py sequences.fasta blast.db</code></pre>
***THIS WILL TAKE ABOUT 5 MINUTES

Code adopted from <a href="http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc86">7.1  Running BLAST over the Internet Biopython Documentation</a>, <a href="http://pythoncentral.io/introduction-to-sqlite-in-python/">Introduction to SQLite in Python</a> and 
<a href="https://github.com/mscook/SeqFindR/blob/master/SeqFindr/blast.py"> git repository</a>

##Dependencies###
+ <a href="http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download">NCBI BLAST</a>
+ <a href="http://www.sqlite.org/download.html">SQLite3</a>
+ <a href="http://www.python.org/">python2.7</a>

##Required python modules##
+ argparse
+ <a href="http://www.tutorialspoint.com/sqlite/sqlite_installation.htm"> sqlite3</a>
+ <a href="http://www.numpy.org/">numpy</a>
+ <a href="https://docs.python.org/2/library/sys.html">sys</a>
+ <a href="http://biopython.org/">biopython</a>

## Installation instruction for Windows Users:##
###To instal argparse:
<pre><code> pip install argparse</code></pre>
*If you do not have pip, download get-pip.py and save it in the following directory: C:\Python27\Scripts.
<pre><code> python get-pip.py </code></pre>
###To install SQLite:
Follow instruction on the following website: <a href="http://www.tutorialspoint.com/sqlite/sqlite_installation.htm">SQLite3</a>
###To install numpy, scipy and biopython:
Follow this video for instalations instruction: <a href="https://www.youtube.com/watch?v=IHRQ5NBqiy8">Installing 64 bit numpy,scipy and biopython on python2.7.9(64-bit)</a>
*scipy is required only for windows user. You need numpy and scipy before you can install biopython.






