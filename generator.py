import vcf


def main():
    # Set up two file readers:
    # One for the ClinVar file, one for the genome data.
    # For now you can just use sys.argv[1], implement
    # flags later.
    clinvar = "/home/emilysa/ChurchLab/clinvar-latest.vcf"
    genome = "/home/emilysa/ChurchLab/hu4040B8.vcf"
    clin_file = vcf.Reader(open(clinvar, "r"))
    genome_file = vcf.Reader(open(genome, "r"))
    # Create a loop where, each step, the file with
    # the earliest line "steps forward".
    clin_record = clin_file.next()
    genome_record = genome_file.next()
    for genome_record in genome_file:

        #Check to see if chromosome match
        if clin_record.CHROM == genome_record.CHROM:
            #If they do, check to see if positions match
            if clin_record.POS > genome_record.POS:
                #if the ClinVar position is greater, advance the genome's file
                genome_record = genome_file.next()
            elif clin_record.POS < genome_record.POS:
                #if the genome's position is greater, advance the ClinVar file
                clin_record = clin_file.next()
            else:
                #Perfect matches
                if clin_record == genome_record:
                    print "Perfect Match!"
                    print "Match Record:",
                    print genome_record
                    print "Clin Record:",
                    print clin_record
                    print "\n"
                    genome_record = genome_file.next()
                    clin_record = clin_file.next()
                else:
                    #Edge Cases and how we're handling them
                    #If ALT = <CGA_CNVWIN>, filter this out
                    if str(genome_record.ALT) == "[<CGA_CNVWIN>]":
                        genome_record = genome_file.next()
                        clin_record = clin_file.next()
                    #If there are multiple ACC#
                    elif genome_record.REF == clin_record.REF:
                        print "Multiple Paths"
                        print "Match Record:",
                        print genome_record
                        print "Clin Record:",
                        print clin_record
                        print "\n"
                        genome_record = genome_file.next()
                        clin_record = clin_file.next()
                    #If REF has different length
                    else:
                        #If REF has different length, but are longer segments,
                        #include in results
                        if (len(str(genome_record.ALT)) - len(genome_record.REF) == 2) and (len(str(genome_record.REF)) - len(str(clin_record.REF))) == (len(str(genome_record.ALT)) - len(str(clin_record.ALT))):
                            print "REF length inconsistent"
                            print "Match Record:",
                            print genome_record
                            print "Clin Record:",
                            print clin_record
                            print "\n"
                            genome_record = genome_file.next()
                            clin_record = clin_file.next()
                        #Don't include if the REF has different length and
                            #represents insertion, deletion, etc
                        else:
                            genome_record = genome_file.next()
                            clin_record = clin_file.next()
        elif clin_record.CHROM > genome_record.CHROM:
            #If the ClinVar chromosome is greater, advance the genome's file
            genome_record = genome_file.next()
        else:
            #If the genome's chromosome is greater, advance the ClinVar file
            clin_record = clin_file.next()
            

if __name__ == "__main__":
    main()

    
