# freq_patterns

Author: Stephen Gass
Date: 2/28/21

This python package is an implementation of two frequent pattern mining algorithms: Apriori and FP-Growth. Import and use in your python3 code.

Both functions take a list of transactions and a minimum support count as inputs and return a list object comprising a list of max patterns and their corresponding support counts. 

For example, 

    data = [ 
      ['M', 'O', 'N', 'K', 'E', 'Y'], 
      ['D', 'O', 'N', 'K', 'E', 'Y'], 
      ['M', 'A', 'K', 'E'], 
      ['M', 'U', 'C', 'K', 'Y'], 
      ['C', 'O', 'O', 'K', 'I', 'E']
    ]

    apriori(data, 3)

will return the following list object:

    [[['E', 'K', 'O']], [3]]
