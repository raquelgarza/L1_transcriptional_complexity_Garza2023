#!/bin/python
import truster
import os

path_parent = os.path.dirname(os.getcwd())
raw_path = ["/projects/fs5/jakobssonlab/CTG_Seq093_98_SingleNuclei/FastQFiles/", "/projects/fs5/jakobssonlab/Seq041_FetalCortex/HHKJNBGXB/outs/fastq_path/10Xscfetal/", "/projects/fs5/jakobssonlab/Seq044_FetalCortex/H3L5MBGXC/outs/fastq_path/10Xscfetal/"]
lunarc = "config_files/lunarc_config.json"
modules = "config_files/software_modules.json"

fetalcortex = truster.Experiment("fetalcortex", lunarc, modules)
fetalcortex.register_samples_from_path(raw_path)

fetalcortex.unregister_sample('Seq093_1')
fetalcortex.unregister_sample('Seq093_2')
fetalcortex.unregister_sample('Seq093_7')
fetalcortex.unregister_sample('Seq093_8')
fetalcortex.unregister_sample('Seq098_1')
fetalcortex.unregister_sample('DA112')
fetalcortex.unregister_sample('Seq095_3')

quantification_dir = "/projects/fs5/raquelgg/FetalCortex/Dec2020/1_counts/"
for sampleId in list(fetalcortex.samples.keys()):
        fetalcortex.set_quantification_outdir(sample_id = sampleId, cellranger_outdir = os.path.join(quantification_dir, sampleId))

clusters_dir = os.path.join(path_parent, "2_getClusters")
#fetalcortex.get_clusters_all_samples(clusters_dir, perc_mitochondrial = 10, normalization_method = "CLR", max_size=2000, res = 0.7, jobs=5)
fetalcortex.set_clusters_outdir(clusters_dir)

per_sample_pipeline_dir = os.path.join(path_parent, "2_getClusters/cluster_pipeline/") 
merged_dir = os.path.join(path_parent, "3_combinedUMAP_perCluster_perCellCycle") 
gene_gtf = "/projects/fs3/raquelgg/annotations/hg38/gencode/v36/gencode.v36.annotation.gtf"
te_gtf = "/projects/fs3/raquelgg/annotations/hg38/repeatmasker/hg38_rmsk_TEtranscripts.gtf"
star_index = "/projects/fs1/common/genome/lunarc/indicies/star/human/hg38/" 


#fetalcortex.merge_samples(merged_dir, "CLR", integrate_samples = True)
fetalcortex.set_merge_samples_outdir(merged_dir)

merged_pipeline_dir = os.path.join(merged_dir, "clusterPipeline")
fetalcortex.process_clusters(mode = "merged", outdir = merged_pipeline_dir, gene_gtf = gene_gtf, te_gtf = te_gtf, star_index = star_index, RAM = 48725506423, jobs=5, groups = {"merged_cluster" : ["DA094", "DA103", "DA140", "Seq095_2", "Seq098_2"]}, factor = "seurat_clusters,cellCycle") 

