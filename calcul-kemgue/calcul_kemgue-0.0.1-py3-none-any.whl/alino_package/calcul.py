
from typing import List
import numpy as np

def add_one(number):
    return number + 1

def addition(operande1: int, operande2: int)-> int :
    return operande1 + operande2

def soustraction(operande1: int, operande2: int)-> int :
    return operande1 - operande2

def multiplication(operande1: int, operande2: int)-> int :
    return operande1 * operande2

def division(operande1: int, operande2: int)-> float :
    return operande1 / operande2

def somme_liste(liste: List[int]) -> int:
    sum=0
    for v in liste:
        sum+=v
    return sum

def somme_liste_array(liste1: List[int],liste2: List[int]) -> List[int]:

    arr1 = np.array(liste1)
    arr2 = np.array(liste2)
    sum_array=np.add(arr1,arr2)

    return np.ndarray.tolist(sum_array)