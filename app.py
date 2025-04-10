import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import re # Needed for stripping color codes in menu width calculation

# pip install supervenn  # Uncomment and run if you don't have supervenn
try:
    from supervenn import supervenn
    SUPERVENN_AVAILABLE = True
except ImportError:
    SUPERVENN_AVAILABLE = False
    print("Warning: 'supervenn' library not found. Visualization for 4-5 sets will be unavailable.")
    print("You can install it using: pip install supervenn")

# --- ANSI Color Codes ---
RESET = "\033[0m"
BOLD = "\033[1m"
# Basic Colors
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RED = "\033[91m" # Added Red for potential errors/warnings

# --- Plotting Color Palette ---
PALETTE = [
    '#FF9999', '#66B2FF', '#99FF99',  # Light Red, Light Blue, Light Green
    '#FFCC99', '#FFD700', '#B19CD9',  # Light Orange, Gold, Light Purple
    '#FFB6C1'                           # Light Pink (for 7th region in venn3)
]
HIGHLIGHT_INTERSECTION = '#FFD700' # Gold for intersection emphasis
HIGHLIGHT_DIFFERENCE = '#FF9999'   # Light Red for difference A-B
HIGHLIGHT_SYMM_DIFF_A = '#66B2FF'  # Light Blue for A part of symm diff
HIGHLIGHT_SYMM_DIFF_B = '#99FF99'  # Light Green for B part of symm diff
HIGHLIGHT_COMPLEMENT = '#D3D3D3'   # Light Grey for complement

# --- Helper Functions ---

def get_set_input(prompt):
    """Helper function to get set input from user."""
    while True:
        try:
            print(f"{CYAN}{prompt}{RESET}", end="") # Added color to prompt
            user_input = input().strip()
            if not user_input: # Handle empty input -> empty set
                return set()
            # Attempt to convert all elements to integers
            elements = set(map(int, user_input.split()))
            return elements
        except ValueError:
            print(f"{RED}Invalid input. Please enter space-separated integers only.{RESET}")
        except Exception as e:
            print(f"{RED}An unexpected error occurred: {e}{RESET}")


def union(sets):
    if not sets:
        return set()
    return set.union(*sets)

def intersection(sets):
    if not sets:
        return set()
    # Handle intersection of a single set
    if len(sets) == 1:
        return sets[0].copy()
    return set.intersection(*sets)

def difference(set_a, set_b):
    return set_a - set_b

def symmetric_difference(set_a, set_b):
    return set_a ^ set_b

def check_subset(set_a, set_b):
    return set_a.issubset(set_b)

def complement(universal, set_a):
    return universal - set_a

# --- Plotting Function ---

def plot_sets(sets, operation, result, set_indices=None):
    """Function to plot Venn diagrams with labels, highlighting, and enhanced styling."""
    num_sets_in_plot = len(sets)
    op = operation.lower()
    alpha = 0.6 # Transparency for fills

    # --- Check if plotting is feasible ---
    if num_sets_in_plot < 2:
        print(f"{YELLOW}⚠ Venn diagrams require at least 2 sets to plot.{RESET}")
        print(f"{operation} Result: {result}") # Still print result textually
        return
    if num_sets_in_plot > 3 and not SUPERVENN_AVAILABLE:
        print(f"{YELLOW}⚠ Supervenn library not available. Cannot visualize {num_sets_in_plot} sets.{RESET}")
        print(f"{operation} Result: {result}")
        return
    if num_sets_in_plot > 6:
        print(f"{YELLOW}⚠ Visualization might become complex or unsupported for {num_sets_in_plot} sets.{RESET}")
        print(f"{operation} Result: {result}")
        return

    # --- Proceed with Plotting ---
    plt.figure(figsize=(8, 8)) # Default size, might be overridden by supervenn

    # Determine default labels based on original indices if provided
    if set_indices:
        default_labels = [f"Set {i+1}" for i in set_indices]
    else:
        default_labels = [f"Set {i+1}" for i in range(num_sets_in_plot)]

    plot_title = f"{operation}: {result}" # Base title

    # --- Standard Venn (2 or 3 sets) ---
    if num_sets_in_plot == 2:
        a, b = sets
        subsets_data = (len(a - b), len(b - a), len(a & b))
        v = venn2(subsets=subsets_data, set_labels=default_labels, set_colors=(PALETTE[0], PALETTE[1]), alpha=alpha)

        region_ids = ['10', '01', '11']
        patches = {id_: v.get_patch_by_id(id_) for id_ in region_ids if v.get_patch_by_id(id_)}

        if patches.get('10'): patches['10'].set_color(PALETTE[0]); patches['10'].set_alpha(0.4)
        if patches.get('01'): patches['01'].set_color(PALETTE[1]); patches['01'].set_alpha(0.4)
        if patches.get('11'): patches['11'].set_color(PALETTE[3]); patches['11'].set_alpha(0.5)

        if v.get_label_by_id('10'): v.get_label_by_id('10').set_text(a - b if a-b else '')
        if v.get_label_by_id('01'): v.get_label_by_id('01').set_text(b - a if b-a else '')
        if v.get_label_by_id('11'): v.get_label_by_id('11').set_text(a & b if a&b else '')

        if op == "union":
            if patches.get('10'): patches['10'].set_color(PALETTE[0]); patches['10'].set_alpha(alpha)
            if patches.get('01'): patches['01'].set_color(PALETTE[1]); patches['01'].set_alpha(alpha)
            if patches.get('11'): patches['11'].set_color(PALETTE[3]); patches['11'].set_alpha(alpha)
            plot_title = f"Union (Highlighted): {result}"
        elif op == "intersection":
            if patches.get('11'): patches['11'].set_color(HIGHLIGHT_INTERSECTION); patches['11'].set_alpha(alpha+0.1)
            plot_title = f"Intersection (Highlighted): {result}"
        elif op == "difference":
            if patches.get('10'): patches['10'].set_color(HIGHLIGHT_DIFFERENCE); patches['10'].set_alpha(alpha)
            plot_title = f"Difference (Highlighted): {result}"
        elif op == "symmetric difference":
            if patches.get('10'): patches['10'].set_color(HIGHLIGHT_SYMM_DIFF_A); patches['10'].set_alpha(alpha)
            if patches.get('01'): patches['01'].set_color(HIGHLIGHT_SYMM_DIFF_B); patches['01'].set_alpha(alpha)
            plot_title = f"Symmetric Difference (Highlighted): {result}"

    elif num_sets_in_plot == 3:
        a, b, c = sets
        subsets_data = (
            len(a - b - c), len(b - a - c), len((a & b) - c), len(c - a - b),
            len((a & c) - b), len((b & c) - a), len(a & b & c)
        )
        v = venn3(subsets=subsets_data, set_labels=default_labels, set_colors=(PALETTE[0], PALETTE[1], PALETTE[2]), alpha=alpha)

        region_ids = ['100', '010', '110', '001', '101', '011', '111']
        patches = {id_: v.get_patch_by_id(id_) for id_ in region_ids if v.get_patch_by_id(id_)}

        color_map_default = {'100': PALETTE[0], '010': PALETTE[1], '001': PALETTE[2], '110': PALETTE[3], '101': PALETTE[4], '011': PALETTE[5], '111': PALETTE[6]}
        for id_, patch in patches.items():
            patch.set_color(color_map_default.get(id_, 'grey'))
            patch.set_alpha(0.4)

        if v.get_label_by_id('100'): v.get_label_by_id('100').set_text(a - b - c if a-b-c else '')
        if v.get_label_by_id('010'): v.get_label_by_id('010').set_text(b - a - c if b-a-c else '')
        if v.get_label_by_id('001'): v.get_label_by_id('001').set_text(c - a - b if c-a-b else '')
        if v.get_label_by_id('110'): v.get_label_by_id('110').set_text((a & b) - c if (a&b)-c else '')
        if v.get_label_by_id('101'): v.get_label_by_id('101').set_text((a & c) - b if (a&c)-b else '')
        if v.get_label_by_id('011'): v.get_label_by_id('011').set_text((b & c) - a if (b&c)-a else '')
        if v.get_label_by_id('111'): v.get_label_by_id('111').set_text(a & b & c if a&b&c else '')

        if op == "union":
            color_map_union = {'100': PALETTE[0], '010': PALETTE[1], '001': PALETTE[2], '110': PALETTE[3], '101': PALETTE[4], '011': PALETTE[5], '111': PALETTE[6]}
            for id_, patch in patches.items():
                patch.set_color(color_map_union.get(id_, 'grey'))
                patch.set_alpha(alpha)
            plot_title = f"Union (Highlighted): {result}"
        elif op == "intersection":
             if patches.get('111'): patches['111'].set_color(HIGHLIGHT_INTERSECTION); patches['111'].set_alpha(alpha+0.1)
             plot_title = f"Intersection (Highlighted): {result}"

    # --- Supervenn (4 to 6 sets) ---
    elif SUPERVENN_AVAILABLE and 4 <= num_sets_in_plot <= 6:
        print(f"{YELLOW}Generating Supervenn diagram (may take a moment)...{RESET}")
        try:
            set_labels = [f"Set_{i+1}" for i in range(len(sets))]  # Adjust labels to start from Set_1
            supervenn(sets, set_annotations=set_labels)
            result_str = str(result)
            max_title_len = 80 # Max chars for result in title before truncating
            if len(result_str) > max_title_len:
                 result_str = result_str[:max_title_len - 3] + "..." # Truncate long results

            # Create a title with operation and result on separate lines
            title_text = f"{operation.capitalize()}\nResult: {result_str}" # Capitalize op name
            plt.suptitle(title_text, fontsize=12) # Add result clearly in the super title

            # Adjust layout AFTER drawing and titling
            # Make top margin slightly larger to accommodate two-line title (e.g., 0.92 or 0.9)
            plt.tight_layout(rect=[0, 0.03, 1, 0.92])

        except Exception as e:
             print(f"{RED}Error generating Supervenn diagram: {e}{RESET}")
             print(f"{YELLOW}Displaying result textually.{RESET}")
             print(f"{operation} Result: {result}")
             plt.close() 
             return # Exit plotting function
        
    
    plt.title(plot_title)
    plt.show() # Show the plot for venn2/venn3/supervenn if successful

# --- Decorated Menu Function ---
def display_menu_unicode_color(sets, universal_set):
    """Displays the main menu with Unicode box characters and colors."""
    # --- Prepare menu content ---
    lines = []
    lines.append(f"{BOLD}{YELLOW}SET OPERATIONS MENU{RESET}") # Title
    lines.append("SEPARATOR") # Placeholder for separator logic
    lines.append(f"{CYAN}Defined Sets:{RESET}")
    lines.append(f"  {MAGENTA}Universal Set U:{RESET} {universal_set}")
    for i, s in enumerate(sets, start=1):
        # Ensure set string representation doesn't get too long for reasonable display
        set_str = str(s)
        if len(set_str) > 60: # Truncate long set strings for menu display
             set_str = set_str[:57] + "..."
        lines.append(f"  {MAGENTA}Set {i}:{RESET}           {set_str}")
    lines.append("SEPARATOR")
    lines.append(f"{CYAN}Options:{RESET}")
    lines.append(f"  {GREEN}1.{RESET} Show Sets Diagram")
    lines.append(f"  {GREEN}2.{RESET} Union (of all defined sets)")
    lines.append(f"  {GREEN}3.{RESET} Intersection (of all defined sets)")
    lines.append(f"  {GREEN}4.{RESET} Difference (Set A - Set B)")
    lines.append(f"  {GREEN}5.{RESET} Symmetric Difference (Set A Δ Set B)")
    lines.append(f"  {GREEN}6.{RESET} Check Subset (Set A ⊆ Set B)")
    lines.append(f"  {GREEN}7.{RESET} Complement (of a set w.r.t. U)")
    lines.append(f"  {GREEN}8.{RESET} Exit")

    # --- Calculate Width (Ignoring color codes) ---
    def get_text_length(text):
        # Remove ANSI codes for length calculation
        return len(re.sub(r'\033\[[0-9;]*m', '', text))

    max_len = 0
    for line in lines:
        if line != "SEPARATOR":
             max_len = max(max_len, get_text_length(line))

    padding = 4
    box_width = max_len + padding
    h_line = "─" * box_width

    # --- Print Box ---
    border_color = BLUE # Color for the box lines
    print(f"\n{border_color}┌{h_line}┐{RESET}")

    # Print Lines within the box
    left_pad_count = padding // 2
    left_pad = " " * left_pad_count

    for i, line in enumerate(lines):
        if line == "SEPARATOR":
             print(f"{border_color}├{h_line}┤{RESET}")
        else:
            # Calculate padding needed for this specific line
            line_len = get_text_length(line)
            # Ensure right_pad_count is not negative if line_len exceeds box_width somehow
            right_pad_count = max(0, box_width - (left_pad_count + line_len))
            right_pad = " " * right_pad_count
            # Special centering for the title
            if i == 0: # Title line
                 # Ensure title padding isn't negative
                 title_pad_left_count = max(0, (box_width - line_len) // 2)
                 title_pad_right_count = max(0, box_width - line_len - title_pad_left_count)
                 title_pad_left = " " * title_pad_left_count
                 title_pad_right = " " * title_pad_right_count
                 print(f"{border_color}│{RESET}{title_pad_left}{line}{title_pad_right}{border_color}│{RESET}")
            else:
                 print(f"{border_color}│{RESET}{left_pad}{line}{right_pad}{border_color}│{RESET}")

    print(f"{border_color}└{h_line}┘{RESET}")


# --- Main Program Logic ---

print(f"{BOLD}{YELLOW}--- Set Theory Visualizer ---{RESET}")

# User input for universal set
universal_set = get_set_input("Enter elements of the Universal Set U (space-separated integers): ")
# print(f"Universal Set U: {universal_set}") # Displayed in menu now

# User input for defining sets
while True:
    try:
        num_sets_input = input(f"{CYAN}Enter the number of sets you want to work with (e.g., 2,4 ..): {RESET}")
        num_sets = int(num_sets_input)
        if num_sets < 1:
             print(f"{RED}Please enter at least 1 set.{RESET}")
        elif num_sets > 6 and not SUPERVENN_AVAILABLE:
             print(f"{YELLOW}Warning: Visualization requires 'supervenn' for > 3 sets. Proceeding without graphs for {num_sets} sets.{RESET}")
             break
        elif num_sets > 6:
             print(f"{YELLOW}Warning: Visualization for {num_sets} sets can be complex. Proceeding with 'supervenn'.{RESET}")
             break
        else:
            break # Exit loop if valid number is entered
    except ValueError:
        print(f"{RED}Invalid input. Please enter an integer.{RESET}")

sets = []
for i in range(num_sets):
    sets.append(get_set_input(f"Enter elements of Set {i+1} (space-separated integers): "))

# --- Main Interaction Loop ---
while True:
    # Display the decorated menu
    display_menu_unicode_color(sets, universal_set)

    try:
        # Get user choice with styled prompt
        choice_input = input(f"Enter your choice (1-8):{BOLD}{GREEN} >> {RESET} ")
        choice = int(choice_input)

        # --- Input Validation Helper for Set Indices ---
        def get_valid_indices(num_required, op_name):
            if len(sets) < num_required:
                 print(f"{RED}Need at least {num_required} set(s) defined for {op_name}.{RESET}")
                 return None # Indicate failure

            while True:
                prompt = f"{CYAN}Enter set number{'s' if num_required > 1 else ''} for {op_name} (e.g., {'1 2' if num_required == 2 else '1'}): {RESET}"
                try:
                    indices_str = input(prompt).split()
                    if len(indices_str) != num_required:
                        print(f"{RED}Please enter exactly {num_required} space-separated number(s).{RESET}")
                        continue

                    indices = [int(s) - 1 for s in indices_str] # Convert to 0-based index

                    valid = True
                    for idx in indices:
                        if not (0 <= idx < len(sets)):
                            print(f"{RED}Invalid set number: {idx + 1}. Please choose between 1 and {len(sets)}.{RESET}")
                            valid = False
                            break
                    if valid:
                        return indices # Return list of 0-based indices

                except ValueError:
                    print(f"{RED}Invalid input. Please enter integer numbers only.{RESET}")

        # --- Menu Choice Handling ---
        if choice == 1:
            print(f"{YELLOW}Displaying defined sets diagram...{RESET}")
            if not sets: print(f"{RED}No sets defined.{RESET}"); continue
            plot_sets(sets, "All Sets Overview", "N/A - Showing set composition") # plot_sets handles checks

        elif choice == 2: # Union
            if not sets: print(f"{RED}No sets defined for Union.{RESET}"); continue
            result = union(sets)
            print(f"Union of all sets: {result}")
            plot_sets(sets, "Union", result)

        elif choice == 3: # Intersection
            if not sets: print(f"{RED}No sets defined for Intersection.{RESET}"); continue
            result = intersection(sets)
            print(f"Intersection of all sets: {result}")
            plot_sets(sets, "Intersection", result)

        elif choice == 4: # Difference
            indices = get_valid_indices(2, "Difference (A - B)")
            if indices:
                a_idx, b_idx = indices
                set_a, set_b = sets[a_idx], sets[b_idx]
                result = difference(set_a, set_b)
                print(f"Difference (Set {a_idx+1} - Set {b_idx+1}): {result}")
                # Only plot the two relevant sets for Difference
                plot_sets([set_a, set_b], "Difference", result, set_indices=[a_idx, b_idx])

        elif choice == 5: # Symmetric Difference
            indices = get_valid_indices(2, "Symmetric Difference (A Δ B)")
            if indices:
                 a_idx, b_idx = indices
                 set_a, set_b = sets[a_idx], sets[b_idx]
                 result = symmetric_difference(set_a, set_b)
                 print(f"Symmetric Difference (Set {a_idx+1} Δ Set {b_idx+1}): {result}")
                 # Only plot the two relevant sets
                 plot_sets([set_a, set_b], "Symmetric Difference", result, set_indices=[a_idx, b_idx])

        elif choice == 6: # Subset Check
             indices = get_valid_indices(2, "Subset Check (A ⊆ B)")
             if indices:
                 a_idx, b_idx = indices
                 set_a, set_b = sets[a_idx], sets[b_idx]
                 is_subset = check_subset(set_a, set_b)
                 print(f"Is Set {a_idx+1} a subset of Set {b_idx+1}? : {is_subset}")
                 # Only plot the two relevant sets
                 plot_sets([set_a, set_b], f"Subset Check: Set {a_idx+1} vs Set {b_idx+1}", f"Result: {is_subset}", set_indices=[a_idx, b_idx])

        elif choice == 7: # Complement
            indices = get_valid_indices(1, "Complement (U - A)")
            if indices:
                a_idx = indices[0]
                set_a = sets[a_idx]
                result = complement(universal_set, set_a)
                print(f"Complement of Set {a_idx+1} (U - Set {a_idx+1}): {result}")

                # Complement visualization uses venn2 directly, not plot_sets
                plt.figure(figsize=(7, 7))
                v = venn2([universal_set, set_a], set_labels=('Universal Set U', f'Set {a_idx+1}'))

                if v.get_label_by_id('10'): v.get_label_by_id('10').set_text(result if result else '')
                if v.get_label_by_id('01'): v.get_label_by_id('01').set_text('')
                if v.get_label_by_id('11'): v.get_label_by_id('11').set_text(set_a & universal_set if set_a & universal_set else '')

                patch_10 = v.get_patch_by_id('10')
                if patch_10:
                    patch_10.set_color(HIGHLIGHT_COMPLEMENT)
                    patch_10.set_alpha(0.7)

                patch_11 = v.get_patch_by_id('11')
                if patch_11:
                     patch_11.set_color(PALETTE[1])
                     patch_11.set_alpha(0.5)

                plt.title(f"Complement of Set {a_idx+1} = U - Set {a_idx+1}")
                plt.show()

        elif choice == 8: # Exit
            print(f"\n{YELLOW}Exiting...{RESET}")
            print(f"{YELLOW}Thank you for using the Set Theory Visualizer!{RESET}")
            plt.close('all')
            break
        else:
            print(f"{RED}Invalid choice. Please enter a number between 1 and 8.{RESET}")

    except ValueError:
        print(f"{RED}Invalid input. Please enter a number for the choice.{RESET}")
    except Exception as e:
        print(f"{RED}An unexpected error occurred: {e}{RESET}")
