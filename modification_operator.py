import random
import operator

"""
This file contains the code that define the modification operators used in GEPCLASS 
Author: Matthijs van Ede
Date: 12-12-2019 
"""

def mutation_uniform(chrm, terminal, operatorlist): 
    n = 1 # number of mutations to be performed
    
    chromosome = chrm.copy()
    # print(chromosome)

    for i in range(n):
        n_genes = len(chromosome)
        r_gene = random.randint(0, (n_genes - 1))
        gene = chromosome[r_gene]
       # print("gene:", r_gene)

        max_index = len(gene) - 1
        r_index = random.randint(0, max_index)
       # print("index:", r_index)

        if gene[r_index] in operatorlist[0:3]: 
            if gene[r_index] != operator.not_:
                rint = random.randint(0, 1)
                gene[r_index] = operatorlist[rint]
        
        elif gene[r_index] in operatorlist[3:7]: 
            rint = random.randint(3, 6)
            gene[r_index] = operatorlist[rint]
        
        else:
            rint = random.randint(0, 3)     # Change inputs
            terminal_choose = terminal[rint]
            gene[r_index] = terminal_choose + str(round(random.uniform(-1, 1), 5)) 

    return chromosome


def recombination(chromosome1, chromosome2, terminal, operatorlist, h):
    r = random.random()

    # 1p crossover
    if r < 0.5:
        t = int((h + 1)/2) + 1 # + 1 is used to get the right index in [...: t], it has nothing to do with the tail length!

        # deciding the gene to perform the crossover
        # switching the tails in this gene
        rint = random.randint(0, (len(chromosome1)-1))
        tmp_gene_tail = chromosome2[rint][h:(h+t)] # WERKT NOG NIET ! lijst blijft leeeeeeeeeeeeeeg :(
        chromosome2[rint][h:(h+t)] = chromosome1[rint][h:(h+t)]
        chromosome1[rint][h:(h+t)] = tmp_gene_tail

        #switching the trailing genes, from the crossover point
        for j in range((rint + 1), len(chromosome1)):
            tmp_gene = chromosome2[j]
            chromosome2[j] = chromosome1[j]
            chromosome1[j] = tmp_gene



    # 2p crossover
    # Still to be implemented if needed, nothing is said about this function in the GEPCLASS paper
    # elif (r >= 0.9 and r < 0.91):
    #     print("2p cx")


    # gene crossover
    else:
        rint = random.randint(0, (len(chromosome1)-1))
        tmp_gene = chromosome2[rint]
        chromosome2[rint] = chromosome1[rint]
        chromosome1[rint] = tmp_gene


    return chromosome1, chromosome2


def mut_IS(chromosome, h): 
    """
    inputs: 
        chromosome: chromosome to be modified
        h         : headlength of gene
    
    return: 
        modified chromosome
    """
    
    # Implementing a safety net, in the case that a chromosome consists out of 1 gene.
    if len(chromosome) < 2: 
        print("For IS a chromosome should have at least 2 genes!")
        return chromosome

    # selecting a gene for copying and for inserting
    rint = random.randint(0, (len(chromosome)-1))
    gene_copy_index = rint
   # print("gene", rint)
    rint_II = random.randint(0, (len(chromosome)-1))
    gene_insert_index = rint_II
    #print("gene in", rint_II)

    # length of tail
    t = int((h + 1)/2)

    # choosing the part to be copied
    r_start = random.randint(0, (t-1))
    if r_start == (t-1):
        r_end = r_start
    else:
        r_end = random.randint((r_start + 1), (t-1))

    # list to be copied
    copy_list = chromosome[gene_copy_index][(h + r_start):(h  + r_end + 1)]
   # print("copy list", copy_list)

    # inserting: 
    r_insert = random.randint(0, (t - len(copy_list)))
    if ((t-len(copy_list)) == 0): 
        chromosome[gene_insert_index] = chromosome[gene_insert_index][0 : h] + copy_list
    elif r_insert == 0: 
        chromosome[gene_insert_index] = chromosome[gene_insert_index][0 : h] + copy_list + chromosome[gene_insert_index][(h + r_insert) : (h + (t-len(copy_list)))]
    else: 
        chromosome[gene_insert_index] = chromosome[gene_insert_index][0 : h] + chromosome[gene_insert_index][h : (h + r_insert)] + copy_list + chromosome[gene_insert_index][(h + r_insert) : (h + (t-len(copy_list)))]

    return chromosome


def mut_RIS(chromosome, operatorlist, h): 
    """
    From the GEPCLASS paper: 
    in RIS transposition, the donor site is in the tail of a gene,
    whereas the receptor site is always the first terminal of this same gene
    """
    
    # choosing a gene
    r_gene = random.randint(0, (len(chromosome) - 1))
    #print("gene index:", r_gene)

    running = True
    firts_terminal_index = 0
    # finding the first terminal index
    while running: 
        if chromosome[r_gene][firts_terminal_index] in operatorlist: 
            firts_terminal_index += 1
        else: 
            running = False
    
    # length of tail
    t = int((h + 1)/2)

    # choosing the part to be copied
    r_start = random.randint(0, (t-1))
    if r_start == (t-1):
        r_end = r_start
    else:
        r_end = random.randint((r_start + 1), (t-1))

    # list to be copied
    copy_list = chromosome[r_gene][(h + r_start):(h  + r_end + 1)]
    #print("copy list:", copy_list)

    chromosome[r_gene] = chromosome[r_gene][0 : firts_terminal_index] + copy_list + chromosome[r_gene][firts_terminal_index : h] + chromosome[r_gene][h : (h + t - len(copy_list))]

    return chromosome




        


    
    
