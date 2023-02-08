#!/bin/python
import truster
import os

path_parent = os.path.dirname(os.getcwd())
raw_path = "/projects/fs5/jakobssonlab/CTG_Seq109_110/210202_A00681_0301_BHWFL5DMXX/HWFL5DMXX/outs/fastq_path/10Xsc/"
lunarc = "config_files/lunarc_config.json"
modules = "config_files/software_modules.json"

healthy = truster.Experiment("healthy", lunarc, modules)
healthy.register_sample(sample_id = "Seq109_11", sample_name = "TBI_HuBrainCTL_Nuclei501F_Hg38", raw_path = os.path.join(raw_path, "Seq109_11"))
healthy.register_sample(sample_id = "Seq109_12", sample_name = "TBI_HuBrainCTL_Nuclei501T_Hg38", raw_path = os.path.join(raw_path, "Seq109_12"))
healthy.register_sample(sample_id = "Seq109_13", sample_name = "TBI_HuBrainCTL_Nuclei529F_Hg38", raw_path = os.path.join(raw_path, "Seq109_13"))
healthy.register_sample(sample_id = "Seq109_14", sample_name = "TBI_HuBrainCTL_Nuclei529T_Hg38", raw_path = os.path.join(raw_path, "Seq109_14"))
healthy.register_sample(sample_id = "Seq109_6", sample_name = "TBI_HuBrainCTL_Nuclei502T_Hg38", raw_path = os.path.join(raw_path, "Seq109_6"))

quantification_dir = "/projects/fs5/jakobssonlab/TBIProject_ProcessedFiles/ControlFiles"
cellranger_index = "/projects/fs3/jakobssonlab/premRNAREF_SingleCells/GRCh38_premRNA/"
gene_gtf = "/projects/fs3/raquelgg/annotations/hg38/gencode/v30/gencode.v30.annotation.gtf"
te_gtf = "/projects/fs3/raquelgg/annotations/hg38/repeatmasker/hg38_rmsk_TEtranscripts.gtf"

for sample in list(healthy.samples.values()):
    healthy.set_quantification_outdir(sample_id = sample.sample_id, cellranger_outdir = os.path.join(quantification_dir, sample.sample_name))

clusters_dir = os.path.join(path_parent, "2_getClusters")
healthy.get_clusters_all_samples(clusters_dir, res = 0.7, perc_mitochondrial = 10, normalization_method = "CLR", max_size=2000, jobs=5)
#healthy.set_clusters_outdir(clusters_dir)

mergedsamples_dir = os.path.join(path_parent, "3_mergeSamples/")
healthy.merge_samples(outdir = mergedsamples_dir, max_size = 1000, normalization_method = "CLR")
#healthy.set_merge_samples_outdir(mergedsamples_dir)

perSamplePipeline_dir = os.path.join(path_parent, "2_getClusters/clusterPipeline/") 
star_index = "/projects/fs5/jakobssonlab/GRCh38.p13_gencode.v38_STAR/"

grouped_mergedPipeline_dir = os.path.join(mergedsamples_dir, "clusterPipeline_grouped")
mergedPipeline_dir = os.path.join(mergedsamples_dir, "clusterPipeline")

healthy.process_clusters(mode = "merged", outdir = mergedPipeline_dir, gene_gtf = gene_gtf, te_gtf = te_gtf, star_index = star_index, RAM = 48725506423, jobs=5, groups = {"all" : ["Seq109_11", "Seq109_12", "Seq109_13", "Seq109_14", "Seq109_6"]})
healthy.process_clusters(mode = "merged", outdir = grouped_mergedPipeline_dir, gene_gtf = gene_gtf, te_gtf = te_gtf, star_index = star_index, RAM = 48725506423, jobs=5, groups = {"Seq109_11" : ["Seq109_11"], "Seq109_12" : ["Seq109_12"], "Seq109_13" : ["Seq109_13"], "Seq109_14" : ["Seq109_14"], "Seq109_6" : ["Seq109_6"]})
#healthy.set_merge_samples_outdir(mergedsamples_dir)






