import urllib
import gzip

urllib.urlretrieve("ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar-latest.vcf.gz",
                       "gzip.gz")

f = gzip.open('gzip.gz', 'r')
vcffile = open('clinvar-latest.vcf', 'w')
file_content = f.read()
vcffile.write(file_content)
f.close()
vcffile.close()
