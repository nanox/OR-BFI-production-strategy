#!/usr/bin/env python

"""
Universidad Internacional de la Rioja
Programa: Ingenieria Informatica
Catedra: Investigacion de Operaciones
Caso: Estrategia de Produccion
"""
__author__ = "Jose Leonardo Alvarez Lopez"
__contact__ = "joseleonardo.alvarez696@comunidadunir.net"
__copyright__ = "Copyright 2024, UNIR"
__credits__ = ["Fundación Universitaria UNIR Colombia"]
__date__ = "2024/04/15"
__email__ = "jalvarez82@gmail.com"
__license__ = "Apache License 2.0"
__maintainer__ = "nanox"
__status__ = "stable"
__version__ = "1.0.0"


from pulp import *

# Crear el problema de maximización
prob = LpProblem("Maximize_Profit", LpMaximize)

# Variables de decisión
quantity = LpVariable.dicts("Quantity", ['BodyPlus100', 'BodyPlus200'],
                            lowBound=0, cat='Integer')

# Parámetros
profit = {'BodyPlus100': 1091, 'BodyPlus200': 1411}
price = {'BodyPlus100': 2400, 'BodyPlus200': 3500}
required_resources = {
    'BodyPlus100': {'machining': 8, 'painting': 5, 'assembly': 2},
    'BodyPlus200': {'machining': 12, 'painting': 10, 'assembly': 2}
}
available_resources = {'machining': 600, 'painting': 450, 'assembly': 140}
min_bodyplus200_percentage = 0.25

# Función objetivo
prob += lpSum(profit[m] * quantity[m] for m in quantity)

# Restricciones de recursos
for resource in available_resources:
    prob += lpSum(required_resources[m][resource] *
                  quantity[m] for m in quantity) <= available_resources[resource]

# Restricción mínima de BodyPlus200
prob += quantity['BodyPlus200'] >= min_bodyplus200_percentage * lpSum(quantity[m] for m in quantity)

# Resolver el problema
prob.solve()

# Mostrar resultados
print('================= Solución con PuLP =================\n')
print("Cantidad óptima a producir de cada máquina: \n")
for m in quantity:
    print(f"{m}: {value(quantity[m])}")

print(f"\nBeneficio total óptimo: $ {value(prob.objective):,.2f} usd")
