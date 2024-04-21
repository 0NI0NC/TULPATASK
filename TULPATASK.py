from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
import getpass
import os

print("""                                             

 /$$$$$$$$ /$$   /$$ /$$       /$$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$   /$$$$$$  /$$   /$$
|__  $$__/| $$  | $$| $$      | $$__  $$ /$$__  $$|__  $$__//$$__  $$ /$$__  $$| $$  /$$/
   | $$   | $$  | $$| $$      | $$  \ $$| $$  \ $$   | $$  | $$  \ $$| $$  \__/| $$ /$$/ 
   | $$   | $$  | $$| $$      | $$$$$$$/| $$$$$$$$   | $$  | $$$$$$$$|  $$$$$$ | $$$$$/  
   | $$   | $$  | $$| $$      | $$____/ | $$__  $$   | $$  | $$__  $$ \____  $$| $$  $$  
   | $$   | $$  | $$| $$      | $$      | $$  | $$   | $$  | $$  | $$ /$$  \ $$| $$\  $$ 
   | $$   |  $$$$$$/| $$$$$$$$| $$      | $$  | $$   | $$  | $$  | $$|  $$$$$$/| $$ \  $$
   |__/    \______/ |________/|__/      |__/  |__/   |__/  |__/  |__/ \______/ |__/  \__/
   ======================================================================================
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
""")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("GOOGLE_API_KEY: NOT FOUND")

def save_tulpa(tulpa_name, tulpa_description):
    with open("SAVE.txt", "a") as file:
        file.write(f"Tulpa Name: {tulpa_name}\n")
        file.write(f"Tulpa Description: {tulpa_description}\n\n")

def load_saved_tulpas():
    saved_tulpas = []
    try:
        with open("SAVE.txt", "r") as file:
            lines = file.readlines()
            tulpa_name = None
            tulpa_description = None
            for line in lines:
                line = line.strip()
                if line.startswith("Tulpa Name:"):
                    if tulpa_name and tulpa_description:
                        saved_tulpas.append((tulpa_name, tulpa_description))
                    tulpa_name = line.split(": ")[1].strip()
                elif line.startswith("Tulpa Description:"):
                    tulpa_description = line.split(": ")[1].strip()
            if tulpa_name and tulpa_description:
                saved_tulpas.append((tulpa_name, tulpa_description))
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

def select_tulpa(saved_tulpas):
    print("Select tulpas to include in the team:")
    display_saved_tulpas(saved_tulpas)
    selected_tulpas = []
    while True:
        choice = input("Enter the number of the tulpa to include in the team (0 to finish): ")
        if choice == "0":
            break
        index = int(choice) - 1
        if 0 <= index < len(saved_tulpas):
            tulpa_name, tulpa_description = saved_tulpas[index]
            selected_tulpas.append((tulpa_name, tulpa_description))
        else:
            print(f"Invalid index: {index + 1}")
    return selected_tulpas

def tulpa_tasks(tulpa):
    papirus_phrases = input(f"Make Task For {tulpa.role}: ")
    description = papirus_phrases
    expected_output = ""
    task = Task(description=description, expected_output=expected_output)
    task.agent = tulpa
    return task

def main(saved_tulpas):
    MAX_TULPAS_LIMIT = 6

    tulpas_limit = min(MAX_TULPAS_LIMIT, len(saved_tulpas))

    if len(saved_tulpas) >= MAX_TULPAS_LIMIT:
        print("You have reached the limit of 6 saved tulpas.")
        return saved_tulpas
    
    print(" ----------------------------------")
    print("-  1. Create New Tulpa             -")
    print("-  2. Load Saved Tulpas as Team     -")
    print("-  3. Exit                          -")
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
            allow_delegation=True,
            verbose=True,
            llm=llm
        )
        
        saved_tulpas.append((TULPA_NAME, PAPIRUS))

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
        selected_tulpas = select_tulpa(saved_tulpas)
        agents = []
        for tulpa_name, tulpa_description in selected_tulpas:
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
                print("Tulpa Team is now working...")
                break

        crew.kickoff()

        print("Tulpa Team is now sleeping...")
        
    elif choice == "3":
        pass
    else:
        print("Invalid choice")

    return saved_tulpas

if __name__ == "__main__":
    saved_tulpas = load_saved_tulpas()
    saved_tulpas = main(saved_tulpas)
