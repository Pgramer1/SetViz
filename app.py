import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
from supervenn import supervenn  

def get_set_input(prompt):
    """Helper function to get set input from user."""
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

def plot_sets(sets, operation, result):
    """Function to plot Venn diagrams with labels."""
    plt.figure(figsize=(7, 7))

    if len(sets) == 2:
        labels = ["Set 1", "Set 2"]
        v = venn2(subsets=sets, set_labels=labels)

        # Add set elements in each region
        v.get_label_by_id("10").set_text(sets[0] - sets[1]) if v.get_label_by_id("10") else None
        v.get_label_by_id("01").set_text(sets[1] - sets[0]) if v.get_label_by_id("01") else None
        v.get_label_by_id("11").set_text(sets[0] & sets[1]) if v.get_label_by_id("11") else None

    elif len(sets) == 3:
        labels = ["Set 1", "Set 2", "Set 3"]
        v = venn3(subsets=sets, set_labels=labels)

        # Add set elements in each region
        v.get_label_by_id("100").set_text(sets[0] - sets[1] - sets[2]) if v.get_label_by_id("100") else None
        v.get_label_by_id("010").set_text(sets[1] - sets[0] - sets[2]) if v.get_label_by_id("010") else None
        v.get_label_by_id("001").set_text(sets[2] - sets[0] - sets[1]) if v.get_label_by_id("001") else None
        v.get_label_by_id("110").set_text((sets[0] & sets[1]) - sets[2]) if v.get_label_by_id("110") else None
        v.get_label_by_id("101").set_text((sets[0] & sets[2]) - sets[1]) if v.get_label_by_id("101") else None
        v.get_label_by_id("011").set_text((sets[1] & sets[2]) - sets[0]) if v.get_label_by_id("011") else None
        v.get_label_by_id("111").set_text(sets[0] & sets[1] & sets[2]) if v.get_label_by_id("111") else None

    elif 4 <= len(sets) <= 5:
        set_labels = [f"Set_{i+1}" for i in range(len(sets))]  # Adjust labels to start from Set_1
        supervenn(sets, set_annotations=set_labels)
        
    else:
        print("⚠ Visualization not supported for more sets in Venn diagrams.")
        return

    plt.title(f"{operation}: {result}")
    plt.show()

# User input for universal set
universal_set = get_set_input("Enter elements of the universal set (space-separated): ")

# User input for defining sets
num_sets = int(input("Enter the number of sets (2-3): "))
sets = [get_set_input(f"Enter elements of set {i+1} (space-separated): ") for i in range(num_sets)]

while True:
    print(f"\n{5*'--'} SET OPERATIONS MENU {5*'--'}\n")
    print("1. Show all sets")
    print("2. Union")
    print("3. Intersection")
    print("4. Difference of sets")
    print("5. Symmetric Difference")
    print("6. Check Subset Relation")
    print("7. Complement")
    print("8. Exit")
    
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        print("Sets:")
        for i, s in enumerate(sets, start=1):
            print(f"Set {i}: {s}")
        if len(sets) == 2:
            plt.figure(figsize=(6, 6))
            venn2(sets, set_labels=["Set 1", "Set 2"])
            plt.title("All Sets")
            plt.show()
        elif len(sets) == 3:
            plt.figure(figsize=(6, 6))
            venn3(sets, set_labels=["Set 1", "Set 2", "Set 3"])
            plt.title("All Sets")
            plt.show()
        elif 4 <= len(sets) <= 5:
            set_labels = [f"Set_{i+1}" for i in range(len(sets))]
            supervenn(sets, set_annotations=set_labels)
            plt.title("All Sets")
            plt.show()
        else:
            print("⚠ Visualization not supported for more sets.")
    elif choice == 2:
        result = union(sets)
        print("Union of all sets:", result)
        plot_sets(sets, "Union", result)
        
    elif choice == 3:
        result = intersection(sets)
        print("Intersection of all sets:", result)
        plot_sets(sets, "Intersection", result)
        
    elif choice == 4:
        a, b = map(int, input("Enter set numbers (1 2 ..) for difference: ").split())
        result = difference(sets[a-1], sets[b-1])
        print(f"Difference (Set {a} - Set {b}):", result)
        plot_sets([sets[a-1], sets[b-1]], "Difference", result)
        
    elif choice == 5:
        a, b = map(int, input("Enter set numbers (1 2 ..) for symmetric difference: ").split())
        result = symmetric_difference(sets[a-1], sets[b-1])
        print(f"Symmetric Difference (Set {a} Δ Set {b}):", result)
        plot_sets([sets[a-1], sets[b-1]], "Symmetric Difference", result)
        
    elif choice == 6:
        a, b = map(int, input("Enter set numbers (1 2 ..) to check subset: ").split())
        result = check_subset(sets[a-1], sets[b-1])
        print(f"Set {a} is a subset of Set {b}: {result}")

        # Show Venn diagram only if subset relation holds
        if result:
            plot_sets([sets[a-1], sets[b-1]], "Subset Relation", sets[a-1])

    elif choice == 7:
        a = int(input("Enter set number for complement: "))
        result = complement(universal_set, sets[a-1])
        print(f"Complement of Set {a} relative to Universal Set:", result)

        plt.figure(figsize=(6, 6))
        v = venn2([universal_set, sets[a-1]], set_labels=("Universal", f"Set {a}"))
        
        # Highlight complement area (elements in universal but not in set A)
        if result:
            v.get_patch_by_id("10").set_color('red')

        v.get_label_by_id("10").set_text(result) if v.get_label_by_id("10") else None
        v.get_label_by_id("01").set_text(sets[a-1]) if v.get_label_by_id("01") else None

        plt.title(f"Complement of Set {a}")
        plt.show()
        
    elif choice == 8:
        print("\nExiting...")
        print("Thank you for using the Set Theory Visualizer!")
        plt.close('all')
        break
    else:
        print("Invalid choice, please try again.")
