from crewai import Agent, Task, Crew
from crewai_tools import DirectoryReadTool, FileReadTool, FileWriteTool, BaseTool
from langchain_community.llms import Ollama
import getpass
import os

class FileCreateTool(BaseTool):
    name: str = "File Create Tool"
    description: str = "A tool to create a file with specified content."

    def _run(self, file_path_content: dict) -> str:
        file_path = file_path_content.get("file_path")
        content = file_path_content.get("content")

        try:
            with open(file_path, "w") as file:
                file.write(content)
            return "File created successfully."
        except Exception as e:
            return f"Error creating file: {str(e)}"

class DirectoryCreateTool(BaseTool):
    name: str = "Directory Create Tool"
    description: str = "A tool to create a directory."

    def _run(self, directory_path: str) -> str:
        try:
            os.makedirs(directory_path, exist_ok=True)
            return "Directory created successfully."
        except Exception as e:
            return f"Error creating directory: {str(e)}"

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

llm = Ollama(model="llama3")

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("GOOGLE_API_KEY: NOT FOUND")

docs_tool = DirectoryReadTool(directory='./data')
file_read_tool = FileReadTool()
file_write_tool = FileWriteTool()
create_file_tool = FileCreateTool()
create_dir_tool = DirectoryCreateTool()

def tulpa_tasks(tulpa):
    papirus_phrases = input(f"Make Task For {tulpa.role}: ")
    description = papirus_phrases
    expected_output = ""
    task = Task(description=description, expected_output=expected_output)
    task.agent = tulpa

    directory = "data"  
    file_name = input("Enter the name of the file (e.g., CALC.py): ")
    file_path = os.path.join(directory, file_name)  

    content = input("Enter the content for the file: ")

    task.tools[create_file_tool] = {"file_path": file_path, "content": content}

    directory_name = input("Enter the name of the directory: ")
    directory_path = os.path.join(directory, directory_name)

    task.tools[create_dir_tool] = {"directory_path": directory_path}

    return task

def main(saved_tulpas):
    MAX_TULPAS_LIMIT = 6

    tulpas_limit = min(MAX_TULPAS_LIMIT, len(saved_tulpas))

    if len(saved_tulpas) >= MAX_TULPAS_LIMIT:
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

        TULPA = Agent(
            role=TULPA_NAME,
            goal=f"{TULPA_NAME} knows and will follow whatever his owner wants, because, {TULPA_NAME} Is An Tulpa Companion Of Owner",
            backstory=PAPIRUS,
            allow_delegation=True,
            verbose=True,
            llm=llm,
            memory=True,
            tools=[docs_tool, file_read_tool, file_write_tool, create_file_tool, create_dir_tool],
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
                allow_delegation=True,
                verbose=True,
                llm=llm,
                memory=True,
                tools=[docs_tool, file_read_tool, file_write_tool, create_file_tool, create_dir_tool],
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
