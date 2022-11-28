import math

lead_density = 11.29 # Grams per cm^3
pla_density = 1.25

token_weight = 5.04

sheet_thickness = 1.5875

plastic_volume = math.pi * ((40/2) ** 2) * 3.5 / 1000
lead_volume = math.pi * ((38/2)** 2) * sheet_thickness /1000


net_plastic_volume = plastic_volume-lead_volume

print(net_plastic_volume)

print(plastic_volume * pla_density,  lead_volume * lead_density)
print(lead_volume/1000 * lead_density, plastic_volume/1000 * pla_density)

# print(plastic_volume)
