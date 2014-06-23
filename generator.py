'''This is the generator for searching two .vcf docs for matching info'''
import vcf
class generator():
    
    clinvar = "/home/emilysa/ChurchLab/clinvar-latest.vcf"
    genome = "/home/emilysa/ChurchLab/hu4040B8.vcf"    
    clin_file = vcf.Reader(open(clinvar, "r"))
    genome_file = vcf.Reader(open(genome, "r"))
    # Create a loop where, each step, the file with
    # the earliest line "steps forward".
    clin_record = clin_file.next()
    genome_record = genome_file.next()
    
    def display_match():
        print "Match Record:",
        print genome_record
        print "Clin Record:",
        print clin_record
        print "\n"
    
    def check_pos():
        for genome_record in genome_file:
            if clin_record.POS > genome_record.POS:
                #if the ClinVar position is greater, advance the genome's file
                genome_record = genome_file.next()
            elif clin_record.POS < genome_record.POS:
                #if the genome's position is greater, advance the ClinVar file
                clin_record = clin_file.next()
            else:
                #Perfect matches
                if clin_record == genome_record:
                    #print "Perfect Match!"
                    #display_match
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
                        display_match()
                        genome_record = genome_file.next()
                        clin_record = clin_file.next()
                    #If REF has different length
                    else:
                        #If REF has different length, but are longer segments,
                        #include in results
                        genome_alt = str(genome_record.ALT)
                        genome_ref = str(genome_record.REF)
                        clin_alt = str(clin_record.ALT)
                        clin_ref = str(clin_record.REF)
                        if (len(genome_alt) - len(genome_ref) == 2) and \
                        len(genome_ref) - len(clin_ref) == \
                        len(genome_alt) - len(clin_alt):
                            print "REF length inconsistent"
                            display_match()
                            genome_record = genome_file.next()
                            clin_record = clin_file.next()
                            #Don't include if the REF has different length and
                            #represents insertion, deletion, etc
                        else:
                            genome_record = genome_file.next()
                            clin_record = clin_file.next()
    def main():
        for genome_record in genome_file:
            #Check to see if chromosome match
            if clin_record.CHROM == genome_record.CHROM:
                check_pos()
            elif clin_record.CHROM > genome_record.CHROM:
                #If the ClinVar chromosome is greater, advance the genome's file
                genome_record = genome_file.next()
            else:
                #If the genome's chromosome is greater, advance the ClinVar file
                clin_record = clin_file.next()
                
    if __name__ == "__main__":
        main()
