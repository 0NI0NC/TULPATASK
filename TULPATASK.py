### Imports ###
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from functools import wraps
import getpass
import os
import cProfile
import time

### Function to print ASCII art ###
def print_ascii_art():
    print(
    "                                             \n"
    " /$$$$$$$$ /$$   /$$ /$$       /$$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$   /$$$$$$  /$$   /$$\n"
    "|__  $$__/| $$  | $$| $$      | $$__  $$ /$$__  $$|__  $$__//$$__  $$ /$$__  $$| $$  /$$/\n"
    "   | $$   | $$  | $$| $$      | $$  \\ $$| $$  \\ $$   | $$  | $$  \\ $$| $$  \\__/| $$ /$$/ \n"
    "   | $$   | $$  | $$| $$      | $$$$$$$/| $$$$$$$$   | $$  | $$$$$$$$|  $$$$$$ | $$$$$/  \n"
    "   | $$   | $$  | $$| $$      | $$____/ | $$__  $$   | $$  | $$__  $$ \\____  $$| $$  $$  \n"
    "   | $$   | $$  | $$| $$      | $$      | $$  | $$   | $$  | $$  | $$ /$$  \\ $$| $$\\  $$  \n"
    "   | $$   |  $$$$$$/| $$$$$$$$| $$      | $$  | $$   | $$  | $$  | $$|  $$$$$$/| $$ \\  $$\n"
    "   |__/    \\______/ |________/|__/      |__/  |__/   |__/  |__/  |__/ \\______/ |__/  \\__/\n"
    "   ======================================================================================\n"
)

### Delay Function ###
def delay(seconds):
    print(f"Waiting for {seconds} seconds...")
    time.sleep(seconds) 

### Profiling decorator ###
def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        profiler.print_stats(sort="cumulative")
        return result
    return wrapper

### Function to save tulpa to file ###
def save_tulpa(tulpa_name, tulpa_description):
    with open("SAVE.txt", "a") as file:
        file.write(f"Tulpa Name: {tulpa_name}\n")
        file.write(f"Tulpa Description: {tulpa_description}\n\n")

### Function to load saved tulpas from file ###
def load_saved_tulpas():
    saved_tulpas = []
    try:
        with open("SAVE.txt", "r") as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                if lines[i].startswith("Tulpa Name:") and i + 1 < len(lines) and lines[i + 1].startswith("Tulpa Description:"):
                    tulpa_name = lines[i].split(": ")[1].strip()
                    tulpa_description = lines[i + 1].split(": ")[1].strip()
                    saved_tulpas.append((tulpa_name, tulpa_description))
                    i += 2
                else:
                    i += 1 
    except FileNotFoundError:
        print("No saved tulpas found.")
    return saved_tulpas
    
### Function to delete tulpa ###
def delete_tulpa(saved_tulpas, number):
    try:
        index = int(number)
        if 1 <= index <= len(saved_tulpas):
            saved_tulpas.pop(index - 1)
            with open("SAVE.txt", "w") as file:
                for tulpa in saved_tulpas:
                    file.write(f"Tulpa Name: {tulpa[0]}\n")
                    file.write(f"Tulpa Description: {tulpa[1]}\n\n")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input. Please provide a valid number.")
    return saved_tulpas

### Function to create tulpa tasks ###
def tulpa_tasks(agents):
    tasks = []
    for agent in agents:
        while True:
            num_tasks_str = input(f"Enter the number of tasks for {agent.role}: ")
            if len(num_tasks_str) > 1000000000:
                print("Input too long. Please provide a shorter input.")
                continue
            try:
                num_tasks = int(num_tasks_str)
                break
            except ValueError:
                print("Invalid input. Please provide a valid number.")
        
        ### Collect task descriptions ###
        task_descriptions = []
        for _ in range(num_tasks):
            papirus_phrases = input(f"Task for {agent.role}: ")
            description = papirus_phrases
            task_descriptions.append(description)

        ### Batch tasks ###
        batch_size = 5 
        for i in range(0, len(task_descriptions), batch_size):
            batch_descriptions = task_descriptions[i:i+batch_size]
            batch_expected_output = [""] * len(batch_descriptions)
            batch_tasks = [Task(description=desc, expected_output=output) for desc, output in zip(batch_descriptions, batch_expected_output)]
            for task in batch_tasks:
                task.agent = agent
            tasks.extend(batch_tasks)
            
    return tasks

### Function to load tulpas ###
def load_tulpa(saved_tulpas):
    print("Selecting all loaded tulpas to include in the team.")
    loaded_tulpas = saved_tulpas
    return loaded_tulpas

### Function to display saved tulpas ###
def display_saved_tulpas(saved_tulpas):
    print("Saved Tulpas:")
    for i, tulpa in enumerate(saved_tulpas, 1):
        print(f"{i}. Name: {tulpa[0]}, Description: {tulpa[1]}")

### Main function ###
@profile
def main(saved_tulpas):
    print_ascii_art()

    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro")

    while True:
        print(" ----------------------------------------")
        print("-  1. Create New Tulpa                   -")
        print("-  2. Load Saved Tulpas as Team          -")
        print("-  3. Exit                               -")
        print(" ----------------------------------------")
        choice = input("Select an option: ")

        if choice == "1":
            TULPA_NAME = input("Choose Name For Tulpa: ")
            PAPIRUS = input("Create Your Tulpa Description: ")
            save_tulpa(TULPA_NAME, PAPIRUS)

            TULPA = Agent(
                role=TULPA_NAME,
                goal=f"{TULPA_NAME} knows and will follow whatever his owner wants, because, {TULPA_NAME} Is An Tulpa Companion Of Owner",
                backstory=PAPIRUS,
                allow_delegation=True,
                verbose=True,
                memory=True,
                llm=llm
            )

            saved_tulpas.append((TULPA_NAME, PAPIRUS))

            crew = Crew(agents=[TULPA], tasks=[], verbose=1)

            while True:
                choice = input("Select An Option (1 - TASKS / 2 - DELETE TULPA / 3 - EXIT): ")

                if choice == "1" or choice.lower() == "one":
                    tasks = tulpa_tasks([TULPA])
                    crew.tasks.extend(tasks)
                elif choice == "2" or choice.lower() == "two":
                    display_saved_tulpas(saved_tulpas)
                    index = int(input("Enter the number of the tulpa to delete: "))
                    saved_tulpas = delete_tulpa(saved_tulpas, index)
                elif choice == "3" or choice.lower() == "three":
                    print(f"{TULPA_NAME} Now Is Working...")
                    break

            if TULPA is not None:
                crew.kickoff()

            print(f"{TULPA_NAME} Now Is Sleeping...")

        elif choice == "2":
            loaded_tulpas = load_tulpa(saved_tulpas)
            agents = []
            for tulpa_name, tulpa_description in loaded_tulpas:
                tulpa = Agent(
                    role=tulpa_name,
                    goal=f"{tulpa_name} knows and will follow whatever his owner wants, because, {tulpa_name} Is An Tulpa Companion Of Owner",
                    backstory=tulpa_description,
                    allow_delegation=True,
                    verbose=True,
                    memory=True,
                    llm=llm
                )
                agents.append(tulpa)

            print("Select tulpas to include in the team:")
            display_saved_tulpas(saved_tulpas)
            while True:
                choice = input("Enter the number of the tulpa to include in the team (0 to finish): ")
                if choice == "0":
                    break
                index = int(choice) - 1
                if 0 <= index < len(saved_tulpas):
                    tulpa_name, tulpa_description = saved_tulpas[index]
                    tulpa = Agent(
                        role=tulpa_name,
                        goal=f"{tulpa_name} knows and will follow whatever his owner wants, because, {tulpa_name} Is An Tulpa Companion Of Owner",
                        backstory=tulpa_description,
                        allow_delegation=True,
                        verbose=True,
                        memory=True,
                        process=Process.hierarchical,  
                        manager_llm=llm
                    )
                    agents.append(tulpa)
                else:
                    print(f"Invalid index: {index + 1}")

            crew = Crew(agents=agents, tasks=[], verbose=1)

            while True:
                choice = input("Select An Option (1 - TASKS / 2 - DELETE TULPA / 3 - EXIT): ")

                if choice == "1" or choice.lower() == "one":
                    tasks = tulpa_tasks(agents)
                    crew.tasks.extend(tasks)
                elif choice == "2" or choice.lower() == "two":
                    display_saved_tulpas(saved_tulpas)
                    index = int(input("Enter the number of the tulpa to delete: "))
                    saved_tulpas = delete_tulpa(saved_tulpas, index)
                elif choice == "3" or choice.lower() == "three":
                    print("Tulpa Team is now working...")
                    break

            crew.kickoff()
            delay(2)

            print("Tulpa Team is now sleeping...")

        elif choice == "3":
            break
        else:
            print("Invalid choice")

    return saved_tulpas

if __name__ == "__main__":
    saved_tulpas = load_saved_tulpas()
    saved_tulpas = main(saved_tulpas)
