import vcf


def main():
    # Set up two file readers:
    # One for the ClinVar file, one for the genome data.
    # For now you can just use sys.argv[1], implement
    # flags later.
    clinvar = "/home/emilysa/ChurchLab/clinvar-latest.vcf"
    genome = "/home/emilysa/ChurchLab/hu4040B8.vcf"
    clinFile = vcf.Reader(open(clinvar, "r"))
    genomeFile = vcf.Reader(open(genome, "r"))
    # Create a loop where, each step, the file with
    # the earliest line "steps forward".
    clinRecord = clinFile.next()
    genomeRecord = genomeFile.next()
    for genomeRecord in genomeFile:

        #Check to see if chromosome match
        if clinRecord.CHROM == genomeRecord.CHROM:
            #If they do, check to see if positions match
            if clinRecord.POS > genomeRecord.POS:
                #if the ClinVar position is greater, advance the genome's file
                genomeRecord = genomeFile.next()
            elif clinRecord.POS < genomeRecord.POS:
                #if the genome's position is greater, advance the ClinVar file
                clinRecord = clinFile.next()
            else:
                #Perfect matches
                if clinRecord == genomeRecord:
                    print "Perfect Match!"
                    print "Match Record:",
                    print genomeRecord
                    print "Clin Record:",
                    print clinRecord
                    print "\n"
                    genomeRecord = genomeFile.next()
                    clinRecord = clinFile.next()
                else:
                    #Edge Cases and how we're handling them
                    #If ALT = <CGA_CNVWIN>, filter this out
                    if str(genomeRecord.ALT) == "[<CGA_CNVWIN>]":
                        genomeRecord = genomeFile.next()
                        clinRecord = clinFile.next()
                    #If there are multiple ACC#
                    elif genomeRecord.REF == clinRecord.REF:
                        print "Multiple Paths"
                        print "Match Record:",
                        print genomeRecord
                        print "Clin Record:",
                        print clinRecord
                        print "\n"
                        genomeRecord = genomeFile.next()
                        clinRecord = clinFile.next()
                    #If REF has different length
                    else:
                        #If REF has different length, but are longer segments, include in results
                        if (len(str(genomeRecord.ALT)) - len(genomeRecord.REF) == 2) and (len(str(genomeRecord.REF)) - len(str(clinRecord.REF))) == (len(str(genomeRecord.ALT)) - len(str(clinRecord.ALT))):
                            print "REF length inconsistent"
                            print "Match Record:",
                            print genomeRecord
                            print "Clin Record:",
                            print clinRecord
                            print "\n"
                            genomeRecord = genomeFile.next()
                            clinRecord = clinFile.next()
                        #Don't include if the REF has different length and represents insertion, deletion, etc
                        else:
                            genomeRecord = genomeFile.next()
                            clinRecord = clinFile.next()
        elif clinRecord.CHROM > genomeRecord.CHROM:
            #If the ClinVar chromosome is greater, advance the genome's file
            genomeRecord = genomeFile.next()
        else:
            #If the genome's chromosome is greater, advance the ClinVar file
            clinRecord = clinFile.next()
            

if __name__ == "__main__":
    main()

    
