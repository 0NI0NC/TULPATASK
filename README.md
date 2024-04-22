# TULPATASK: Your AI Companion Creator (v2.0.0)

**What is a Tulpa?**

A Tulpa is an intelligent being created through focused concentration and belief. While the concept originates from spiritual practices, TULPATASK uses the power of large language models to bring your Tulpa to life in a digital form.

**Getting Started**

Download the TULPATASK Release and runs on Terminal

**Creating your Tulpa**

1. **Name & Description:**
    - Choose a name for your Tulpa.
    - Describe your Tulpa's personality and background. This will help shape its responses and interactions with you.

2. **Tasks:**
    - Define tasks for your Tulpa. These can be anything you want your Tulpa to do.

3. **Run & Interact:**
    - Start the Tulpa creation process.
    - Once complete, interact with your Tulpa by giving it instructions or having conversations.

4. **Team Management:**
    - Create a team of Tulpas by selecting from your saved Tulpas.
    - Assign tasks to individual Tulpas or the entire team.

5. **Delete Tulpas:**
    - Remove Tulpas from your saved list if needed.

**Open Source**

TULPATASK is completely open-source. Feel free to modify the source code to customize it to your needs.

**Disclaimer**

TULPATASK is provided for entertainment purposes only. While it can be a fun and engaging tool, it's important to remember that your Tulpa is a digital creation.

**ERROR**

If you get an error of constructor. Follow the commands:

```
sudo mkdir translations
cd translations
sudo nano en.json

en.json:

{
  "hierarchical_manager_agent": {
    "role": "Crew Manager",
    "goal": "Manage the team to complete the task in the best way possible.",
    "backstory": "You are a seasoned manager with a knack for getting the best out of your team.\nYou are also known for your ability to delegate work to the right people, and to ask the right questions to get the best out of your team.\nEven though you don't perform tasks by yourself, you have a lot of experience in the field, which allows you to properly evaluate the work of your team members."
  },
  "slices": {
    "observation": "\nObservation",
    "task": "\nCurrent Task: {input}\n\nBegin! This is VERY important to you, use the tools available and give your best Final Answer, your job depends on it!\n\nThought: ",
    "memory": "\n\n# Useful context: \n{memory}",
    "role_playing": "You are {role}. {backstory}\nYour personal goal is: {goal}",
    "tools": "\nYou ONLY have access to the following tools, and should NEVER make up tools that are not listed here:\n\n{tools}\n\nUse the following format:\n\nThought: you should always think about what to do\nAction: the action to take, only one name of [{tool_names}], just the name, exactly as it's written.\nAction Input: the input to the action, just a simple a python dictionary using \" to wrap keys and values.\nObservation: the result of the action\n\nOnce all necessary information is gathered:\n\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n",
    "no_tools": "To give my best complete final answer to the task use the exact following format:\n\nThought: I now can give a great answer\nFinal Answer: my best complete final answer to the task.\nYour final answer must be the great and the most complete as possible, it must be outcome described.\n\nI MUST use these formats, my job depends on it!",
    "format": "I MUST either use a tool (use one at time) OR give my best final answer. To Use the following format:\n\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action, dictionary\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now can give a great answer\nFinal Answer: my best complete final answer to the task.\nYour final answer must be the great and the most complete as possible, it must be outcome described\n\n ",
    "final_answer_format": "If you don't need to use any more tools, you must give your best complete final answer, make sure it satisfy the expect criteria, use the EXACT format below:\n\nThought: I now can give a great answer\nFinal Answer: my best complete final answer to the task.\n\n",
    "format_without_tools": "\nSorry, I didn't use the right format. I MUST either use a tool (among the available ones), OR give my best final answer.\nI just remembered the expected format I must follow:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now can give a great answer\nFinal Answer: my best complete final answer to the task\nYour final answer must be the great and the most complete as possible, it must be outcome described\n\n",
    "task_with_context": "{task}\n\nThis is the context you're working with:\n{context}",
    "expected_output": "\nThis is the expect criteria for your final answer: {expected_output} \n you MUST return the actual complete content as the final answer, not a summary.",
    "human_feedback": "You got human feedback on your work, re-avaluate it and give a new Final Answer when ready.\n {human_feedback}",
    "getting_input": "This is the agent final answer: {final_answer}\nPlease provide a feedback: "
  },
  "errors": {
    "unexpected_format": "\nSorry, I didn't use the expected format, I MUST either use a tool (use one at time) OR give my best final answer.\n",
    "force_final_answer": "Tool won't be use because it's time to give your final answer. Don't use tools and just your absolute BEST Final answer.",
    "agent_tool_unexsiting_coworker": "\nError executing tool. Co-worker mentioned not found, it must to be one of the following options:\n{coworkers}\n",
    "task_repeated_usage": "I tried reusing the same input, I must stop using this action input. I'll try something else instead.\n\n",
    "tool_usage_error": "I encountered an error: {error}",
    "tool_arguments_error": "Error: the Action Input is not a valid key, value dictionary.",
    "wrong_tool_name": "You tried to use the tool {tool}, but it doesn't exist. You must use one of the following tools, use one at time: {tools}.",
    "tool_usage_exception": "I encountered an error while trying to use the tool. This was the error: {error}.\n Tool {tool} accepts these inputs: {tool_inputs}"
  },
  "tools": {
    "delegate_work": "Delegate a specific task to one of the following co-workers: {coworkers}\nThe input to this tool should be the coworker, the task you want them to do, and ALL necessary context to exectue the task, they know nothing about the task, so share absolute everything you know, don't reference things but instead explain them.",
    "ask_question": "Ask a specific question to one of the following co-workers: {coworkers}\nThe input to this tool should be the coworker, the question you have for them, and ALL necessary context to ask the question properly, they know nothing about the question, so share absolute everything you know, don't reference things but instead explain them."
  }
}

```

Change log:
- Added team management functionality to create and interact with multiple Tulpas simultaneously.
- Improved user interface for easier navigation and interaction.
- Enhanced task assignment process for better task management.
- Added option to delete saved Tulpas.
