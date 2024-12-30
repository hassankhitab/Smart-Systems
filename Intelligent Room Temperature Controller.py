import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import messagebox

# Step 1: Define fuzzy variables
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')  # Temperature in °C
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')        # Humidity in %
heater = ctrl.Consequent(np.arange(0, 101, 1), 'heater')            # Heater level in %

# Step 2: Define membership functions
# Temperature
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['warm'] = fuzz.trimf(temperature.universe, [15, 25, 35])
temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 40])

# Humidity
humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 50])
humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['high'] = fuzz.trimf(humidity.universe, [60, 100, 100])

# Heater
heater['low'] = fuzz.trimf(heater.universe, [0, 0, 50])
heater['medium'] = fuzz.trimf(heater.universe, [30, 50, 70])
heater['high'] = fuzz.trimf(heater.universe, [60, 100, 100])

# Step 3: Define fuzzy rules
rule1 = ctrl.Rule(temperature['cold'] & humidity['low'], heater['high'])
rule2 = ctrl.Rule(temperature['cold'] & humidity['medium'], heater['medium'])
rule3 = ctrl.Rule(temperature['warm'], heater['low'])
rule4 = ctrl.Rule(temperature['hot'], heater['low'])

# Step 4: Build the control system
heater_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
heater_simulation = ctrl.ControlSystemSimulation(heater_ctrl)

# Step 5: GUI Implementation
def calculate_heater_level():
    try:
        temp = float(temp_entry.get())
        hum = float(hum_entry.get())
        
        if not (0 <= temp <= 40):
            raise ValueError("Temperature should be between 0 and 40°C")
        if not (0 <= hum <= 100):
            raise ValueError("Humidity should be between 0 and 100%")
        
        # Run fuzzy logic system
        heater_simulation.input['temperature'] = temp
        heater_simulation.input['humidity'] = hum
        heater_simulation.compute()
        heater_level = heater_simulation.output['heater']
        
        # Display result
        result_label.config(text=f"Heater Level: {heater_level:.2f}%")
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create GUI window
root = tk.Tk()
root.title("Intelligent Room Temperature Controller")
root.geometry("400x300")

# Add labels and entry boxes
tk.Label(root, text="Room Temperature (°C):").pack(pady=5)
temp_entry = tk.Entry(root)
temp_entry.pack(pady=5)

tk.Label(root, text="Humidity (%):").pack(pady=5)
hum_entry = tk.Entry(root)
hum_entry.pack(pady=5)

# Add a calculate button
calc_button = tk.Button(root, text="Calculate Heater Level", command=calculate_heater_level)
calc_button.pack(pady=20)

# Add a result label
result_label = tk.Label(root, text="Heater Level: --%", font=("Helvetica", 14))
result_label.pack(pady=10)

# Run the GUI loop
root.mainloop()
