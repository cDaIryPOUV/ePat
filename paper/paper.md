---
title: 'extended PROVEAN annotation tool'
tags:
  - Python
  - Singularity
  - SNP Annotation
  - PROVEAN
authors:
  - name: Takumi Ito
    orcid: 0000-0002-6376-584X
    affiliation: 1, 2
  - name: Kazutoshi Yoshitake
    orcid: 
    affiliation: 1, 2
  - name: Takeshi Iwata
    orcid: 
    affiliation: 1
  
affiliations:
  - name : The Molecular and Cellular Biology Division at the National Institute of Sensory Organs (NISO), National Hospital Organization Tokyo Medical Center
    index: 1
  - name : Laboratory of Aquatic Molecular Biology and Biotechnology, Aquatic Bioscience, Graduate school of Agricultural and Life Sciences, The Univresity of Tokyo
    index: 2
    
date: 13/10/2021
bibliography: paper.bib
---

# Summary

The 'ePat' (extended PROVEAN annotation tool) is a software tool that extends the functionality of PROVEAN: a software tool for predicting whether amino acid substitutions and indels will affect the biological function of proteins. The 'ePat' extends the conventional PROVEAN to enable the following two things. Fisrt is to calculate the pathogenicity of indel mutations with frameshift and variants near splice junctions, for which the conventional PROVEAN could not calculate the pathogenicity of these variants. Second is to use batch processing to calculate the pathogenicity of multiple variants in a variants list (VCF file) in a single step.In order to identify variants that are predicted to be functionally important from the variants list, ePat can help filter out variants that affect biological functions by utilizing not only point mutations, and indel mutations that does not cause frameshift, but also frameshift, stop gain, and splice variants.

# Statement of Need

In recent years, improvements in sequencing technology have generated a large amount of information on mutations in diseased people and organisms with specific phenotype compared to normal phenotype. Mutations suchc as amino acid substitutions, insertions, deletions, frameshifts, and acquisition of stop codons affect protein function[@kawamura2018] [@hayashi2021] [@minegishi2016] [@mizobuchi2020] [@suga2016] [@yang2020].

Computational tools such as Polyphen[@adzhubei2010], SIFT[@kumar2009], PROVEAN[@choi2015], and other prediction tools[@suybeng2020] have been developed to search for variants that cause diseases or specific phenotypes, and to quantify the impact of variants on protein function (pathogenicity). PROVEAN made it enable to predict the pathogenicity of variants not limited to single amino acid substitutions but also in-frame insertions, deletions, and multiple amino acid substitutions[@choi2012]. However, these tools have two problems: first, they are unable to calculate variants that are considered to have a significant impact on protein function, such as frameshift and stop gain, and second, they cannot calculate the pathogenicity of variants that spread across multiple genes at a time.

We have developed 'ePat' (extended PROVEAN annotation tool), an extension of PROVEAN that solves the above two problems. Unlike existing tools, ePat is able to calculate the pathogenicity of variants near the splice junction, frame shift, stop gain, and start Lost. In addition, batch processing is used to calculate the pathogenicity of all variants in a VCF file at once.

# ePat

With the given reference, we create a database for SnpEff and annotate with SnpEff. We then extract variants that have a HIGH or MODERATE pathogenicity level as a result of the SnpEff annotation. For each row of the VCF file, extract the information of the variants annotated with SnpEff. With this information, the variants are classified into 5 categories. The first is a variant near the splice junction(splice variants), the second is frameshift, the third is stop gain, the fourth is start lost, and the last is inframe variants (point mutation or indel mutations that do not cause frameshift). 

Variants from category 1 to 4 are given pathogenicity as defined by ePat, and category 5 is given pathogenicity by PROVEAN. The pathogenicity defined by ePat is calculated with the following method. For each amino acid, calculate the pathogenicity when it is replaced by each of the 20 amino acids. The average of these pathogenicity is used as the pathogenicity for that position. The maximum pathogenicity for each position is the pathogenicity of this variants.

# Reference
