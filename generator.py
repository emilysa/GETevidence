'''Generator that takes two .vcf files and displays matches'''
def main():
    '''Takes two .vcf files and returns matches'''
    clinvar = "/home/emilysa/ChurchLab/clinvar-latest.vcf"
    genome = "/home/emilysa/ChurchLab/hu4040B8.vcf"
    clin_file = open(clinvar, 'r')
    genome_file = open(genome, 'r')
    clin_record = clin_file.next()
    genome_record = genome_file.next()
    #Ignores all the lines that start with a hashtag
    while clin_record.startswith("#"):
        clin_record = clin_file.next()
    #splits the record at the tabs so information can be processed
    clin_line = clin_record.split("\t")
    clin_chrom = clin_line[0]
    clin_pos = int(clin_line[1])
    clin_ref = clin_line[3]
    clin_alt = clin_line[4]
    #Ignores all the lines that start with a hashtag
    while genome_record.startswith("#"):
        genome_record = genome_file.next()
    #splits the record at the tabs so information can be processed
    genome_line = genome_record.split("\t")
    genome_chrom = genome_line[0]
    genome_pos = int(genome_line[1])
    genome_ref = genome_line[3]
    genome_alt = genome_line[4]
    #Check to see if chromosome match
    #While the clinvar file is behind the genome file's position
    #Move to the next line until the positions are equal or
    #the clinvar's position has past the genome file's position
    while genome_record or clin_record:
        #Check to see if chromosome match
        if clin_chrom == genome_chrom:
            #If they do, check to see if positions match
            if clin_pos > genome_pos:
                #if the ClinVar position is greater, advance the genome's file
                genome_record = genome_file.next()
                genome_line = genome_record.split("\t")
                genome_chrom = genome_line[0]
                genome_pos = int(genome_line[1])
                genome_ref = genome_line[3]
                genome_alt = genome_line[4]
            elif clin_pos < genome_pos:
                #if the genome's position is greater, advance the ClinVar file
                clin_record = clin_file.next()
                clin_line = clin_record.split("\t")
                clin_chrom = clin_line[0]
                clin_pos = int(clin_line[1])
                clin_ref = clin_line[3]
                clin_alt = clin_line[4]
            else:
                #Perfect matches
                if clin_alt == genome_alt and clin_ref == genome_ref:
##                    print "Perfect Match!"
##                    print "genome:",
##                    print genome_chrom, genome_pos, genome_ref, genome_alt,
##                    print "clinvar:",
##                    print clin_chrom, clin_pos, clin_ref, clin_alt
                    None
                else:
                    #Edge Cases and how we're handling them
                    #If ALT = <CGA_CNVWIN>, filter this out
                    if str(genome_alt) == "<CGA_CNVWIN>":
                        None
                    #If there are multiple ACC#
                    elif genome_ref == clin_ref:
                        clin_alt_split = clin_alt.split(",")
                        genome_alt_split = genome_alt.split(",")
                        for i in clin_alt_split:
                            for j in genome_alt_split:
                                if i == j:
                                    print "Multiple Paths"
                                    print "genome:",
                                    print genome_chrom, genome_pos, genome_ref, genome_alt,
                                    print "clinvar:",
                                    print clin_chrom, clin_pos, clin_ref, clin_alt
                        #If REF has different length
                    else:
                    #If REF has different length, but are longer segments,
                    #include in results
                        clin_alt_split = clin_alt.split(",")
                        genome_alt_split = genome_alt.split(",")
                        for i in clin_alt_split:
                            for j in genome_alt_split:
                                if len(genome_ref) - \
                                    len(clin_ref) == \
                                    len(j) - \
                                    len(i):
                                    print "REF length inconsistent"
                                    print "genome:",
                                    print genome_chrom, genome_pos, genome_ref, genome_alt,
                                    print "clinvar:",
                                    print clin_chrom, clin_pos, clin_ref, clin_alt
                        #Don't include if the REF has different length and
                        #represents insertion, deletion, etc
                                else:
##                                    print "Not Actually a Match"
##                                    print "genome:",
##                                    print genome_chrom, genome_pos, genome_ref, genome_alt
##                                    print "clinvar:",
##                                    print clin_chrom, clin_pos, clin_ref, clin_alt
                                    None
                genome_record = genome_file.next()

                genome_line = genome_record.split("\t")
                genome_chrom = genome_line[0]
                genome_pos = int(genome_line[1])
                genome_ref = genome_line[3]
                genome_alt = genome_line[4]

                clin_record = clin_file.next()

                clin_line = clin_record.split("\t")
                clin_chrom = clin_line[0]
                clin_pos = int(clin_line[1])
                clin_ref = clin_line[3]
                clin_alt = clin_line[4]
        elif (clin_chrom == "X" and int(genome_chrom) <= 22) or \
             (clin_chrom == "Y" and genome_chrom == "X") or \
            (int(clin_chrom) > int(genome_chrom)):
        #If the ClinVar chromosome is greater, advance the genome's file
            genome_record = genome_file.next()
            genome_line = genome_record.split("\t")
            genome_chrom = genome_line[0]
            genome_pos = int(genome_line[1])
            genome_ref = genome_line[3]
            genome_alt = genome_line[4]
        else:
        #If the genome's chromosome is greater, advance the ClinVar file
            clin_record = clin_file.next()
            clin_line = clin_record.split("\t")
            clin_chrom = clin_line[0]
            clin_pos = int(clin_line[1])
            clin_ref = clin_line[3]
            clin_alt = clin_line[4]

if __name__ == "__main__":
    main()
