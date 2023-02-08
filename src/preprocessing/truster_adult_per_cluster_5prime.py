#!/bin/python
import truster
import os

path_parent = os.path.dirname(os.getcwd())
raw_path = "/projects/fs5/jakobssonlab/ASAP_Project_Raw_Data_pt2/"
lunarc = "config_files/lunarc_config.json"
modules = "config_files/software_modules.json"

healthy = truster.Experiment("healthy", lunarc, modules)
print(healthy.modules)
healthy.register_sample(sample_id = "DA478", sample_name = "ASAP13-Ctl-NP16-161-PFCTX-5endseq-Seq135-4", raw_path = os.path.join(raw_path, "seq134B_135_137_139/fastq/ASAP/DA478-ASAP13-Ctl-NP16-161-PFCTX-5endseq-Seq135-4/"))
healthy.register_sample(sample_id = "DA480", sample_name = "ASAP15-Ctl-NP16-21-PFCTX-5endseq-Seq135-6", raw_path = os.path.join(raw_path, "seq134B_135_137_139/fastq/ASAP/DA480-ASAP15-Ctl-NP16-21-PFCTX-5endseq-Seq135-6/"))
healthy.register_sample(sample_id = "DA488", sample_name = "ASAP16-Ctl-PT231-PFCTX-5endseq-Seq135-8", raw_path = os.path.join(raw_path, "seq134B_135_137_139/fastq/ASAP/DA488-ASAP16-Ctl-PT231-PFCTX-5endseq-Seq135-8/"))
healthy.register_sample(sample_id = "DA428", sample_name = "ASAP13_Ctl_NP16-161_PFCTX_5prim", raw_path = "/projects/fs5/jakobssonlab/CTG_JGJSeq127_128/210907_A00681_0456_BH3KL5DMXY/H3KL5DMXY/outs/fastq_path/10X/Seq127_1/")

quantification_dir = os.path.join(path_parent, "1_counts")
cellranger_index = "/projects/fs3/jakobssonlab/premRNAREF_SingleCells/GRCh38_premRNA/" # PremRNA index since these are single nuclei samples
gene_gtf = "/projects/fs3/raquelgg/annotations/hg38/gencode/v30/gencode.v30.annotation.gtf"
te_gtf = "/projects/fs3/raquelgg/annotations/hg38/repeatmasker/hg38_rmsk_TEtranscripts.gtf"

# Nuclei was set to False since we are using a premRNA index and is redundant
healthy.quantify(cr_index = cellranger_index, outdir=quantification_dir, jobs=5, nuclei={"DA478" : False, "DA480" : False, "DA488" : False, "DA428" : False})

#for sample in list(healthy.samples.values()):
#    healthy.set_quantification_outdir(sample_id = sample.sample_id, cellranger_outdir = os.path.join(quantification_dir, sample.sample_id))

clusters_dir = os.path.join(path_parent, "2_getClusters")
healthy.get_clusters_all_samples(clusters_dir, res = 0.4, perc_mitochondrial = 10, normalization_method = "CLR", max_size=2000, jobs=5)
#healthy.set_clusters_outdir(clusters_dir)

mergedsamples_dir = os.path.join(path_parent, "3_mergeSamples/")
#healthy.set_merge_samples_outdir(mergedsamples_dir)
healthy.merge_samples(outdir = mergedsamples_dir, max_size = 1000, normalization_method = "CLR", res = 0.1)

perSamplePipeline_dir = os.path.join(path_parent, "2_getClusters/clusterPipeline/") 
star_index = "/projects/fs5/jakobssonlab/GRCh38.p13_gencode.v38_STAR/"

grouped_mergedPipeline_dir = os.path.join(mergedsamples_dir, "clusterPipeline_perSample")
healthy.process_clusters(mode = "merged", outdir = grouped_mergedPipeline_dir, gene_gtf = gene_gtf, te_gtf = te_gtf, star_index = star_index, RAM = 48725506423, jobs=5, s=2, groups = {"DA478" : ["DA478"], "DA480" : ["DA480"], "DA488" : ["DA488"], "DA428" : ["DA428"]}, tsv_to_bam = True, filter_UMIs = True, bam_to_fastq = True, concatenate_lanes = True, merge_clusters = True, map_cluster = True, TE_counts = False, normalize_TE_counts = False)






