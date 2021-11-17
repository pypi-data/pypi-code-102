from .pt_translator import (
    call_function, define_function, print_structure, declare_variable
)


def from_pt(natural_text: str):
    if natural_text.split(' ')[0] == 'print':
        code = print_structure(natural_text)
    elif natural_text.split(' ')[0] == 'variável':
        code = declare_variable(natural_text)
    elif natural_text.split(' ')[0] == 'defina':
        code = define_function(natural_text)
    elif natural_text.split(' ')[0] == 'chame':
        code = call_function(natural_text)
    return code


def run(natural_text: str, language='pt-BR'):
    if language == 'pt-BR':
        code = from_pt(natural_text)
    return code


if __name__ == '__main__':
    code_line = run('chame this function parâmetros inteiro number string algo')
    print(code_line)
