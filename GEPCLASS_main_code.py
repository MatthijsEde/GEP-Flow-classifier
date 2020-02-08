"""
This file cointains the main run code for running the GEPCLASS algorithm. 
Author: Matthijs van Ede
Date: 16-01-2020 
"""
import random
import operator
import own_operators as own
import make_chromosome as chrom
import to_compile as tcom
import modification_operator as mod


# Defining the operator and terminal set
# Change inputs
terminal = ["a", "b", "c", "d"]

# This name can NOT be changed!! see compiler
operatorlist = [operator.and_, 
                operator.or_, 
                operator.not_, 
                own.own_lt, 
                own.own_gt,
                own.own_le, 
                own.own_ge]


def evaluate(chromosome, terminal, operatorlist, X, n_genes): 
    """
    This function returns the "fitness" or in this test case the number of times the chromosome is results the correct answer

    input: 
            - chromosome: the actual chromosome to be evaluated
            - terminal: list with input terminals
            - operatorlist: list with operators
            - X: training data, input (list of lists)
            - Y: training data, output (list)

    return:
            - n_correct: int() number of times the chromosome was correct
    """

    # Om te testen
    #maximums = [0.9969159576076934, 0.9999219031110207, 0.6593284433098201]

    if n_genes == 2: 
        func_str = tcom.compiler(chromosome, terminal, operatorlist, operator.or_, True)
    elif n_genes > 2: 
        func_str = tcom.multi_compiler(chromosome, terminal, operatorlist, operator.or_, n_genes) # linking function 

    func = eval(func_str)
    n_correct = 0
    for i, x in enumerate(X): 
        # Change inputs
        r = func(x[0], x[1], x[2], x[3])
        if r == x[4]:
            n_correct += 1
    return n_correct


def roulettewheel(gen, gen_fitness, N): 
    """
    input: 
            - gen : generation; list with all chromosomes
            - gen_fitness : list with fittnes of each chromosome
            - N : number of selections to be done

    return: 
            - new_gen: a new generation with selected chromosomes
    WARNING!: this function does not use elitetism this has to be applied outside the loop by for example appending the best solution. 
    """
    sum_fit = sum(gen_fitness)
    wheel = [0]
    index_list = []
    new_gen = []

    for i, f in enumerate(gen_fitness): 
        p = wheel[i] + (f/sum_fit)
        wheel.append(p)

    for i in range(N): 
        r = random.random()
        index = -1 
        for w in wheel: 
            if r >= w: 
                index += 1
        index_list.append(index)

    for indx in index_list:
        tocopy = n_genes*[None] # for 2 genes
        for o, p in enumerate(gen[indx]): 
            for i, u in enumerate(p):
                    if i == 0: 
                        deep = [u]
                    else: 
                        deep += [u]
            tocopy[o] = deep
        new_gen.append(tocopy)

    return new_gen

   

# -------- Start of the algorithm --------
"""
IT IS NOW SET TO 2D!!!
"""

# # Defining the dataset for testing
# # Exact solution:
# def test_func(a, b):
#     return (a-b > 0)


# Reading data from dataset
file = open("inputs_new.txt", "r")
datalist = []

for i, row in enumerate(file):
    if i>200 and i<600:
        row = row.strip("\n")
        data = row.split("]")
        data = data[:-1]
        for j, element in enumerate(data):
            if j > 1 and j < 120:
                element = str(element) + "]"
                datalist.append(eval(element))    



print("best solution would be:", len(datalist))

# # Dataset
# Input = []
# Output = []
# for i in range(10000): # change training number
#     a = round(random.uniform(-1, 1), 2)
#     b = round(random.uniform(-1, 1), 2)
#     c = round(random.uniform(-1, 1), 2)
#     d = round(random.uniform(-1, 1), 2)
#     # Change inputs
#     Input.append((a, b))
#     Output.append(test_func(a, b))


#Creating initial generation
generation = []
n_genes = 4 # n_genes = number of genes
for i in range(250):
    c = chrom.generate_chromosome(n_genes, operatorlist, terminal, 7)
    generation.append(c)


running = True
runs = 25
while running: 
    best = [None, 0] # best chromosome, fittness of best chromosme
    gen_fitt = [] # generaion fittness
    for indv in generation:
        #print(indv)
        correct = evaluate(indv, terminal, operatorlist, datalist, n_genes)
        fittness = correct/len(datalist) # change this value according to how many correct values are possible, change training number
        gen_fitt.append(fittness)
    
    deepcopy = n_genes*[None] # just to test
    for i, fitt in enumerate(gen_fitt): 
        if fitt > best[1]: 
            
            for r, q in enumerate(generation[i]): 
                for e, w in enumerate(q): 
                    if e == 0: 
                        deep = [w]
                    else: 
                        deep += [w]
                deepcopy[r] = deep
            
            best[0] = deepcopy
            best[1] = fitt
    

    if runs == 0: 
        running = False
    if best[1] == 1: 
        running = False
    if len(gen_fitt) == 1: 
        running = False
    
    print("run:", runs,  " - number correct:", best[1]*len(datalist), " - difference:", len(datalist) - best[1]*len(datalist) ) # change training number
    
    new_generation = roulettewheel(generation, gen_fitt, (len(generation) - 11))

    for i, chrm in enumerate(new_generation): 
        rint = random.randint(0, 3)
        if rint == 0: 
            new_generation[i] = mod.mutation_uniform(chrm, terminal, operatorlist)
        if rint == 1: 
            new_generation[i] = mod.mut_IS(chrm, 7)
        if rint == 2: 
            new_generation[i] = mod.mut_RIS(chrm, operatorlist, 7)
        if rint == 3: 
            if i != (len(new_generation) - 1): 
                new_generation[i], new_generation[i+1] = mod.recombination(chrm, new_generation[i+1], terminal, operatorlist, 7)
            else:
                new_generation[i] = mod.mutation_uniform(chrm, terminal, operatorlist)
        
    new_generation.append(best[0]) 

    generation = new_generation
    runs -= 1 
  
print("best chrm:", best[0])
print("fittness:", best[1])
#print(tcom.compiler(best[0], terminal, operatorlist, operator.or_, True))
print(tcom.multi_compiler(best[0], terminal, operatorlist, operator.or_, n_genes))