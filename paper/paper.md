---
title: 'extended PROVEAN annotation tool'
tags:
  - python
  - singularity
  - bioinfomatics
  - molecular biology
authors:
  - name: Takumi Ito^[co-first author]
    orcid: 0000-0002-6376-584X
    affiliation: 1
  - name: Kazutoshi Yoshitake^[co-first author]
    orcid: 
    affiliation: 1
  - name: Takeshi Iwata
    orcid: 
    affiliation: 1
  
affiliations:
  - name : The Molecular and Cellular Biology Division at the National Institute of Sensory Organs (NISO), National Hospital Organization Tokyo Medical Center
    index: 1
    
date: 13/10/2021
bibliography: paper.bib
---

# Summary

The 'ePat' (extended PROVEAN annotation tool) is a software tool that extends the functionality of PROVEAN: a software tool for predicting whether amino acid substitutions and indels will affect the biological function of proteins. The 'ePat' extends the conventional PROVEAN to enable the following two things. Fisrt is to calculate the damage level of indel mutations with frameshift and mutations near splice junctions, for which the conventional PROVEAN could not calculate the damage level of these mutations. Second is to use batch processing to calculate the damage level of multiple mutations in a mutation list (VCF file) in a single step.In order to identify variants that are predicted to be functionally important from the mutation list, ePat can help filter out variants that affect biological functions by utilizing not only point mutation, and indel mutation that does not cause frameshift, but also frameshift, stop gain, and splice variant.

# Statement of Need

In recent years, improvements in sequencing technology have generated a large amount of information on mutations in diseased people and organisms with specific phenotype compared to normal phenotype. Mutations suchc as amino acid substitutions, insertions, deletions, frameshifts, and acquisition of stop codons affect protein function.

Computational tools such as Polyphen, SIFT, and PROVEAN have been developed to search for mutations that cause diseases or specific phenotypes, and to quantify the impact of sequence variations on protein function (damage score). However, these tools have two problems: first, they are unable to calculate mutations that are considered to have a significant impact on protein function, such as frameshift and stop gain, and second, they are cumbersome because they need to calculate mutations that spread across multiple genomic regions.

We have developed 'ePat' (extended PROVEAN annotation tool), an extension of PROVEAN that solves the above two problems. Unlike existing tools, ePat is able to calculate the damage score of mutations near the splice junction, frame shift, stop gain, and start Lost. In addition, batch processing is used to calculate the damage score of all mutations in a VCF file at once.

# ePat

Using the given reference, we create a database for SnpEff and annotate with SnpEff. We then extract mutations that have a HIGH or MODERATE mutation hazard level as a result of the SnpEff annotation. For each row of the VCF file, extract the information of the mutation annotated with SnpEff. From this information, the mutations are classified into 5 categories. The first is variants near the splice junction(splice variants), the second is frameshift, the third is stop gain, the fourth is start lost, and the last is inframe variants (point Mutation or indel mutations that do not cause frameshift). 

Variants from category 1 to 4 are given a damage level score as defined by ePat, and category 5 will be gived a damage level score by PROVEAN. The damage level score defined by ePat is calculated with the following method. For each amino acid, calculate the damage level score when it is replaced by each of the 20 amino acids. The average of these damage level score is used as the damage level score for that frame. The minimum damage level score for each frame is the damage level score of this mutation.

# Acknowledgments

# Reference
