# цикл по словарям
zoo_pet_mass = {
    'lion': 300,
    'skunk': 5,
    'elephant': 5000,
    'horse': 400,
}
total_mass = 0
for mass in zoo_pet_mass.values():
    print( mass)
    total_mass += mass
print('Общая масса животных', total_mass)
