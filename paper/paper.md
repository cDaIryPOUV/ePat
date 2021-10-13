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

