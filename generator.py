'''Generator that takes two .vcf files and displays matches'''
CHROM_INDEX = {"1" : 1,
               "2" : 2,
               "3" : 3,
               "4" : 4,
               "5" : 5,
               "6" : 6,
               "7" : 7,
               "8" : 8,
               "9" : 9,
               "10" : 10,
               "11" : 11,
               "12" : 12,
               "13" : 13,
               "14" : 14,
               "15" : 15,
               "16" : 16,
               "17" : 17,
               "18" : 18,
               "19" : 19,
               "20" : 20,
               "21" : 21,
               "22" : 22,
               "X" : 23,
               "Y" : 24,
               "M" : 25
               }
CLNSIG_INDEX = {0 : "unknown",
                1 : "untested",
                2 : "non-pathogenic",
                3 : "probably non-pathogenic",
                4 : "probably pathogenic",
                5 : "pathogenic",
                6 : "affecting drug response",
                7 : "affecting histocompatibility",
                255 : "other"
                }
def main():
    '''Takes two .vcf files and returns matches'''
    clinvar = "clinvar-latest.vcf"
    genome = "hu4040B8.vcf"
    clin_file = open(clinvar, 'r')
    genome_file = open(genome, 'r')
    clin_record = clin_file.next()
    genome_record = genome_file.next()
    #Ignores all the lines that start with a hashtag
    while clin_record.startswith("#"):
        clin_record = clin_file.next()
    #splits the record at the tabs so information can be processed
    def clin_forward(clin_record):
        global clin_chrom
        global clin_pos
        global clin_alt
        global clin_ref
        global clin_line
        global clin_info
        clin_line = clin_record.split("\t")
        clin_chrom = CHROM_INDEX[clin_line[0]]
        clin_pos = int(clin_line[1])
        clin_ref = clin_line[3]
        clin_alt = clin_line[4]
        clin_info = clin_line[7]
    #Ignores all the lines that start with a hashtag
    while genome_record.startswith("#"):
        genome_record = genome_file.next()
    #splits the record at the tabs so information can be processed
    def genome_forward(genome_record):
        global genome_chrom
        global genome_pos
        global genome_alt
        global genome_ref
        global genome_line
        genome_line = genome_record.split("\t")
        genome_chrom = CHROM_INDEX[genome_line[0]]
        genome_pos = int(genome_line[1])
        genome_ref = genome_line[3]
        genome_alt = genome_line[4]
        genome_info = genome_line[7]
    def get_clnsig():
        global info_split
        info_split = clin_info.split(";")
        for i in info_split:
            parse_info = i.split("=")
            if parse_info[0] == "CLNSIG":
                split = parse_info[1].replace("|", ",")
                values = split.split(",")
                for i in values:
                    int_i = int(i)
                    if int_i >= 5 or int_i == 0:
                        print CLNSIG_INDEX[int_i]
                        return True
    def get_clnalle():
        global info_split
        info_split = clin_info.split(";")
        for i in info_split:
            parse_info = i.split("=")
            if parse_info[0] == "CLNALLE":
                split = parse_info[1].split(",")
                for i in split:
                    print i
                    if int(i) == 0:
                        print "REF:"
                        print clin_ref, genome_ref
                    else:
                        print "ALT:"
                        print clin_alt, genome_alt
    def print_line():
        if get_clnsig():
            print "Genome:",
            print genome_line[0], genome_pos, genome_ref, genome_alt
            print "Clinvar:",
            print clin_line[0], clin_pos, clin_ref, clin_alt
            get_clnsig()
            get_clnalle()
    '''Takes two .vcf files and returns matches'''
    #Check to see if chromosome match
    #While the clinvar file is behind the genome file's position
    #Move to the next line until the positions are equal or
    #the clinvar's position has past the genome file's position
    clin_forward(clin_record)
    genome_forward(genome_record)
    while genome_record or clin_record:
        #Check to see if chromosome match
        if clin_chrom == genome_chrom:
            #If they do, check to see if positions match
            if clin_pos > genome_pos:
                #if the ClinVar position is greater, advance the genome's file
                genome_record = genome_file.next()
                genome_forward(genome_record)
            elif clin_pos < genome_pos:
                #if the genome's position is greater, advance the ClinVar file
                clin_record = clin_file.next()
                clin_forward(clin_record)
            else:
                #Perfect matches 
                if clin_alt == genome_alt and clin_ref == genome_ref:
                    print_line()
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
                                    print_line()
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
                                    print_line()
                genome_record = genome_file.next()
                genome_forward(genome_record)
                clin_record = clin_file.next()
                clin_forward(clin_record)
        elif clin_chrom > genome_chrom:
        #If the ClinVar chromosome is greater, advance the genome's file
            genome_record = genome_file.next()
            genome_forward(genome_record)
        else:
        #If the genome's chromosome is greater, advance the ClinVar file
            clin_record = clin_file.next()
            clin_forward(clin_record)

if __name__ == "__main__":
    main()
