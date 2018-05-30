# this goes by the index file "GE_filenames.txt" and creates
#an alignment object for the appropriate filenames, runs the
#aligner, etc
import aligner
L = []
index = open("Gene_filenames.txt","r")
for line in index:
    line = line.strip()
    print("Attempting to align",line)
    TE_name = "GENE_ids/"+line
    RNA_name = "RNA_ids/"+line.split(".")[0]+".rna"
    writefile = "gene_overlaps/"+line.split(".")[0]+".out"
    try:
        A = aligner.TE_RNA_Aligner(TE_name,RNA_name,writefile)
    except FileNotFoundError:
        print("No .rna file for",line)
        L.append(line)
    A.run()
    print("Done aligning",line)
print("JOB DONE")
print("Unmatched GENE files:",L)
index.close()
