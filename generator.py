#useful modules: PyVCF, vcftools, optparse, pylint, pep8


def process_header(vcf_line, build):
    return "the build of the vcf file, ie 36, 37)"

def process_info(info_str):
    return "content from the info column of vcf file, in dict form"

def process_line(vcf_line):
    return "output = [chrom, datatype, vartype," +
            "start, end, '.', '+', '.', attr_string]"

def convert(vcf_input):
    return "internal rep of input as a string or potentially an object"

def convert_to_file(vcf_input):
    return "runs convert and then saves output as a file"

def main():
    #main will contain flags -i and -o for infile and outfile, respectively.
    #Data will be read from infile and will uncompress automatically if
    #*.zip, *gz, or *.bz2
    #Report will go to outfile location
    
