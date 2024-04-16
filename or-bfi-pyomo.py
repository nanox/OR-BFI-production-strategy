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


from pyomo.environ import *

# Crear una instancia del modelo de optimización
model = ConcreteModel()

# Conjuntos de maquinas
model.MACHINES = Set(initialize=['BodyPlus100', 'BodyPlus200'])

# Parámetros
model.PROFIT = Param(model.MACHINES, initialize={'BodyPlus100': 1091, 'BodyPlus200': 1411})
model.PRICE = Param(model.MACHINES, initialize={'BodyPlus100': 2400, 'BodyPlus200': 3500})

model.REQUIRED_RESOURCES = Param(model.MACHINES, initialize={
    'BodyPlus100': {'machining': 8, 'painting': 5, 'assembly': 2},
    'BodyPlus200': {'machining': 12, 'painting': 10, 'assembly': 2}
})

model.AVAILABLE_RESOURCES = {'machining': 600, 'painting': 450, 'assembly': 140}

model.MIN_BODYPLUS200_PERCENTAGE = 0.25

# Variables de decisión
model.quantity = Var(model.MACHINES, within=NonNegativeIntegers)

# Función objetivo
def total_profit(model):
    return sum(model.PROFIT[m] * model.quantity[m] for m in model.MACHINES)

model.total_profit = Objective(rule=total_profit, sense=maximize)

# Restricciones de recursos
def resource_constraint_rule(model, resource):
    return sum(model.REQUIRED_RESOURCES[m][resource] *
               model.quantity[m] for m in model.MACHINES) <= model.AVAILABLE_RESOURCES[resource]

model.resource_constraint = Constraint(model.AVAILABLE_RESOURCES.keys(),
                                       rule=resource_constraint_rule)

# Restricción mínima de BodyPlus200
def min_bodyplus200_constraint_rule(model):
    return model.quantity['BodyPlus200'] >= model.MIN_BODYPLUS200_PERCENTAGE * sum(model.quantity[m] for m in model.MACHINES)

model.min_bodyplus200_constraint = Constraint(rule=min_bodyplus200_constraint_rule)

# Resolver el modelo
solver = SolverFactory('glpk', executable='/usr/bin/glpsol')
solver.solve(model)

# Verificar el modelo
model.pprint()
print()
solver.solve(model).write()

# Mostrar resultados
print('\n\n================= Solución Pyomo GLPK =================\n')
print("Cantidad óptima a producir de cada máquina: \n")

for m in model.MACHINES:
    print(f"{m}: {model.quantity[m].value}")

print(f"\nBeneficio total óptimo: : $ {model.total_profit():,.2f} usd\n")
print('=======================================================\n')
