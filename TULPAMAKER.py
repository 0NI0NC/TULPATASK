from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
import os

print("""                                             

 /$$$$$$$$ /$$   /$$ /$$       /$$$$$$$   /$$$$$$  /$$      /$$  /$$$$$$  /$$   /$$ /$$$$$$$$ /$$$$$$$ 
|__  $$__/| $$  | $$| $$      | $$__  $$ /$$__  $$| $$$    /$$$ /$$__  $$| $$  /$$/| $$_____/| $$__  $$
   | $$   | $$  | $$| $$      | $$  \ $$| $$  \ $$| $$$$  /$$$$| $$  \ $$| $$ /$$/ | $$      | $$  \ $$
   | $$   | $$  | $$| $$      | $$$$$$$/| $$$$$$$$| $$ $$/$$ $$| $$$$$$$$| $$$$$/  | $$$$$   | $$$$$$$/
   | $$   | $$  | $$| $$      | $$____/ | $$__  $$| $$  $$$| $$| $$__  $$| $$  $$  | $$__/   | $$__  $$
   | $$   | $$  | $$| $$      | $$      | $$  | $$| $$\  $ | $$| $$  | $$| $$\  $$ | $$      | $$  \ $$
   | $$   |  $$$$$$/| $$$$$$$$| $$      | $$  | $$| $$ \/  | $$| $$  | $$| $$ \  $$| $$$$$$$$| $$  | $$
   |__/    \______/ |________/|__/      |__/  |__/|__/     |__/|__/  |__/|__/  \__/|________/|__/  |__/
                                                                                                                                                                                                            
                                                                                                      
""")

llm = Ollama(model="gemma:2b-v1.1")

def save_tulpa(tulpa_name, tulpa_description):
    with open("SAVE.txt", "a") as file:
        file.write(f"Tulpa Name: {tulpa_name}\n")
        file.write(f"Tulpa Description: {tulpa_description}\n\n")

def load_saved_tulpas():
    saved_tulpas = []
    try:
        with open("SAVE.txt", "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 4):
                if i + 1 < len(lines):
                    name = lines[i].split(": ")[1].strip()
                    description = lines[i + 1].split(": ")[1].strip()
                    saved_tulpas.append((name, description))
                else:
                    print("Invalid format in SAVE.txt file.")
    except FileNotFoundError:
        print("No saved tulpas found.")
    return saved_tulpas

def display_saved_tulpas(saved_tulpas):
    print("Saved Tulpas:")
    for i, tulpa in enumerate(saved_tulpas, 1):
        print(f"{i}. Name: {tulpa[0]}, Description: {tulpa[1]}")

def delete_tulpa(saved_tulpas, number):
    try:
        index = int(number)
        if 1 <= index <= len(saved_tulpas):
            del saved_tulpas[index - 1]
            with open("SAVE.txt", "w") as file:
                for tulpa in saved_tulpas:
                    file.write(f"Tulpa Name: {tulpa[0]}\n")
                    file.write(f"Tulpa Description: {tulpa[1]}\n\n")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input. Please provide a valid number.")
    return saved_tulpas

def tulpa_tasks(tulpa):
    papirus_phrases = input(f"Make Task For {tulpa.role}: ")
    description = papirus_phrases
    expected_output = ""
    task = Task(description=description, expected_output=expected_output)
    task.agent = tulpa
    return task

def load_tulpa(saved_tulpas):
    print("Select the number of tulpas to load as workers:")
    display_saved_tulpas(saved_tulpas)
    num_tulpas = int(input("Enter the number of tulpas to load: "))
    loaded_tulpas = []
    for i in range(num_tulpas):
        index = i + 1
        if 1 <= index <= len(saved_tulpas):
            loaded_tulpas.append(saved_tulpas[index - 1])
        else:
            print(f"Invalid index: {index}")
    return loaded_tulpas

def main(saved_tulpas):
    if len(saved_tulpas) >= 6:
        print("You have reached the limit of 6 saved tulpas.")
        return saved_tulpas
    
    print(" ----------------------------------")
    print("-  1. Create New Tulpa             -")
    print("-  2. Load Saved Tulpas as Workers -")
    print("-  3. Exit                         -")
    print(" ----------------------------------")
    choice = input("Select an option: ")

    if choice == "1":
        TULPA_NAME = input("Choose Name For Tulpa: ")
        PAPIRUS = input("Create Your Tulpa Description: ")
        save_tulpa(TULPA_NAME, PAPIRUS)

        TULPA = Agent(
            role=TULPA_NAME,
            goal=f"{TULPA_NAME} knows and will follow whatever his owner wants, because, {TULPA_NAME} Is An Tulpa Companion Of Owner",
            backstory=PAPIRUS,
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

        crew = Crew(agents=[TULPA], tasks=[], verbose=1)

        while True:
            choice = input("Select An Option (1 - TASKS / 2 - DELETE TULPA / 3 - EXIT): ")

            if choice == "1" or choice.lower() == "one":
                task = tulpa_tasks(TULPA)
                crew.tasks.append(task)
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
                allow_delegation=False,
                verbose=True,
                llm=llm
            )
            agents.append(tulpa)
        crew = Crew(agents=agents, tasks=[], verbose=1)

        while True:
            choice = input("Select An Option (1 - TASKS / 2 - DELETE TULPA / 3 - EXIT): ")

            if choice == "1" or choice.lower() == "one":
                for tulpa in agents:
                    task = tulpa_tasks(tulpa)
                    crew.tasks.append(task)
            elif choice == "2" or choice.lower() == "two":
                display_saved_tulpas(saved_tulpas)
                index = int(input("Enter the number of the tulpa to delete: "))
                saved_tulpas = delete_tulpa(saved_tulpas, index)
            elif choice == "3" or choice.lower() == "three":
                print("Tulpas are now working...")
                break

        crew.kickoff()

        print("Tulpas are now sleeping...")
        
    elif choice == "3":
        pass
    else:
        print("Invalid choice")

    return saved_tulpas

if __name__ == "__main__":
    saved_tulpas = load_saved_tulpas()
    saved_tulpas = main(saved_tulpas)
