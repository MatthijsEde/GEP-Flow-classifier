import random
import operator
import own_operators as own
import make_chromosome as chrom
from collections.abc import Iterable

"""
This file cointains the compile algorithm to compile a chromosome to a working lambda functions 
Author: Matthijs van Ede
Date: 15-01-2019

The first function element_converter() is there to convert a operator to an operatorlist[<index>] as this can be read by the eval() function
Inputs:     - element: the actual element (operator or terminal) you want to convert
            - terminal: the list with input terminals
            - operatorlist: the list with operators

Returns: str(): operatorlist[<index of operator in list>] or just the terminal


The second function compiler() is there to actually make a lambda function, type = str(), which can be used in the eval() function
Inputs:     - chromosome: the actual chromosome, consisiting out of 2 genes. IMPORTANT the linker right now only works for 2 genes!
            - terminal: the list with input terminals
            - operatorlist: the list with operators
            - linker: linker function that links the individual genes inside the chromosomes

Returns: str(): "lambda <arguments> : <function>" --> which can be used for eval() to get an actual working function


IMPORTANT!
The name of operatorlist, "operatorlist" should NOT change in the main file, otherwise element_converter() will not work, and in their turn eval(compiler())
The code only runs for input values [-1.0, 1.0]
"""

# Converts the code to something eval() can read
def element_converter(element, terminal, operatorlist):
    return_str = None
    index_oper = None
    if element in operatorlist: 
        index_oper = operatorlist.index(element)
        return_str = "operatorlist" + "[" + str(index_oper) + "]"
        return return_str
    else: 
        return element
            


#Compiler from a chromosome to a lambda function
def compiler(chromosome, terminal, operatorlist, linker, two_genes):
    # about this linker it now only accomodates 2 genes!!!!!!! for the final code this number might have to increase!
    func = element_converter(linker, terminal, operatorlist) + "( "
    for num_gene, gene in enumerate(chromosome):
        code = None
        inputs = []
        for t in terminal: 
            inputs.append(t[0])
        arguments = ', '.join(inputs)
        
        num_rel = 0
        rel_index = 0

        for i, element in enumerate(gene): 
            for oper in operatorlist[3 : 7]:
                if element == oper: 
                    num_rel = num_rel + 1
                    rel_index = i
        
        
        code = gene[:(rel_index + num_rel + 1)]
         
        # start sorting the code to get the right expression
        flat_sort_code = []
        sort_code = [None]
        running = True
        code_index = 0

        #print("code", code)
        # Applying the arity to the "None" spots
        while running:
            for j, element in enumerate(sort_code): 
                if element == None: 
                    if code[code_index] == operator.not_:
                        sort_code[j] = [code[code_index], None]
                        code_index = code_index + 1
                        continue
                    elif code[code_index] in operatorlist:
                        sort_code[j] = [code[code_index], None, None]
                        code_index = code_index + 1
                        continue
                    else: 
                        sort_code[j] = code[code_index][0]
                        if j != 0:
                            sort_code[j+1] = code[code_index][1:]
                        else:
                            sort_code.append(code[code_index][1:])
                        code_index = code_index + 1

            # flattining the sort_code list, as it is a list of lists, we want a single list
            flat_sort_code = []
            for e in sort_code: 
                try: # testing if the element of the sort_code is iterable
                    iterator = iter(e) 
                except TypeError:
                    flat_sort_code.append(e)
                else:
                    for f in e: 
                        if ((f == "0") or (f == "-") or (f == "1")): 
                            flat_sort_code.append(e)
                            break
                        flat_sort_code.append(f)        

            sort_code = flat_sort_code  

            # checking whether there is still a "None" in the sorted list
            none_num = 0
            for t in sort_code: 
                if t == None: 
                    none_num = none_num + 1

            if none_num == 0: 
                running = False
        
        # -------
        final_code = ""
        num_close = 0
        num_args = 2
        not_active = False
        

        for i, element in enumerate(sort_code):        
            if element in operatorlist:
                final_code = final_code + element_converter(element, terminal, operatorlist) + "("
                num_close += 1
                if element == operator.not_: 
                    num_args = 1
                    not_active = True
                else: 
                    if not_active:
                        if (element == operator.and_ or element == operator.or_):
                            num_args += 1
                        not_active = False

            elif element in terminal: 
                final_code = final_code + element_converter(element, terminal, operatorlist) + ", "
                num_args -= 1
                continue
            else:
                final_code = final_code + element_converter(element, terminal, operatorlist) + ")"
                num_close -= 1
                if ((i != (len(sort_code) - 1)) and (num_args != 0)):
                    final_code = final_code + ", "
            if num_args == 0: 
                final_code = final_code + ")"
                if i != (len(sort_code) - 1):
                    final_code = final_code + ", "
                num_close -= 1
                num_args = 2
                
        if num_close != 0: 
            for j in range(num_close):
                final_code = final_code + ")"
        




        # creating the final string combining the n genes
        if num_gene != (len(chromosome) - 1):
            func = func + str(final_code) + " , "
        else:
            func = func + str(final_code) + " )"

        #print("\n FINAL: \n", func)

        #print("final code:", final_code, "\n")
        # -------
    if two_genes:
        func = 'lambda {} : {}'.format(arguments, func)
    return func


def multi_compiler(chromosome, terminal, operatorlist, linker, n_genes):
    """
    Inputs:     - chromosome: the actual chromosome, consisiting out of 2 genes. IMPORTANT the linker right now only works for 2 genes!
            - terminal: the list with input terminals
            - operatorlist: the list with operators
            - linker: linker function that links the individual genes inside the chromosomes
            - n_genes: number of genes in the chromosome Note! it has to be 2^n

    Returns: str(): "lambda <arguments> : <function>" --> which can be used for eval() to get an actual working function
    """
    inputs = []
    for t in terminal: 
        inputs.append(t[0])
    arguments = ', '.join(inputs)

    if linker == operator.and_: 
        indx = 0
    if linker == operator.or_: 
        indx = 1

    link_pair = []
    i = 0
    running = True
    while running: 
        if i == (len(chromosome) - 2):
            running = False
        link_pair.append(compiler([chromosome[i], chromosome[i+1]], terminal, operatorlist, linker, False))
        i += 2

    run = True
    skip = False
    while run:
        if len(link_pair) != 2:
            link_pair_next = []

            for j, pair in enumerate(link_pair):
                if skip: 
                    skip = False
                    continue 
                new_pair = "operatorlist" + "[" + str(indx) + "]" + "( " + str(link_pair[j]) + " , " + str(link_pair[j+1]) + ")"
                link_pair_next.append(new_pair)
                skip = True

            link_pair = link_pair_next
        else: 
            run = False

    result_func = "operatorlist" + "[" + str(indx) + "]" + "( " + str(link_pair[0]) + " , " + str(link_pair[1]) + ")"
    result = 'lambda {} : {}'.format(arguments, result_func)

    return result

