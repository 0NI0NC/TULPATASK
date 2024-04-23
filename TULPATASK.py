from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, DirectoryReadTool, BaseTool
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

class FileReadTool:
    def __init__(self):
        pass

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            with open(file_path, 'w') as file:
                file.write("")
            return f"File '{file_path}' created."
        except Exception as e:
            return str(e)

class FileWriteTool(BaseTool):
    name: str = "File Write Tool"
    description: str = "A tool for writing content to a file."

    def _run(self, file_path: str, content: str) -> str:
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return f"Content successfully written to file '{file_path}'."
        except Exception as e:
            return f"Error writing to file '{file_path}': {str(e)}"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
file_read_tool = FileReadTool()
directory_read_tool = DirectoryReadTool()
file_write_tool = FileWriteTool()


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

def select_tulpa(agents):
    print("Select a tulpa to assign the task:")
    for i, tulpa in enumerate(agents, 1):
        print(f"{i}. {tulpa.role}")
    choice = int(input("Enter the number of the tulpa: "))
    if 1 <= choice <= len(agents):
        return agents[choice - 1]
    else:
        print("Invalid choice.")
        return None

def tulpa_tasks(tulpa):
    papirus_phrases = input(f"Make Task For {tulpa.role}: ")
    description = papirus_phrases
    expected_output = ""
    task = Task(description=description, expected_output=expected_output)
    task.agent = tulpa
    return task

def load_tulpa(saved_tulpas):
    print("Select the number of tulpas to load as team members:")
    display_saved_tulpas(saved_tulpas)
    num_tulpas = int(input("Enter the number of tulpas to load: "))
    loaded_tulpas = []
    for _ in range(num_tulpas):
        index = int(input("Enter the number of tulpas to load: ")) - 1
        if 0 <= index < len(saved_tulpas):
            loaded_tulpa = saved_tulpas[index]
            tulpa_name, tulpa_description = loaded_tulpa
            tulpa = Agent(
                role=tulpa_name,
                goal=f"{tulpa_name} knows and will follow whatever his owner wants, because, {tulpa_name} Is An Tulpa Companion Of Owner",
                backstory=tulpa_description,
                allow_delegation=False,
                verbose=True,
                memory=True,
                tools=[file_read_tool, directory_read_tool, file_write_tool],  
                llm=llm
            )
            loaded_tulpas.append(tulpa)
        else:
            print(f"Invalid index: {index + 1}")
    return loaded_tulpas

def main(saved_tulpas):
    if len(saved_tulpas) >= 6:
        print("You have reached the limit of 6 saved tulpas.")
        return saved_tulpas
    
    print(" ----------------------------------")
    print("-  1. Create New Tulpa              -")
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
            memory=True,
            tools=[file_read_tool, directory_read_tool, file_write_tool],
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
        loaded_tulpas = load_tulpa(saved_tulpas)
        agents = []
        for tulpa_name, tulpa_description in loaded_tulpas:
            tulpa = Agent(
                role=tulpa_name,
                goal=f"{tulpa_name} knows and will follow whatever his owner wants, because, {tulpa_name} Is An Tulpa Companion Of Owner",
                backstory=tulpa_description,
                allow_delegation=False,
                verbose=True,
                memory=True,
                tools=[file_read_tool, directory_read_tool, file_write_tool],
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
                    tools=[file_read_tool, directory_read_tool, file_write_tool],
                    llm=llm
                )
                agents.append(tulpa)
            else:
                print(f"Invalid index: {index + 1}")

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
