# SetViz : A set operation visualizer 📊

A command-line tool written in Python to perform fundamental set theory operations and visualize the relationships between sets using Venn diagrams (`matplotlib-venn`) and Supervenn diagrams (`supervenn`).

## Description

This interactive script allows users to:
1.  Define a Universal Set and multiple working sets (up to 6 for full visualization).
2.  Perform common set operations:
    * Union
    * Intersection
    * Difference
    * Symmetric Difference
    * Subset Check
    * Complement (relative to the Universal Set)
3.  Visualize the sets and operation results graphically:
    * For 2 or 3 sets, it uses `matplotlib-venn` to generate classic Venn diagrams, labeling regions with elements and highlighting the result of the selected operation with distinct colors.
    * For 4 to 6 sets, it utilizes the `supervenn` library to create a matrix-based visualization showing the structure and size of intersections between the sets. The overall operation result is displayed in the plot title.
4.  Interact through a colorful, formatted command-line menu using Unicode box characters and ANSI colors for enhanced readability (requires a compatible terminal).

## Features ✨

* **Interactive CLI:** Easy-to-use menu-driven interface.
* **Multiple Set Operations:** Covers essential set theory functions.
* **Dual Visualization:** Automatically chooses between `matplotlib-venn` and `supervenn` based on the number of sets.
* **Element Labeling:** Shows elements within regions for 2/3-set Venn diagrams.
* **Result Highlighting:** Clearly highlights the resulting areas/sets for operations in `matplotlib-venn`.
* **Supervenn Integration:** Visualizes complex intersections for 4-6 sets.
* **Operation Result Display:** Shows the calculated result set both textually and in the plot title.
* **Enhanced Menu:** Uses Unicode characters and ANSI colors for a visually appealing menu (terminal permitting).
* **Robust Input:** Handles invalid input gracefully.
* **Customizable Colors:** Plotting colors defined in easily modifiable palettes within the code.


## Requirements 📋

* **Python:** Version 3.x
* **Libraries:**
    * `matplotlib`
    * `matplotlib-venn`
    * `supervenn` (Optional, but required for visualizing 4-6 sets)
    * `re` (Built-in Python module)

## Installation ⚙️

1.  **Clone the repository or download the script.** (Assuming you save the code as `set_visualizer.py`)
2.  **Install required libraries using pip:**
    ```bash
    pip install matplotlib matplotlib-venn supervenn
    ```
    * If you only plan to work with 2 or 3 sets, you can omit `supervenn`:
        ```bash
        pip install matplotlib matplotlib-venn
        ```
        *(Note: The script will warn you if `supervenn` is needed but not found).*

## Usage 🚀

1.  **Run the script** from your terminal:
    ```bash
    python set_visualizer.py
    ```
2.  **Enter Universal Set:** When prompted, enter the elements of the universal set, separated by spaces (e.g., `1 2 3 4 5 6 7 8 9 10`). Press Enter.
3.  **Enter Number of Sets:** Enter the total number of working sets you want to define (e.g., `2`, `3`, `4`). Press Enter.
4.  **Enter Set Elements:** For each set, enter its elements separated by spaces when prompted (e.g., `1 2 3 4`). Press Enter after each set definition.
5.  **Interact with the Menu:**
    * The script will display a decorated menu listing the defined sets and available operations.
    * Enter the number corresponding to your desired action (1-8) and press Enter.
    * Follow any subsequent prompts (e.g., entering the numbers of the sets for Difference or Subset Check).
6.  **View Results:**
    * The calculated result set will be printed to the console.
    * A plot window (Matplotlib) will open, displaying the relevant Venn or Supervenn diagram.
7.  **Exit:** Choose option `8` from the menu to close the application.

## Code Overview 🔍

* **Helper Functions:**
    * `get_set_input()`: Handles user input for sets with validation.
    * `union()`, `intersection()`, `difference()`, etc.: Perform the core set logic.
* **Plotting:**
    * `plot_sets()`: The main function responsible for generating plots. It checks the number of sets and calls either `matplotlib-venn` (`venn2`, `venn3`) or `supervenn`. It also handles labeling, coloring, highlighting, and titling.
* **Menu:**
    * `display_menu_unicode_color()`: Formats and prints the interactive menu with colors and Unicode box characters. Uses an internal helper `get_text_length()` to handle width calculations with ANSI codes.
* **Main Logic:**
    * The script first collects the universal set and working set definitions.
    * It then enters a `while True` loop that displays the menu, gets the user's choice, validates input, calls the appropriate set operation and plotting functions, and repeats until the user chooses to exit.

## Dependencies 🔗

* [matplotlib](https://matplotlib.org/)
* [matplotlib-venn](https://github.com/konstantint/matplotlib-venn)
* [supervenn](https://github.com/gecko984/supervenn)

---

*This project is in progress. Contributions, suggestions, and feedback are welcome! Feel free to open issues or pull requests on GitHub.*

*License: MIT License*

