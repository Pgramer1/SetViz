import matplotlib.pyplot as plt
import matplotlib_venn as venn
import pandas as pd
import supervenn

def get_set_input(prompt):
    return set(map(int, input(prompt).split()))

def union(sets):
    return set.union(*sets)

def intersection(sets):
    return set.intersection(*sets)

def difference(set_a, set_b):
    return set_a - set_b

def symmetric_difference(set_a, set_b):
    return set_a ^ set_b

def check_subset(set_a, set_b):
    return set_a.issubset(set_b)

def complement(universal, set_a):
    return universal - set_a

def plot_venn(sets, operation, result):
    plt.figure(figsize=(6, 6))
    if len(sets) == 2:
        venn.venn2(sets, set_labels=[f"Set 1: {sets[0]}", f"Set 2: {sets[1]}"])
    elif len(sets) == 3:
        venn.venn3(sets, set_labels=[f"Set 1: {sets[0]}", f"Set 2: {sets[1]}", f"Set 3: {sets[2]}"])
    elif len(sets) > 3:
        print("More than 3 sets detected. Using Supervenn plot.")
        plot_supervenn(sets, operation)
        return
    plt.title(f"{operation}: {result}")
    plt.show()

def plot_supervenn(sets, operation):
    labels = [f"Set {i+1}" for i in range(len(sets))]
    supervenn.supervenn(sets, labels)
    plt.title(f"{operation} (Supervenn Diagram)")
    plt.show()

# User input for universal set
universal_set = get_set_input("Enter elements of the universal set (space-separated): ")

# User input for defining sets
num_sets = int(input("Enter the number of sets: "))
sets = []
for i in range(num_sets):
    sets.append(get_set_input(f"Enter elements of set {i+1} (space-separated): "))

while True:
    print("\nSet Operations Menu:")
    print("1. Union")
    print("2. Intersection")
    print("3. Difference of sets")
    print("4. Symmetric Difference")
    print("5. Check Subset Relation")
    print("6. Complement")
    print("7. Exit")
    
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        result = union(sets)
        print("Union of all sets:", result)
        plot_venn(sets, "Union", result)
    elif choice == 2:
        result = intersection(sets)
        print("Intersection of all sets:", result)
        plot_venn(sets, "Intersection", result)
    elif choice == 3:
        a, b = map(int, input("Enter set numbers (1 2 ..) for difference: ").split())
        result = difference(sets[a-1], sets[b-1])
        print(f"Difference (Set {a} - Set {b}):", result)
        plot_venn([sets[a-1], sets[b-1]], "Difference", result)
    elif choice == 4:
        a, b = map(int, input("Enter set numbers (1 2 ..) for symmetric difference: ").split())
        result = symmetric_difference(sets[a-1], sets[b-1])
        print(f"Symmetric Difference (Set {a} Δ Set {b}):", result)
        plot_venn([sets[a-1], sets[b-1]], "Symmetric Difference", result)
    elif choice == 5:
        a, b = map(int, input("Enter set numbers (1 2 ..) to check subset: ").split())
        result = check_subset(sets[a-1], sets[b-1])
        print(f"Set {a} is a subset of Set {b}:", result)
        plot_venn([sets[a-1], sets[b-1]], "Subset Relation", result)
    elif choice == 6:
        a = int(input("Enter set number for complement: "))
        result = complement(universal_set, sets[a-1])
        print(f"Complement of Set {a} relative to Universal Set:", result)
        plot_venn([universal_set, sets[a-1]], "Complement", result)
    elif choice == 7:
        print("Exiting...")
        break
    else:
        print("Invalid choice, please try again.")
