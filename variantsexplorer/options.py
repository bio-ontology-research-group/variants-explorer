FIELD_OPTIONS = {
    "SIFT" : [ 
        { "code" : "deleterious", "display": "Deleterious", "description":"Less than 0.05"},
        { "code" : "tolerated", "display": "Tolerated", "description":"Less than 0.05"}
    ],
    "PolyPhen" : [ 
        { "code" : "probably_damaging", "display": "Probably Damaging", "description":"greater than 0.908"},
        { "code" : "possibly_damaging", "display": "Possibly Damaging", "description":"greater than 0.446 and less than or equal to 0.908"},
        { "code" : "benign", "display": "Benign", "description":"less than or equal to 0.446"},
        { "code" : "unknown", "display": "Unknown", "description":"unknown"},
    ],
    "ClinSig" : [ 
        { "code" : "affects", "display": "affects", "description":""},
        { "code" : "association", "display": "association", "description":""},
        { "code" : "benign", "display": "benign", "description":""},
        { "code" : "drug", "display": "drug", "description":""},
        { "code" : "likely_benign", "display": "likely benign", "description":""},
        { "code" : "likely_pathogenic", "display": "likely pathogenic", "description":""},
        { "code" : "not_provided", "display": "not provided", "description":""},
        { "code" : "other", "display": "other", "description":""},
        { "code" : "pathogenic", "display": "pathogenic", "description":""},
        { "code" : "protective", "display": "protective", "description":""},
        { "code" : "risk_factor", "display": "risk factor", "description":""},
        { "code" : "uncertain significance", "display": "uncertain significance", "description":""}
    ],
    "Consequence" : [ 
        { "code" : "transcript_ablation", "display": "Transcript ablation", "description":"A feature ablation whereby the deleted region includes a transcript feature", "class":"SO:0001893", "ontology": "SO"},
        { "code" : "splice_acceptor_variant", "display": "Splice acceptor variant", "description":"A splice variant that changes the 2 base region at the 3' end of an intron", "class":"SO:0001574", "ontology": "SO"},
        { "code" : "splice_donor_variant", "display": "Splice donor variant", "description":"A splice variant that changes the 2 base region at the 5' end of an intron", "class":"SO:0001575", "ontology": "SO"},
        { "code" : "stop_gained", "display": "Stop gained", "description":"A sequence variant whereby at least one base of a codon is changed, resulting in a premature stop codon, leading to a shortened transcript", "class":"SO:0001587", "ontology": "SO"},
        { "code" : "frameshift_variant", "display": "Frameshift variant", "description": "A sequence variant which causes a disruption of the translational reading frame, because the number of nucleotides inserted or deleted is not a multiple of three", "class":"SO:0001589", "ontology": "SO"},
        { "code" : "stop_lost", "display": "Stop lost", "description":"A sequence variant where at least one base of the terminator codon (stop) is changed, resulting in an elongated transcript", "class":"SO:0001578", "ontology": "SO"},
        { "code" : "start_lost", "display": "Start lost", "description":"A codon variant that changes at least one base of the canonical start codon", "class":"SO:0002012", "ontology": "SO"},
        { "code" : "transcript_amplification", "display": "Transcript amplification", "description":"A feature amplification of a region containing a transcript", "class":"SO:0001889", "ontology": "SO"},
        { "code" : "inframe_insertion", "display": "Inframe insertion", "description":"An inframe non synonymous variant that inserts bases into in the coding sequence", "class":"SO:0001821", "ontology": "SO"},
        { "code" : "inframe_deletion", "display": "Inframe deletion", "description":"An inframe non synonymous variant that deletes bases from the coding sequence", "class":"SO:0001822", "ontology": "SO"},
        { "code" : "missense_variant", "display": "Missense variant", "description":"A sequence variant, that changes one or more bases, resulting in a different amino acid sequence but where the length is preserved	", "class":"SO:0001583", "ontology": "SO"},
        { "code" : "protein_altering_variant", "display": "Protein altering variant", "description":"", "class":"SO:0001818", "ontology": "SO"},
        { "code" : "splice_region_variant", "display": "Splice region variant", "description":"", "class":"SO:0001630", "ontology": "SO"},
        { "code" : "incomplete_terminal_codon_variant", "display": "Incomplete terminal codon variant", "description":"", "class":"SO:0001626", "ontology": "SO"},
        { "code" : "start_retained_variant", "display": "Start retained variant", "description":"", "class":"SO:0002019", "ontology": "SO"},
        { "code" : "stop_retained_variant", "display": "Stop retained variant", "description":"", "class":"SO:0001567", "ontology": "SO"},
        { "code" : "synonymous_variant", "display": "Synonymous variant", "description":"", "class":"SO:0001819", "ontology": "SO"},
        { "code" : "coding_sequence_variant", "display": "Coding sequence variant", "description":"SO:0001580", "class":"", "ontology": "SO"},
        { "code" : "mature_miRNA_variant", "display": "Mature miRNA variant", "description":"", "class":"SO:0001620", "ontology": "SO"},
        { "code" : "5_prime_UTR_variant", "display": "5 prime UTR variant", "description":"", "class":"SO:0001623", "ontology": "SO"},
        { "code" : "3_prime_UTR_variant", "display": "3 prime UTR variant", "description":"", "class":"SO:0001624", "ontology": "SO"},
        { "code" : "non_coding_transcript_exon_variant", "display": "Non coding transcript exon variant", "description":"", "class":"SO:0001792", "ontology": "SO"},
        { "code" : "intron_variant", "display": "Intron variant", "description":"", "class":"SO:0001627", "ontology": "SO"},
        { "code" : "NMD_transcript_variant", "display": "NMD transcript variant", "description":"", "class":"SO:0001621", "ontology": "SO"},
        { "code" : "non_coding_transcript_variant", "display": "Non coding transcript variant", "description":"", "class":"SO:0001619", "ontology": "SO"},
        { "code" : "upstream_gene_variant", "display": "Upstream gene variant", "description":"", "class":"SO:0001631", "ontology": "SO"},
        { "code" : "downstream_gene_variant", "display": "Downstream gene variant", "description":"", "class":"SO:0001632", "ontology": "SO"},
        { "code" : "TFBS_ablation", "display": "TFBS ablation", "description":"", "class":"SO:0001895", "ontology": "SO"},
        { "code" : "TFBS_amplification", "display": "TFBS amplification", "description":"", "class":"SO:0001892", "ontology": "SO"},
        { "code" : "TF_binding_site_variant", "display": "TF binding site variant", "description":"", "class":"SO:0001782", "ontology": "SO"},
        { "code" : "regulatory_region_ablation", "display": "Regulatory region ablation", "description":"", "class":"SO:0001894", "ontology": "SO"},
        { "code" : "regulatory_region_amplification", "display": "Regulatory region amplification", "description":"", "class":"SO:0001891", "ontology": "SO"},
        { "code" : "feature_elongation", "display": "Feature elongation", "description":"", "class":"SO:0001907", "ontology": "SO"},
        { "code" : "regulatory_region_variant", "display": "Regulatory region variant", "description":"", "class":"SO:0001566", "ontology": "SO"},
        { "code" : "feature_truncation", "display": "Feature truncation", "description":"", "class":"SO:0001906", "ontology": "SO"},
        { "code" : "intergenic_variant", "display": "Intergenic variant", "description":"", "class":"SO:0001628", "ontology": "SO"}
    ],
    "headers" : [
        { 
            "code": "#Uploaded_variation", 
            "display": "Uploaded Variant", 
            "description":"Identifier of uploaded variant", 
            "hide": False },
        { 
            "code": "Location", 
            "display": "Location", 
            "description":"Location of variant in standard coordinate format (chr:start or chr:start-end)", 
            "hide": False },
        { 
            "code": "Allele", 
            "display": "Allele", 
            "description":"The variant allele used to calculate the consequence", 
            "hide": False },
        { 
            "code": "Consequence", 
            "display": "Consequence", 
            "description":"Consequence type", 
            "hide": False },
        { 
            "code": "IMPACT", 
            "display": "Impact", 
            "description":"Subjective impact classification of consequence type", 
            "hide": True },
        { 
            "code": "SYMBOL", 
            "display": "Symbol", 
            "description":"Gene symbol (e.g. HGNC)", 
            "hide": False },
        { 
            "code": "Gene", "display": 
            "Gene", "description":"Stable ID of affected gene", 
            "hide": False },
        { 
            "code": "Feature", 
            "display": "Feature", 
            "description":"Stable ID of feature", 
            "hide": False },
        { 
            "code": "Feature_type", 
            "display": "Feature type", 
            "description":"Type of feature - Transcript, RegulatoryFeature or MotifFeature",
             "hide": False },
        { 
            "code": "BIOTYPE", 
            "display": "Biotype", 
            "description":"Stable ID of featureFeature	Biotype of transcript or regulatory feature",
             "hide": False },
        { 
            "code": "TSL", 
            "display": "Transcript support level", 
            "description":"Transcript support level",
            "hide": True },
        { 
            "code": "EXON", 
            "display": "Exon", 
            "description":"Exon number(s) / total",
             "hide": False },
        { 
            "code": "INTRON", 
            "display": "Intron", 
            "description":"Intron number(s) / total",
             "hide": True },
        { 
            "code": "cDNA_position", 
            "display": "cDNA position", 
            "description":"Relative position of base pair in cDNA sequence", 
            "hide": False },
        { 
            "code": "CDS_position", 
            "display": "CDS position", 
            "description":"Relative position of base pair in coding sequence", 
            "hide": False },
        { 
            "code": "Protein_position", 
            "display": "Protein position", 
            "description":"Relative position of amino acid in protein", 
            "hide": False },
        { 
            "code": "Amino_acids", 
            "display": "Amino acids", 
            "description":"Reference and variant amino acids",
             "hide": False },
        { 
            "code": "Codons", 
            "display": "Codons", 
            "description":"Reference and variant codon sequence", 
            "hide": False },
        { 
            "code": "Existing_variation", 
            "display": "Existing variant", 
            "description":"Identifier(s) of co-located known variants", 
            "hide": True },
        { 
            "code": "DISTANCE", 
            "display": "Distance to transcript", 
            "description":"Shortest distance from variant to transcript", 
            "hide": True },
        { 
            "code": "Feature_strand", 
            "display": "Feature strand", 
            "description":"Strand of the feature (1/-1)", 
            "hide": False },
        { 
            "code": "FLAGS", 
            "display": "FLAGS", 
            "description":"Transcript quality flags", 
            "hide": True },
        { 
            "code": "SYMBOL_SOURCE", 
            "display": "Symbol source", 
            "description":"Source of gene symbol", 
            "hide": True },
        { 
            "code": "HGNC_ID", 
            "display": "HGNC ID", 
            "description":"Stable identifer of HGNC gene symbol", 
            "hide": True },
        { 
            "code": "SWISSPROT", 
            "display": "SWISSPROT", 
            "description":"UniProtKB/Swiss-Prot accession", 
            "hide": True },
        { 
            "code": "TREMBL", 
            "display": "TREMBL", 
            "description":"UniProtKB/TrEMBL accession", 
            "hide": True },
        { 
            "code": "UNIPARC", 
            "display": "UNIPARC", 
            "description":"UniParc accession", 
            "hide": True },
        { 
            "code": "UNIPROT_ISOFORM", 
            "display": "UNIPROT ISOFORM", 
            "description":"Direct mappings to UniProtKB isoforms", 
            "hide": True },
        { 
            "code": "SOURCE", 
            "display": "Source", 
            "description":"", 
            "hide": True },
        { 
            "code": "SIFT", 
            "display": "SIFT", 
            "description":"SIFT prediction and/or score", 
            "hide": False },
        { 
            "code": "PolyPhen",  
            "display": "PolyPhen", 
            "description":"PolyPhen prediction and/or score", 
            "hide": False},
        { 
            "code": "HGVSc",  
            "display": "HGVSc", 
            "description":"HGVS coding sequence name", 
            "hide": True},
        { 
            "code": "HGVSp",  
            "display": "HGVSp", 
            "description":"HGVS protein sequence name", 
            "hide": True },
        { 
            "code": "HGVS_OFFSET",  
            "display": "HGVS Offset", 
            "description":"", 
            "hide": True },
        { 
            "code": "AF",  
            "display": "MAF", 
            "description":"Frequency of existing variant in 1000 Genomes combined population", 
            "hide": False 
            },
        						
        { 
            "code": "AFR_AF",  
            "display": "1000 Genomes AFR MAF", 
            "description":"Frequency of existing variant in 1000 Genomes combined African/American population", 
            "hide": True},
        { 
            "code": "1000 Genomes AMR_AF",  
            "display": "AMR MAF", 
            "description":"Frequency of existing variant in 1000 Genomes combined American population", 
            "hide": True},
        { 
            "code": "EAS_AF",  
            "display": "1000 Genomes EAS MAF", 
            "description":"Frequency of existing variant in 1000 Genomes combined East Asian population", 
            "hide": True },
        { 
            "code": "EUR_AF",  
            "display": "1000 Genomes EUR MAF", 
            "description":"Frequency of existing variant in 1000 Genomes combined European population", 
            "hide": True },
        { 
            "code": "SAS_AF",  
            "display": "1000 Genomes SAS MAF",
            "description":"Frequency of existing variant in 1000 Genomes combined South Asian population", 
            "hide": True },
        { 
            "code": "AA_AF",  
            "display": "1000 Genomes African American MAF", 
            "description":"Frequency of existing variant in NHLBI-ESP African American population", 
            "hide": True},
        { 
            "code": "EA_AF",  
            "display": "1000 Genomes EA MAF", 
            "description":"Frequency of existing variant in NHLBI-ESP European American population", 
            "hide": True},
        { 
            "code": "gnomAD_AF",  
            "display": "gnomAD MAF", 
            "description":"Frequency of existing variant in gnomAD exomes combined population", 
            "hide": True
        },
        { 
            "code": "gnomAD_AFR_AF",  
            "display": "gnomAD AFR MAF", 
            "description":"Frequency of existing variant in gnomAD exomes African/American population", 
            "hide": True},
        { 
            "code": "gnomAD_AMR_AF",  
            "display": "gnomAD AMR MAF", 
            "description":"Frequency of existing variant in gnomAD exomes American population", 
            "hide": True},
        { 
            "code": "gnomAD_ASJ_AF",  
            "display": "gnomAD ASJ MAF", 
            "description":"Frequency of existing variant in gnomAD exomes Ashkenazi Jewish population", 
            "hide": True},
        { 
            "code": "gnomAD_EAS_AF",  
            "display": "gnomAD EAS MAF", 
            "description":"Frequency of existing variant in gnomAD exomes East Asian population", 
            "hide": True },
        { 
            "code": "gnomAD_FIN_AF",  
            "display": "gnomAD FIN MAF", 
            "description":"Frequency of existing variant in gnomAD exomes Finnish population", 
            "hide": True },
        { 
            "code": "gnomAD_NFE_AF",  
            "display": "gnomAD NFE MAF", 
            "description":"Frequency of existing variant in gnomAD exomes Non-Finnish European population", 
            "hide": True },
        { 
            "code": "gnomAD_OTH_AF",  
            "display": "gnomAD OTH MAF", 
            "description":"Frequency of existing variant in gnomAD exomes other combined populations", 
            "hide": True },
        { 
            "code": "gnomAD_SAS_AF",  
            "display": "gnomAD SAS MAF",
            "description":"Frequency of existing variant in gnomAD exomes South Asian population", 
            "hide": True },
        { 
            "code": "gnomAD_AFR_AF",  
            "display": "gnomAD AFR MAF", 
            "description":"Frequency of existing variant in gnomAD exomes African/American population", 
            "hide": True},
        { 
            "code": "gnomAD_AMR_AF",  
            "display": "gnomAD AMR MAF", 
            "description":"Frequency of existing variant in gnomAD exomes American population", 
            "hide": True},
        { 
            "code": "gnomAD_ASJ_AF",  
            "display": "gnomAD ASJ MAF", 
            "description":"Frequency of existing variant in gnomAD exomes Ashkenazi Jewish population", 
            "hide": True},
        { 
            "code": 
            "gnomAD_EAS_AF",  
            "display": "gnomAD EAS MAF", 
            "description":"Frequency of existing variant in gnomAD exomes East Asian population", 
            "hide": True },
        { 
            "code": "gnomAD_FIN_AF",  
            "display": "gnomAD FIN MAF", 
            "description":"Frequency of existing variant in gnomAD exomes Finnish population", 
            "hide": True },
        { 
            "code": "gnomAD_NFE_AF",  
            "display": "gnomAD NFE MAF", 
            "description":"Frequency of existing variant in gnomAD exomes Non-Finnish European population", 
            "hide": True },
        { 
            "code": "gnomAD_OTH_AF",  
            "display": "gnomAD OTH MAF", 
            "description":"Frequency of existing variant in gnomAD exomes other combined populations", 
            "hide": True },
        { 
            "code": "gnomAD_SAS_AF",  
            "display": "gnomAD SAS MAF",
            "description":"Frequency of existing variant in gnomAD exomes South Asian population", 
            "hide": True },
        { 
            "code": "CLIN_SIG",  
            "display": "Clinical significance", 
            "description":"ClinVar clinical significance of the dbSNP variant", 
            "hide": False },
        { 
            "code": "SOMATIC",  
            "display": "Somatic status", 
            "description":"Somatic status of existing variant", 
            "hide": True },
        { 
            "code": "PHENO",  
            "display": "Phenotype or disease", 
            "description":"Indicates if existing variant(s) is associated with a phenotype, disease or trait; multiple values correspond to multiple variants", 
            "hide": True },
        { 
            "code": "PUBMED",  
            "display": "Pubmed", 
            "description":"Pubmed ID(s) of publications that cite existing variant", 
            "hide": False },
        { 
            "code": "G2P_complete",  
            "display": "G2P Confidence", 
            "description":"Indicates this variant completes the allelic requirements for a G2P gene", 
            "hide": False},
        { 
            "code": "G2P_flag",  
            "display": "Variant count by Zygosity", 
            "description":"Flags zygosity of valid variants for a G2P gene", 
            "hide": False},
        { 
            "code": "G2P_gene_req",  
            "display": "Allelic requirement", 
            "description":"MONO or BI depending on the context in which this gene has been explored", 
            "hide": False},
        { 
            "code": "GO_CLASSES",  
            "display": "Protein Functions", 
            "description":"Custom protein function annotations from GO", 
            "hide": False},
        { 
            "code": "PHENOTYPE", 
            "display": "Phenotype Annotation", 
            "description":"Custom phenotype annotations from HPO", 
            "hide": False },
        { 
            "code": "PPI", 
            "display": "PPIs", 
            "description":"Protein Protein Interactions", 
            "hide": False }
    ]
}

		