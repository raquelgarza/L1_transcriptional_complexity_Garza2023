from Bio import SeqIO
hg38 = SeqIO.to_dict(SeqIO.parse("bd_adult_FL_L1HS_L1PA4_location.fa", "fasta"))
intact = {i:str(hg38[i].seq) for i in hg38 if "CAAGATGGCCG" in str(hg38[i].seq)[0:100]}
truncated = {i:str(hg38[i].seq) for i in hg38 if "CAAGATGGCCG" not in str(hg38[i].seq)[0:100]}

with open("bd_adult_FL_L1HS_L1PA4_location_intact.fa", "w")  as fout_intact, open("bd_adult_FL_L1HS_L1PA4_location_intact.bed", "w") as bedout_intact:
	for k, v in intact.items():
		fout_intact.write(f">{k}\n{v}\n")
		chr = k.split(":")[0]
		coords = k.split(":")[1]
		strand = coords.split("(")[1].strip(")")
		coords = coords.split("(")[0]
		start = coords.split("-")[0]
		end = coords.split("-")[1]
		bedout_intact.write(f"{chr}\t{start}\t{end}\t.\t.\t{strand}\n")

with open("bd_adult_FL_L1HS_L1PA4_location_truncated.fa", "w")  as fout_truncated, open("bd_adult_FL_L1HS_L1PA4_location_truncated.bed", "w") as bedout_truncated:
	for k, v in truncated.items():
		fout_truncated.write(f">{k}\n{v}\n")
		chr = k.split(":")[0]
		coords = k.split(":")[1]
		strand = coords.split("(")[1].strip(")")
		coords = coords.split("(")[0]
		start = coords.split("-")[0]
		end = coords.split("-")[1]
		bedout_truncated.write(f"{chr}\t{start}\t{end}\t.\t.\t{strand}\n")