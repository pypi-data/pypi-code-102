TYPES = {
    'string': 'str',
    'inteiro': 'int',
    'flutuante': 'float',
    'booleano': 'bool',
    'complexo': 'complex',
    'lista': 'list',
    'objeto': 'object'
}


def print_structure(natural_text: str):
    content = natural_text.split('print ')[1]
    return f"print('{content}')"


def declare_variable(natural_text: str):
    content = natural_text.split('variável ')[1]
    name, type_and_value = content.split('recebe ')
    name = name.strip()
    type_of, value = type_and_value.split(' ')
    type_of = TYPES[type_of]
    code = f"{name} = {type_of}('{value}')"
    return f"{code}"


def define_function(natural_text: str):
    content = natural_text.split('defina ')[1]
    if 'parâmetros' in content:
        types_of_parameters = []
        names_of_parameters = []
        function_name, parameters = content.split(' parâmetros ')
        function_name = function_name.strip().replace(' ', '_')
        for parameter in range(0, len(parameters.split(' '))):
            if parameter % 2 == 0:
                types_of_parameters.append(parameters.split(' ')[parameter])
            else:
                names_of_parameters.append(parameters.split(' ')[parameter])
        names_and_types = ''
        for counter in range(0, len(types_of_parameters)):
            type_of = TYPES[types_of_parameters[counter]]
            names_and_types += f"{names_of_parameters[counter]}: {type_of}, "
        names_and_types = names_and_types[:-2]
        code = f"def {function_name}({names_and_types}):"
    elif 'parâmetro' in content:
        function_name, parameter = content.split(' parâmetro ')
        function_name = function_name.strip().replace(' ', '_')
        type_of, parameter = parameter.strip().split(' ')
        type_of = TYPES[type_of]
        code = f"def {function_name}({parameter}: {type_of}):"
    else:
        function_name = content.strip().replace(' ', '_')
        code = f"def {function_name}():"
    return code


def call_function(natural_text: str):
    content = natural_text.split('chame ')[1]
    if 'parâmetros' in content:
        types_of_parameters = []
        names_of_parameters = []
        function_name, parameters = content.split(' parâmetros ')
        function_name = function_name.strip().replace(' ', '_')
        for parameter in range(0, len(parameters.split(' '))):
            if parameter % 2 == 0:
                types_of_parameters.append(parameters.split(' ')[parameter])
            else:
                names_of_parameters.append(parameters.split(' ')[parameter])
        names_and_types = ''
        for counter in range(0, len(types_of_parameters)):
            type_of = TYPES[types_of_parameters[counter]]
            names_and_types += f"{type_of}({names_of_parameters[counter]}), "
        names_and_types = names_and_types[:-2]
        code = f"{function_name}({names_and_types})"
    elif 'parâmetro' in content:
        function_name, parameter = content.split(' parâmetro ')
        function_name = function_name.strip().replace(' ', '_')
        type_of, parameter = parameter.strip().split(' ')
        type_of = TYPES[type_of]
        code = f"{function_name}({type_of}({parameter}))"
    else:
        function_name = content.strip().replace(' ', '_')
        code = f"{function_name}()"
    return code
