# freq_patterns

This is an implementation of two frequent pattern mining algorithms: Apriori and FP-Growth. 

Both functions take a list of transactions as inputs and return a 2 by n dimensional list comprising a list of max patterns in the input set and their corresponding support counts. 

For example, 

    data = [ 
      ['M', 'O', 'N', 'K', 'E', 'Y'], 
      ['D', 'O', 'N', 'K', 'E', 'Y'], 
      ['M', 'A', 'K', 'E'], 
      ['M', 'U', 'C', 'K', 'Y'], 
      ['C', 'O', 'O', 'K', 'I', 'E']
    ]

    apriori(data, 3)

will return the following:

    [[['E', 'K', 'O']], [3]]
