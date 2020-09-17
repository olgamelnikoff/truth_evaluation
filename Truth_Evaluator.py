"""
Overview:
1) The program first takes a number of propositional variables (P1, P2... Pn) as an input.
2) It then takes a statement involving these variables as an input.
3) The statement may include logical operators NOT, AND, OR, IMPLIES and EQUAL, as well as parentheses.
4) The program parses the statement and outputs "True" if the given assignment satisfies the sentence.
It outputs "False" if it does not. 
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
    if ('EQUALS' in expression and 'IMPLIES' in expression):
        connective_index = min(expression.index('EQUALS'), expression.index('IMPLIES'))
    elif ('EQUALS' in expression):
        connective_index = expression.index('EQUALS')
    else:
        connective_index = expression.index('IMPLIES')

    connective = expression[connective_index]

    left_value = expression[connective_index - 1]
    right_value = expression[connective_index + 1]

    if (connective == 'EQUALS'):
        if (left_value == right_value):
            expression[connective_index - 1] = 'TRUE'
        else:
            expression[connective_index - 1] = 'FALSE'
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

#Class for an object containing the name of the variable (P1, P2, etc.) and its value (True or False)
class propositionalVariables:
    def __init__(self, name, value):  
        self.name = name  
        self.value = value

#Parsing the propositional values entered by the user
def parsing_first_input (values):

    #parsing the input and creating an array of values
    val_list = []

    for i in range(len(values)):
        if (values[i] == '1' or values[i] == '0'):
            val_list.append(values[i])
        else:
            print('Unauthorized input. Exiting the program.')
            exit()
            
    #creating a list of objects of propositionalVariables class
    objects_list = []
    
    for i in range(len(val_list)):
        objects_list.append(propositionalVariables(('P' + str(i + 1)), val_list[i]))    
    
    return objects_list
    
#Parsing the propositional sentence entered by the user
def parsing_second_input (prop_var_list, statement):

    #splitting the input into values
    statement = statement.split()

    for i in range(len(prop_var_list)):
        while (prop_var_list[i].name in statement):
            ind = statement.index(prop_var_list[i].name)
            
            if (prop_var_list[i].value == '1'):
                statement[ind] = 'TRUE'
            else:
                statement[ind] = 'FALSE'
                
    return statement

# main
print('Please enter truth values for P1, P2, P3')
print ('by entering 1 for True and 0 for False without any spaces.')
print ('Important: The only permitted input is 0 or 1.')
print('If you enter some other input,')
print ('such as spaces or commas, the program will exit.')
print ('The number of values that you may enter is unlimited.')

truthAssignment = input()

truthAssignment = parsing_first_input(truthAssignment)

print('Please enter a sentence using P1 through P' + str(len(truthAssignment)))
print ('as well as True and False as variables.')
print ('Please use NOT, AND, OR, IMPLIES or EQUALS as operators. ')
print ('Please also use parenthesis where necessary')
print ('and use whitespaces between variables and operators.')
statement = input()

statement = parsing_second_input(truthAssignment, statement)

output = parsing_outside_parentheses(statement)

print(output)
