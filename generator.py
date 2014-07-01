'''Generator that takes two .vcf files and displays matches'''
import re
from vcf_parsing_tools import (ClinVarEntry, ClinVarAllele, ClinVarData)

CLINVAR_FILEPATH = "clinvar-latest.vcf"
GENOME_FILEPATH = "hu4040B8.vcf"

CHROM_INDEX = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
               "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
               "11": 11, "12": 12, "13": 13, "14": 14, "15": 15,
               "16": 16, "17": 17, "18": 18, "19": 19, "20": 20,
               "21": 21, "22": 22, "X": 23, "Y": 24, "M": 25,
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

def vcf_line_pos(vcf_line):
    """
    Very lightweight processing of vcf line to enable position matching.

    Returns a dict containing:
        'chrom': index of chromosome (int), indicates sort order
        'pos': position on chromosome (int)
    """
    if not vcf_line:
        return None
    vcf_data = vcf_line.strip().split("\t")
    return_data = dict()
    return_data['chrom'] = CHROM_INDEX[vcf_data[0]]
    return_data['pos'] = int(vcf_data[1])
    return return_data

def genome_vcf_line_alleles(vcf_line):
    if not vcf_line:
        return None
    vcf_data = vcf_line.strip().split("\t")
    possible_alleles = [vcf_data[3]] + vcf_data[4].split(',')
    format_tags = vcf_data[8].split(":")
    genome_values = vcf_data[9].split(":")
    genome_data = { format_tags[i]:genome_values[i] for i in
                    range(len(genome_values)) }
    alleles = [possible_alleles[int(x)] for x in
               re.split('[|/]', genome_data['GT'])
               if x != '.']
    return alleles

def main():
    '''Takes two .vcf files and returns matches'''
    clin_file = open(CLINVAR_FILEPATH, 'r')
    genome_file = open(GENOME_FILEPATH, 'r')
    clin_curr_line = clin_file.next()
    genome_curr_line = genome_file.next()

    # Ignores all the lines that start with a hashtag
    while clin_curr_line.startswith("#"):
        clin_curr_line = clin_file.next()
    while genome_curr_line.startswith("#"):
        genome_curr_line = genome_file.next()

    # Advance through both files simultaneously to find matches
    while clin_curr_line or genome_curr_line:

        clin_curr_pos = vcf_line_pos(clin_curr_line)
        genome_curr_pos = vcf_line_pos(genome_curr_line)

        if clin_curr_pos['chrom'] > genome_curr_pos['chrom']:
            # If the ClinVar chromosome is greater, advance the genome's file
            genome_curr_line = genome_file.next()

        elif clin_curr_pos['chrom'] < genome_curr_pos['chrom']:
            # If the genome's chromosome is greater, advance the ClinVar file
            clin_curr_line = clin_file.next()

        if clin_curr_pos['chrom'] == genome_curr_pos['chrom']:

            if clin_curr_pos['pos'] > genome_curr_pos['pos']:
                # If the ClinVar position is greater, advance the genome's file
                genome_curr_line = genome_file.next()

            elif clin_curr_pos['pos'] < genome_curr_pos['pos']:
                # If the genome's position is greater, advance the ClinVar file
                clin_curr_line = clin_file.next()

            # Start positions match, look for allele matching.
            else:
                # Figure out what alleles the genome has
                genome_alleles = genome_vcf_line_alleles(genome_curr_line)

                # Because ClinVar records can match ref allele, include
                # checks for both ref and alt alleles in both records.
                clinvar_data = ClinVarData(clin_curr_line)

                for genome_allele in genome_alleles:
                    # Using index so we can call up relevant ClinVarEntries
                    for i in range(len(clinvar_data.alleles)):
                        is_same_len_change = (
                            len(genome_allele) - len(genome_alleles[0]) ==
                             len(clinvar_data.alleles[i][0]) -
                             len(clinvar_data.alleles[0][0]))
                        is_match = (is_same_len_change and
                            (genome_allele.startswith(
                                clinvar_data.alleles[i][0])) or
                            (clinvar_data.alleles[i][0].startswith(
                                genome_allele)))
                        if is_match:
                            clinvar_data.alleles[i][1] += 1

                for i in range(len(clinvar_data.alleles)):
                    zygosity = "???"
                    if (clinvar_data.alleles[i][1] and
                        clinvar_data.alleles[i][2]):
                        if len(genome_alleles) == 2:
                            if clinvar_data.alleles[i][1] == 1:
                                zygosity = "Het"
                            elif clinvar_data.alleles[i][1] == 2:
                                zygosity = "Hom"
                        elif len(genome_alleles) == 1:
                            if clinvar_data.alleles[i][1] == 1:
                                # Hemizygous, e.g. X chrom when XY.
                                zygosity = "Hem"
                        print '\t'.join([zygosity,
                                         str(clinvar_data.alleles[i][2])])

                # Known bug: A couple ClinVar entries are swapped
                # relative to the genome: what the genome calls
                # reference, ClinVar calls alternate (and visa versa).
                # Currently these rare situations result in a non-match.

                genome_curr_line = genome_file.next()
                clin_curr_line = clin_file.next()


if __name__ == "__main__":
    main()
