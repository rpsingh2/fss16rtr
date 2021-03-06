# Exploration of Early Termination using DTLZ7 model

## Abstract
The stopping conditions for optimizers are typically defined to be a set condition. This however can have negative effects on overall performance especially when using large models. It is worthwhile to explore different ending conditions that are not so static. While analyzing changes in the optimized solution during runtime, perhaps insight can be gained about appropriate conditions for early termination. The overall goal is to minimize computational time while maximizing the amount of optimization done within the same timeframe.

## Introduction
Within this section you will find a brief overview of the optimizers that were used in this experiment (DE, MWS, SA) as well as some descriptions of statistical comparators.

### Simulated Annealing
Simulated Annealing uses a limited set of memory to determine the best solution given an optimization problem. The only three pieces of information a simulated annealer keeps track of is the newest solution, the best solution and the current solution. Early on within this algorithm random jumps are made in order to explore the Model's landscape. As time progresses, the simulated annealer settles down and begins to look for more stable solutions. This is known as the algorithms cooling factor. This interesting behavior helps the simulated annealer avoid local maxima and minima.
```
While has lives and has generations left
  generate candidate solution
  if candidate solution better than best solution:
    candidate solution saved as best solution
  if candidate solution better than current solution:
    candidate solution saved as current solution
  else if (cooling function returns hot value):
    candidate solution saved as current solution
```

### Max-WalkSat
Max-WalkSat is similar to Simulated Annealing, but does not have a cooling factor feature. Instead Max-WalkSat has a certain probability of preforming a local search while jumping around the globally. This also helps avoid local maxima and minima by exploring solutions within the current area.

```
While has lives and has generations left
  generate candidate solution
  if candidate solution better than best solution:
    candidate solution saved as best solution
  if candidate solution better than current solution:
    candidate solution saved as current solution
  
  if random chance:
    Do local search
      if local search solution better than candidate solution
        local search solution better than candidate solution
      if local search solution better than best solution
        local search solution better than best solution
```

### Genetic Algorithm
This optimization technique maintains a population of different solutions while continually to increase the value of said solutions. Genetic algorithms mimic the process of evolution. Individual members of a population bred and produce offspring which then compete with their parents in order to form a set of candidate solutions. This occurs for a set number of generations until a final population containing the best set of solutions is produced.

```
while gen < gens:
    children = []
    for _ in range(pop_size):
        mom = random.choice(population)
        dad = random.choice(population)
        while (mom == dad):
            dad = random.choice(population)
        child = mutate(crossover(mom, dad), mutation_rate)
        if problem.is_valid(child) and child not in population+children:
            children.append(child)
    population += children
    population = elitism(population, pop_size)
    gen += 1

```

### Differential Evolution
The most complicated and newest algorithm of the bunch. This is a type of Genetic Algorithm, meaning that a population of different solutions are maintained and evolved over time. This difference in the operation of Differential Evolution and the singe objective non-population driven optimizers had to be accounted for.

Differential Evolution uses a different mutator method compared to a standard genetic algorithm. DE mutates an individual's decision such that:

new = X + F*(Y - Z)

Where X, Y and Z are other random individual's decisions and F is a set constant.

In this experiment a population of 100 individuals were used. The crossover rate was set to 30% while the mutation factor was 75%. The mutation scheme is DE/rand/1.

```
While has generations left and has lives
	Mutated population = Mutate(population)
	Return n fittest from population
	Save new population	
```

### Comparison Operators
#### Type 1: BDOM
Since Simulated Annealing and Max WalkSat are both traditionally single objective optimizers, I thought it would be interesting to implement them in a way that they could optimize multiple objectives at once. In order to do this, Binary Domination was implemented. A solution from one round of optimization is considered better than a solution from the previous era if the first solutions objectives are greater than both of the objectives of the second solution.

```
def bdom(one, two):
    dominates = False
    
    for i in number of objectives:
        if two[i] < one[i]:
            return False
        elif one[i] < two[i]:
            dominates = True
    
    if dominates: return True
    return False
```

#### Type 2: A12
In order to judge the difference in improvement for each optimizer’s current and previous solutions, the A12 small effect comparison was used. A12 is used to determine the overall difference between two sets of numbers. A12 is used to measure the probability that running an algorithm using one set of numbers yields a higher result than running the same algorithm using the second set of numbers. According to Vargha and Delaney, the output from the A12 test can be viewed as such:

-	A12 > 71% represents a large difference
-	A12 > 64% represents a medium difference
-	A12 =< 56% or less represents a small difference

Within the optimizers I implemented, if A12 shows a small difference between the current solution and a candidate solution, the algorithm is assumed to be close to converting to a solution. As such, the optimizer is set to terminate earlier.

```
lives = 10
while has eras and lives

  DO OPTOMIZATION

  if A12 between candidate and current solutions < 56%
    lives - 1
  else:
    lives + 3
    
end
```

#### Type 3: Scott-Knott
The Scott-Knot test is used for clustering results into similar categories. Scott-Knot recursively bi-clusters the output from each of the optimizers into ranks. At each level of ranks, another split is created where the expected values are the most different. Before continuing, Boostrap (random sampling) and A12 are called to check and see if the splits are significantly different.

### Model: DTLZ7
![alt tag](http://people.ee.ethz.ch/~sop/download/supplementary/testproblems/dtlz7/images/dtlz7_Formulation.png)


DTLZ7 is a model created in order to test the potential for optimizers to find and maintain several distinct disjointed pareto-optimal solutions. As you can see, when using two objectives, x1 and x2, the pareto-optimal regions are spread out quite a bit. With DTLZ7 it is possible to implement the model using any number of objectives and any number of decisions.

## Experimental Setup
In order to explore this problem, three optimization techniques were used; Differential Evolution, MaxWalkSat and Simulated Annealing. The model DTLZ7 was used for optimization. With this model, 10 decisions were used as input to the model I tried to minimize the output for two objectives. 20 Runs of each model were used and the results between cdom loss of the first population and the last population were recorded.

## Results

### Comparison using Cdom 
Continuous domination can be compared to binary domination in that they are both uses to compare the dominance of solutions. The difference is that continuous domination determines by how much one point in space dominates another. Instead of returning a binary "yes or no", cdom returns a value indicating how much one list dominates the other. With continuous domination, the differences between two lists are also increased by an exponential factor. As a result, points that dominate a solution by quite a bit stand out more than points that dominate solutions only by a slight margin.

```
def cdom(self, x, y):
    def expLoss(w, x1, y1, n):
        return -1 * (w * (x1 - y1) / n)

    def loss(x, y):
        losses = []
        n = min(len(x), len(y))
        for obj in range(n):
            x1, y1 = x[obj], y[obj]
            losses += [expLoss(-1, x1, y1, n)]
        return sum(losses) / n

    l1 = loss(x, y)
    return l1

```

### Analysis of Results

```
# Of Eras
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,          mws ,    1000  ,     0 (*              |              ),10.00, 10.00, 10.00, 10.00, 10.00
   1 ,           de ,    1000  ,     0 (*              |              ),10.00, 10.00, 10.00, 10.00, 10.00
   2 ,           sa ,    2600  ,  8900 (     *         |              ),10.00, 10.00, 26.00, 99.00, 99.00

CDOM Between Initial and Final Objectives
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,          mws ,      26  ,    65 (  ---  *    ---|-             ),-0.14,  0.06,  0.26,  0.62,  0.95
   1 ,           sa ,      41  ,    75 (    -     *  --|-----------   ),-0.00,  0.05,  0.41,  0.65,  1.68
   1 ,           de ,      50  ,     8 (           *   |              ), 0.45,  0.46,  0.50,  0.53,  0.55
```

From the table above it is clear that Simulated Annealing on average takes the most amount of runs to make meaningful gains in terms of minimizing its objectives. Max Walksat and Differential Evolution on average take only 10 eras to finish execution while Simulated Annealing finishes in 26 eras.

The bottom chart shows the overall change in the initial and ending population objectives using CDOM. In with this measurement, the higher the value the better. As you can see, Differenetial Evolution ened up having on average the best result for CDOM loss.

## Threats to Validity
* It is possible that the setup for Max WalkSat and Simulated Annealing were suboptimal for this sort of comparison. Judging the performance of a population based method such as Differential Evolution to that of a simpler non Genetic Algorithm style problem could be explored more.
* The overall number of retries per optimization technique could be expanded in order to guarantee a more accurate final result.
* Results of this experiment may solely depend on the model used. Retrying this test with different models may yield results contradictory to what is displayed here.

## Future Work
* Results for the above tests may change based on the type of model used. It is possible that Simulated Annealing or Max WalkSat preforms better on certain models than Differential Evolution does and vice-versa.
* May need to investigate the final Hypervolume, Spread and IGD of the final values for each of the optimizers. It would make for an interesting comparison.
* May be worthwhile to explore the effects of using a Genetic Algorithm to optimize Simulated Annealing, Max WalkSat and Differential Evolution in order to compare the overall performance of optimized optimizers against one another.

## References
* [1] http://people.ee.ethz.ch/~sop/download/supplementary/testproblems/dtlz7/index.php
* [2] https://github.com/txt/ase16/blob/master/doc/perform.md
* [3] https://github.com/txt/ase16/blob/master/doc/talk3sa.md
* [4] https://github.com/txt/ase16/blob/master/doc/mws.md
