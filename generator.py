'''Generator that takes two .vcf files and displays matches'''
import re
import sys

def main():
    '''Takes two .vcf files and returns matches'''
    clinvar = "/home/emilysa/ChurchLab/clinvar-latest.vcf"
    genome = "/home/emilysa/ChurchLab/hu4040B8.vcf"
    clin_file = open(clinvar, 'r')
    genome_file = open(genome, 'r')
    
    clin_record = clin_file.next()  
    genome_record = genome_file.next()

    while clin_record.startswith("#"):
        clin_record = clin_file.next()

    clin_line = clin_record.split("\t")
    clin_chrom = clin_line[0]
    clin_pos = clin_line[1]
    clin_ref = clin_line[3]
    clin_alt = clin_line[4]

    while genome_record.startswith("#"):
        genome_record = genome_file.next()
        
    genome_line = genome_record.split("\t")
    genome_chrom = genome_line[0]
    genome_pos = genome_line[1]
    genome_ref = genome_line[3]
    genome_alt = genome_line[4]
    
    #Check to see if chromosome match
    #While the clinvar file is behind the genome file's position
    #Move to the next line until the positions are equal or
    #the clinvar's position has past the genome file's position
    while genome_chrom >= clin_chrom and genome_pos >= clin_pos:
        #Condition for if position is greater
        if genome_chrom >= clin_chrom and genome_pos != clin_pos:
            clin_record = clin_file.next()
            clin_line = clin_record.split("\t")
            clin_chrom = clin_line[0]
            clin_pos = clin_line[1]
            clin_ref = clin_line[3]
            clin_alt = clin_line[4]
        #Condition if the positions match
        else:
            #Perfect matches
            if clin_record == genome_record:
                print "Perfect Match!"
                print "Match Record:"
                print genome_pos
                genome_record = genome_file.next()
                clin_record = clin_file.next()
                print genome_alt, clin_alt
                print clin_record
                print genome_record
            else:
                #Edge Cases and how we're handling them
                #If ALT = <CGA_CNVWIN>, filter this out
                if str(genome_alt) == "[<CGA_CNVWIN>]":
                    clin_record = clin_file.next()
                #If there are multiple ACC#
                elif genome_ref == clin_ref:
                    print "Multiple Paths"
                    print "Match Record:",
                    print genome_pos
                    print "\n"
                    clin_record = clin_file.next()
                    #If REF has different length
                else:
                #If REF has different length, but are longer segments,
                #include in results
                    if len(str(genome_alt)) - \
                        len(str(genome_ref)) == 2 and \
                        len(str(genome_ref)) - \
                        len(str(clin_ref)) == \
                        len(str(genome_alt)) - \
                        len(str(clin_alt)):
                        print "REF length inconsistent"
                        print "Match Record:",
                        print genome_pos
                        print "\n"
                        clin_record = clin_file.next()
                    #Don't include if the REF has different length and
                    #represents insertion, deletion, etc
                    else:
                        clin_record = clin_file.next()

    #When the genome's position is behind the clivar's position, advance
    #the genome's position until they're equal or the genome's position is
    #past the clinvar's position
    while genome_chrom <= clin_chrom and genome_pos < clin_pos:
        print genome_chrom, genome_pos,
        print clin_chrom, clin_pos
        genome_record = genome_file.next()
        genome_line = genome_record.split("\t")
        genome_chrom = genome_line[0]
        genome_pos = genome_line[1]
        genome_ref = genome_line[3]
        genome_alt = genome_line[4]
        
    print genome_record, clin_record
if __name__ == "__main__":
    main()

