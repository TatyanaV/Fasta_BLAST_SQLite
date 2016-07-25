#! /usr/bin/python

import argparse
import sqlite3
import sys
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
E_VALUE_THRESH = 0.04

'''******************************************************************************
 *  Function to parse command line arguments
 *  Parameters: none
 *  Returns command line arguments: fastafile and name of the database
*   https://docs.python.org/2/howto/argparse.html
 ******************************************************************************/'''
def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('fastafile', help="Fasta file")
    parser.add_argument('database', help="SQLite database.")
    command_line_arguments = parser.parse_args()
    return command_line_arguments

'''******************************************************************************
 *  Function that connect to the sqlite database and creates table to store blast results
 *  Parameters: name of the database
 *  http://pythoncentral.io/introduction-to-sqlite-in-python/
 *  https://github.com/krissu2173/histomap/blob/36de73f508699d03d4f176c06eae5370c6a72c63/cgi-bin-files/histomap/deleteAttachment.py
 ******************************************************************************/'''
def connectToDatabase(database):
    con = None
    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("""
CREATE TABLE IF NOT EXISTS BlastFastaResults(
    id  INTEGER PRIMARY KEY AUTOINCREMENT
    ,sequence TEXT
    ,hsp_align_length INTEGER
    ,score REAL
    ,e_value REAL
    ,identities INTEGER
    ,query_id TEXT
    ,precent_id2 REAL
)
""")
        con.commit()
    except sqlite3.Error,  e:
        print "Sqlite error:", e
        sys.exit(1)
        
    return con

'''******************************************************************************
 *  Function that take a file handle, format name, and returns a SeqRecord iterator
 *  Parameters: fasta file
 *  http://biopython.org/wiki/SeqIO
 * https://github.com/aungthurhahein/biotech_script/blob/226726a5c21ef0a062176e3ea498895baeddf855/py_scripts/trinotate_stepC/get_fastaby_id.py
 ******************************************************************************/'''
def readFastaFile(fastafile):
    try:
        records = SeqIO.parse(open(fastafile),  format="fasta")
    except StandardError, e:
        print "There was a problem with fasta:", e
        exit(1)
    return records

 
'''******************************************************************************
 *  Function that takes blast records, takes 2 alignment for each record
 *  if 2 alignment exist, makes sure that the e-value is above E_VALUE_THRESH
 * and that % id is > 95 and inserts parameters of interest in the sqlite database
 *  Parameters: blast record, query record from the fasta file and con for the database
 ******************************************************************************/''' 
def addBlastResultsSQLite(blast_record,query_record, con):
    for i, alignment in enumerate(blast_record.alignments):
        if i == 2: break
        for hsp in alignment.hsps:
             if ((hsp.expect < E_VALUE_THRESH) and ((hsp.identities/hsp.align_length*100) > 95)):
                data = {}
                data['sequence'] = alignment.title
                data['hsp_align_length'] = hsp.align_length
                data['score'] = hsp.score
                data['e_value'] = hsp.expect
                data['identities'] = hsp.identities
                data['query_id'] = query_record.id
                data['precent_id2'] = hsp.identities/hsp.align_length*100
                try:
                    cur = con.cursor()
                    cur.execute("""
                INSERT INTO BlastFastaResults
                (sequence, hsp_align_length, score, e_value, identities ,query_id, precent_id2 )
                VALUES (:sequence,:hsp_align_length,:score,:e_value,:identities,:query_id,:precent_id2)
                """, data)

                    con.commit()
                except sqlite3.Error,  e:
                    print "Sqlite Error:", e
                    sys.exit(1)


'''******************************************************************************
 *  Function that displays ALL data from the database
 *  Results from the previously run queries and current queries are displayed
 *  Parameters: con to the database
 *  http://www.tutorialspoint.com/sqlite/sqlite_python.htm
 *  http://pythoncentral.io/introduction-to-sqlite-in-python/
 ******************************************************************************/'''

def displayResults(con):
   cursor = con.execute("SELECT* from BlastFastaResults")
   print " SQLite ID ","sequence: ","hsp_align_length: ","score: ","e_value: ","identities: ","query_id","precent_id2: " 
   for row in cursor:
      print('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

'''******************************************************************************
 *  MAIN function that runs the above mentioned functions
 *  see comments in the main function below for more details
 ******************************************************************************/'''
def main():
    #get command line arguments
    command_line_arguments = getArguments()    
    #get a name of the sqlite database from the command line 
    #connect to the database and create a table for storying information if such does not exists
    con = connectToDatabase(command_line_arguments.database)
    #take a file handle, format name, and returns a SeqRecord iterator
    query_records = readFastaFile(command_line_arguments.fastafile) 
    #for each sequence in the fasta file
    for query_record in query_records:
        #do a blast query
        result_handle = NCBIWWW.qblast("blastn",  "nr",  query_record.format("fasta"))   
        blast_records = NCBIXML.parse(result_handle)
        #parse results of the blast query and add those results in the database
        for blast_record in blast_records:
            data = addBlastResultsSQLite(blast_record, query_record, con)
    #display results of the database
    #all results, including results that we previously added will be displayed 
    displayResults(con)        
    con.close()
    exit(0)

main()