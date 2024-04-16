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


import matplotlib.pyplot as plt
import numpy as np

# Datos
profit_bodyplus100 = 1091
profit_bodyplus200 = 1411
price_bodyplus100 = 2400
price_bodyplus200 = 3500

# Función para calcular el beneficio total
def total_profit(quantity_bodyplus100, quantity_bodyplus200):
    return (profit_bodyplus100 * quantity_bodyplus100) + (profit_bodyplus200 * quantity_bodyplus200)

# Rangos de cantidad a producir para cada máquina
quantity_bodyplus100_values = np.arange(0, 100, 1)
quantity_bodyplus200_values = np.arange(0, 100, 1)

# Calcular beneficio total para cada combinación de cantidad
profits = np.array([[total_profit(q1, q2) for q1 in quantity_bodyplus100_values] for q2 in quantity_bodyplus200_values])

# Encontrar la cantidad que maximiza el beneficio total
max_profit_index = np.unravel_index(np.argmax(profits, axis=None), profits.shape)
max_profit_quantity_bodyplus100 = quantity_bodyplus100_values[max_profit_index[0]]
max_profit_quantity_bodyplus200 = quantity_bodyplus200_values[max_profit_index[1]]
max_profit = profits[max_profit_index]

# Crear el gráfico
plt.figure(figsize=(10, 6))
plt.contourf(quantity_bodyplus100_values, quantity_bodyplus200_values,
             profits, cmap='viridis')
plt.colorbar(label='Beneficio Total (USD)')
plt.xlabel('Cantidad de BodyPlus 100')
plt.ylabel('Cantidad de BodyPlus 200')
plt.title('Beneficio Total en función de la Cantidad de Producción')
plt.scatter(max_profit_quantity_bodyplus100, max_profit_quantity_bodyplus200,
            color='red', label=f'Máximo Beneficio: {max_profit:,.2f} USD')
plt.legend()
plt.grid(True)
plt.show()
