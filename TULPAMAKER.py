from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
import os

print("""                                                                                         
 _______  _     _  _       _____    _____    __   __    _____   _    _  ______  _____  
(__ _ __)(_)   (_)(_)     (_____)  (_____)  (__)_(__)  (_____) (_)  (_)(______)(_____) 
   (_)   (_)   (_)(_)     (_)__(_)(_)___(_)(_) (_) (_)(_)___(_)(_)_(_) (_)__   (_)__(_)
   (_)   (_)   (_)(_)     (_____) (_______)(_) (_) (_)(_______)(____)  (____)  (_____) 
   (_)   (_)___(_)(_)____ (_)     (_)   (_)(_)     (_)(_)   (_)(_) (_) (_)____ ( ) ( ) 
   (_)    (_____) (______)(_)     (_)   (_)(_)     (_)(_)   (_)(_)  (_)(______)(_)  (_)
   ------------------------------------------------------------------------------------
""")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

TULPA_NAME = input("Choose Name For Tulpa: ")
PAPIRUS = input("Create Your Tulpa Description: ")
    
TULPA = Agent(
    role=f"{TULPA_NAME}",
    goal=f"{TULPA_NAME} knows and will follow whatever his owner wants, because, {TULPA_NAME} Is An Tulpa Companion Of Owner",
    backstory=PAPIRUS,
    allow_delegation=False,
    verbose=True,
    llm=llm
)

crew = Crew(agents=[TULPA], tasks=[], verbose=1)

google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key
else:
    print("GOOGLE_API_KEY: NOT FOUND!")
    
def tulpa_tasks():
    papirus_phrases = input(f"Make Task For {TULPA_NAME}: ")
    description = papirus_phrases  
    expected_output = "" 
    task = Task(description=description, expected_output=expected_output)
    task.agent = TULPA
    return task

 
def main():
    crew.agents.append(TULPA)
    while True:
        choice = input("Select An Option (1 - TASKS / 2 - EXIT): ")
    
        if choice == "1" or choice.lower() == "one":
            task = tulpa_tasks()
            crew.tasks.append(task)  
        elif choice == "2" or choice.lower() == "two":
            print(f"{TULPA_NAME} Now Is Working...")
            break  
    
    if TULPA is not None:  
        crew.kickoff()  
    
    print(f"{TULPA_NAME} Now Is Sleeping...")

if __name__ == "__main__":
   main()
