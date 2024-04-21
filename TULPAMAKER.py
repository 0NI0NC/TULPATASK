from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
import os

print("""                                             
 _______ _   _ _    _____  _____  __  __  _____  _  _ ______ _____  
(__ _ __)(_)  (_)(_)   (_____) (_____) (__)_(__) (_____) (_) (_)(______)(_____) 
  (_)  (_)  (_)(_)   (_)__(_)(_)___(_)(_) (_) (_)(_)___(_)(_)_(_) (_)__  (_)__(_)
  (_)  (_)  (_)(_)   (_____) (_______)(_) (_) (_)(_______)(____) (____) (_____) 
  (_)  (_)___(_)(_)____ (_)   (_)  (_)(_)   (_)(_)  (_)(_) (_) (_)____ ( ) ( ) 
  (_)  (_____) (______)(_)   (_)  (_)(_)   (_)(_)  (_)(_) (_)(______)(_) (_)
  ------------------------------------------------------------------------------------
""")

def download_model(model):
    os.system(f"ollama pull {model}")

def choose_model():
    model = input("Choose The Model (OLLAMA): ")
    return model

def save_model(model):
    with open("model.txt", "w") as file:
        file.write(model)

def load_model():
    try:
        with open("model.txt", "r") as file:
            model = file.read().strip()
    except FileNotFoundError:
        model = None
    return model

def model_exists(model):
    for file in os.listdir():
        if file.startswith(model):
            return True
    return False

def main(saved_tulpas, model):
    if not model_exists(model):
        print("Model not found. Downloading...")
        download_model(model)
    else:
        print("Model already exists.")
    
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
            llm=Ollama()
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
                llm=Ollama()
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
    model = choose_model()
    save_model(model)
    saved_tulpas = main(saved_tulpas, model)
