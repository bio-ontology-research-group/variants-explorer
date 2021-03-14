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
    "SIFT" : [ 
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
        { "code" : "3_prime_UTR_variant", "display": "", "description":"3 prime UTR variant", "class":"SO:0001624", "ontology": "SO"},
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
    ]
}