"""
Overview:
1. The program first  takes a statement involving variables P1, P2... as an input.
2. It then creates a truth table for this statement
3. Finally, the program determines whether the statement is a tautology, contradiction or contingency.
"""

# LEVEL 1: PARSING LOGICAL OPERATIONS

#NOT:

def parsing_not(variable):
    pos_minus = variable.index('NOT')
    if (variable[pos_minus + 1] == 'TRUE'):
        variable[pos_minus + 1] = 'FALSE'
    else:
        variable[pos_minus + 1] = 'TRUE'
    del variable[pos_minus]
    return variable

#AND and OR:

def parsing_and_or(expression):
    # parsing until the first connective is reached.
    #Then two variables around it are identified.

    if ('AND' in expression and 'OR' in expression):
        connective_index = min(expression.index('AND'), expression.index('OR'))
    elif ('AND' in expression):
        connective_index = expression.index('AND')
    else:
        connective_index = expression.index('OR')

    connective = expression[connective_index]

    left_value = expression [connective_index - 1]
    right_value = expression [connective_index + 1]
    left_value_boolean = ('TRUE' in left_value)
    right_value_boolean = ('TRUE' in right_value)

    if (connective == 'AND'):
        output = left_value_boolean and right_value_boolean
    elif (connective == 'OR'):
        output = left_value_boolean or right_value_boolean
    else:
        print("Unrecognized connective: ", connective)
        exit()
    
    if (output):
        expression[connective_index - 1] = 'TRUE'
    else:
        expression[connective_index - 1] = 'FALSE'
    del expression[connective_index : connective_index + 2]

    return expression

#Implication and Equality:

def parsing_implies_equal(expression):
    if ('EQALS' in expression and 'IMPLIES' in expression):
        connective_index = min(expression.index('EQALS'), expression.index('IMPLIES'))
    elif ('EQALS' in expression):
        connective_index = expression.index('EQALS')
    else:
        connective_index = expression.index('IMPLIES')

    connective = expression[connective_index]

    left_value = expression[connective_index - 1]
    right_value = expression[connective_index + 1]

    if (connective == 'EQALS'):
        if (left_value == right_value):
            expression[connective_index - 1] = 'TRUE'
            print(expression[connective_index - 1])
        else:
            expression[connective_index - 1] = 'FALSE'
            print(expression[connective_index - 1])
    elif (connective == 'IMPLIES'):
        if (left_value == 'TRUE' and right_value == 'FALSE'):
            expression[connective_index - 1] = 'FALSE'
        else:
            expression[connective_index - 1] = 'TRUE'
    else:
        print("Unrecognized connective: ", connective)
        exit()

    del expression[connective_index : connective_index + 2]

    return expression


#LEVEL 2: PARSING INSIDE PARENTHESES:

def parsing_inside_parentheses(expression):

    if (len(expression) == 1):  # we are done
        return expression
    
    #processing NOT:
    while ('NOT' in expression):
        expression = parsing_not(expression)

    #processing AND and OR:
    while (('AND' in expression) or ('OR' in expression)):
        expression = parsing_and_or(expression)

    #processing Implication and Equality:
    while (('EQUALS' in expression) or ('IMPLIES' in expression)):
        expression = parsing_implies_equal(expression)
    
    return expression


#LEVEL 3: PARSING OUTSIDE PARENTHESES

def parsing_outside_parentheses (expression):

    #parsing until the first closing parenthesis is reached
    #finding the opening parenthesis preceding the closing one
    #parsing what is inside
    #repeat until no parentheses are left

    while (')' in expression):
        closing_parenthesis = expression.index(')')
        opening_parenthesis = closing_parenthesis
        while (expression[opening_parenthesis] != '('):
            opening_parenthesis -= 1
            
        statement_inside = expression [opening_parenthesis + 1 : closing_parenthesis]
    
        expression[opening_parenthesis] = parsing_inside_parentheses(statement_inside)[0]
        
        del expression[opening_parenthesis + 1 : closing_parenthesis + 1]

    return parsing_inside_parentheses(expression)

#LEVEL 4: MANIPULATING THE USER INPUT

#Class for an object containing the name of the variable (P1, P2, etc.) and its value (True or False)
class propositionalVariables:
    def __init__(self, name, value):  
        self.name = name  
        self.value = value
        
#Parsing the propositional values entered by the user
def get_statement (statement):

    #splitting the input into values
    statement = statement.split()
    
    return statement

#Getting the number of variables in the sentence
def get_count (values):

    #parsing the input and creating an array of values
    val_list = []

    for i in range(len(values)):
        if (('P' in str(values[i])) & (values[i] not in val_list)
            & (values[i] != 'IMPLIES')):
            val_list.append(values[i])

    count = len(val_list)

    return count
    

#LEVEL 5: TRUTH TABLE CONSTRUCTION

def truth_table_processing (count, statement):

    #The number of rows is determined.
    row_number = 2 ** count
    
    truth_table_list = []

    for i in range(row_number):
        #Converting the current number of row into a binary number
        #Padding the binary number with as many 0-s as needed
        current_number_int = bin(i)[2:].zfill(row_number)

        #Reversing the current number
        current_number_string = str(current_number_int)
        current_number_string_length = len(current_number_string)
        current_number_sliced_string = current_number_string[current_number_string_length::-1]
        
        integer_list = []
        objects_list = []
        
        #Putting all the values to a list
        for k in range (count):
            integer_list.append(current_number_sliced_string[k])
            
        #Creating a list of objects.
        #Each object has a name (e.g., P1) and a value (e.g., 0).
        for l in range(count):
            objects_list.append(propositionalVariables(('P' + str(l + 1)), integer_list[l]))
            print(objects_list[l].name, ' = ', objects_list[l].value)

        #Converting all 0-s and 1-s to "True" or "False"    
        this_statement = transform(objects_list, statement)

        #Parsing the statement to get the final value for the row 
        this_output = parsing_outside_parentheses(this_statement)

        print('The final truth value for row ', i, ' is ', this_output)

        #Appending the row value to the final list of truth values
        truth_table_list.append(this_output)

    return truth_table_list

#A method to convert all 0-s and 1-s to "True" or "False" 
def transform (objects_list, statement):
    #Processing this row and outputting its value.
    this_statement = statement.copy()
    for j in range (len(objects_list)):
        while (objects_list[j].name in this_statement):
            ind = this_statement.index(objects_list[j].name)
    
            if (objects_list[j].value == '1'):
                this_statement[ind] = 'TRUE'

            else:
                this_statement[ind] = 'FALSE'
                
    return this_statement

#Method to determine if all the row values are the same
def all_same (truth_table_list):
    first = truth_table_list[0]
    for i in range(len(truth_table_list)):
        if (truth_table_list[i] != first):
            return False
    return True

#Method to determine if this is a Tautology, Contradiction or Contingency
def category (truth_table_list):

    #Using method all_same above
    all_same_boolean = all_same (truth_table_list)
    
    #If all the values in the list are the same, it is either Tautology or Contradiction
    if (all_same_boolean == True):
        if (truth_table_list[0] == ['TRUE']):
                print('Tautology')
        else:
                print('Contradiction')
    else:
        print('Contingency')

# main
print('Please enter a sentence using P1 through Pn, as well as True and False as variables.')
print ('Please use NOT, AND, OR, IMPLIES or EQALS as operators. ')
print ('Please also use parenthesis where necessary and use whitespaces between variables and operators.')
statement = input()
statement = get_statement (statement)
variables_count = get_count(statement)
output = truth_table_processing (variables_count, statement)
output = category(output)
