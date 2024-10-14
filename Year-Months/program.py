import os
import curses

# Function to choose a directory
def choose_directory():
    choice = input("Where would you like to generate folders?\n1. Current directory (default)\n2. Specify a directory\nEnter 1 or 2: ").strip()
    if choice == '2':
        directory = input("Please provide the full path to the directory: ").strip()
        if not os.path.exists(directory):
            print("Directory does not exist. Exiting.")
            return None
    else:
        directory = os.getcwd()
    return directory

# Function to show and get year selections from the user
def choose_years():
    years = ["2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"]
    selected_years = []
    
    def interactive_menu(stdscr):
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        stdscr.addstr("Use SPACE to select/deselect years. Press ENTER when done.\n")
        selected = [False] * len(years)
        current_idx = 0

        while True:
            for idx, year in enumerate(years):
                if idx == current_idx:
                    stdscr.addstr(idx + 2, 0, f"> {year}", curses.A_REVERSE)
                else:
                    mark = "x" if selected[idx] else " "
                    stdscr.addstr(idx + 2, 0, f"  [{mark}] {year}")

            key = stdscr.getch()

            if key == curses.KEY_UP and current_idx > 0:
                current_idx -= 1
            elif key == curses.KEY_DOWN and current_idx < len(years) - 1:
                current_idx += 1
            elif key == ord(' '):
                selected[current_idx] = not selected[current_idx]
            elif key == ord('\n'):
                break

        return [years[i] for i, sel in enumerate(selected) if sel]

    selected_years = curses.wrapper(interactive_menu)
    return selected_years

# Function to create the year and month folders
def create_folders(directory, years):
    for year in years:
        year_short = year[-2:]
        year_path = os.path.join(directory, year_short)
        os.makedirs(year_path, exist_ok=True)

        for month in range(1, 13):
            month_path = os.path.join(year_path, str(month))
            os.makedirs(month_path, exist_ok=True)
        print(f"Created folders for {year_short} in {year_path}")

def main():
    # Step 1: Choose directory
    directory = choose_directory()
    if directory is None:
        return

    # Step 2: Choose years
    selected_years = choose_years()
    if not selected_years:
        print("No years selected. Exiting.")
        return

    # Step 3: Generate the folders
    create_folders(directory, selected_years)
    print("Folder generation complete.")

if __name__ == "__main__":
    main()
