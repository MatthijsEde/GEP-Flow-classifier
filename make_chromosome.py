"""
This file cointains the definitions for creating the genes and chromosomes
This file is a subfile beloning to the GEPCLASS algorithm --> see: GEPCLASS_main_code.py

!! This file is only applicable for the operatos used in GEPCLASS_main_code.py, because it assumes a certain operatorlist order. 
!! It only works for 4 inputs now, some values will have to be changed in order to make it correct. (in de rint statements)

Author: Matthijs van Ede
Date: 04-12-2019 
"""

import random
import operator
import own_operators as own

def generate_gene(functions, terminal, headlength): 
    """
    This function will create a single gene, with the operator order based on the GEPCLASS ruleset. 

    arguments: 
        functions:  list with all available operators
        terminal:   list with all available terminals
        headlength: length of the gene head section

    Return: 
        The function will return a single gene
    
    Notice that the tail length can be calculated by t = h*(max_arity_operator -1 ) + 1
    """
    h = headlength
    arity_max = 2 # The logical operators take 2 arguments
    t = int((h*(arity_max - 1) + 1)/2)
    gene = [None]*(h + t)
    max_logical = int((h-1) / 2) # Expression that describes the maximum number of logical operators allowed in the head section 
    logical_count = 0
    relational_count = 0
    not_count = 0

    index_0_log = False # logical operator
    index_0_rel = False # relational operator
    index_0_ter = False # terminal
    logical_break = False # to break the logical iteration

    # variables used for the indexing
    relational_left = 0
    index = 0
    max_rel_index = 0


    # Creating the head
    rnum = random.random()

    # index 0
    # logical 
    if (rnum < 0.6): 
        rint = random.randint(0, 2)
        gene[0] = functions[rint]
        logical_count = logical_count + 1
        index_0_log = True
    
    # relational
    elif (rnum >= 0.6 and rnum <= 1.0): 
        rint = random.randint(3, 6)
        gene[0] = functions[rint]
        index_0_rel = True
    
    # terminal --> This is impossible due to the rules of GEPCLASS
    # elif (rnum >= 0.75):
    #     rint = random.randint(0, 3)
    #     terminal_choose = terminal[rint]
    #     gene[0] = terminal_choose + str(random.randint(1, 9)) # Choosing the terminal constant between 1 and 10 
    #     index_0_ter = True

    
    # index 1 -> (h-1)
    # if index 0 was a logical operator
    if index_0_log:
        for i in range(1, h):
            rint = random.randint(0, 6)
            gene[i] = functions[rint]

            if (gene[i] == operator.and_  or gene[i] == operator.or_ or gene[i] == operator.not_):
                if logical_count < max_logical:
                    logical_count = logical_count + 1
                else: 
                    rint = random.randint(3, 6)
                    gene[i] = functions[rint]
                    relational_count = relational_count + 1
                    index = i
                    logical_break = True       

            else: 
                index = i
                logical_break = True
            
            if logical_break:
                break

        for i in range(0, h): 
            if gene[i] == operator.not_:
                not_count = not_count + 1
        
        relational_left = logical_count - not_count 
        max_rel_index = index + relational_left + 1

        for i in range((index + 1), max_rel_index): 
            rint = random.randint(3, 6)
            gene[i] = functions[rint]

        if max_rel_index != h: 
            for i in range(max_rel_index, h): 
                r_int = random.randint(0, 3)    # Change inputs
                terminal_choose = terminal[r_int]
                gene[i] = terminal_choose + str(round(random.uniform(-1, 1), 5)) 

    # if index 0 is a relation operator
    if index_0_rel or index_0_ter: # filling up the head with terminals
        for i in range(1, h): 
            r_int = random.randint(0, 3)    # Change inputs 
            terminal_choose = terminal[r_int]
            gene[i] = terminal_choose + str(round(random.uniform(-1, 1), 5)) 


    # creating the tail
    for j in range(h, (h + t)):
        r_int = random.randint(0, 3)    # Change inputs
        terminal_choose = terminal[r_int]
        gene[j] = terminal_choose + str(round(random.uniform(-1, 1), 5)) 
    
    return gene

            
def generate_chromosome(n, function, terminal, headlength):
    """
    This function will create a single chromosome, with the operator order based on the GEPCLASS ruleset. 

    arguments:
        n:          number of genes per chromosome 
        functions:  list with all available operators
        terminal:   list with all available terminals
        headlength: length of the gene head section

    Return: 
        The function will return a single chromosome
    
    """
    chromosome = []
    
    for i in range(n): 
        chromosome.append(generate_gene(function, terminal, headlength))
    
    return chromosome









