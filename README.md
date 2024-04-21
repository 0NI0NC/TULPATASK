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
  "code": "en",
  "messages": {
    "alpha": "The {_field_} field may only contain alphabetic characters",
    "alpha_num": "The {_field_} field may only contain alpha-numeric characters",
    "alpha_dash": "The {_field_} field may contain alpha-numeric characters as well as dashes and underscores",
    "alpha_spaces": "The {_field_} field may only contain alphabetic characters as well as spaces",
    "between": "The {_field_} field must be between {min} and {max}",
    "confirmed": "The {_field_} field confirmation does not match",
    "digits": "The {_field_} field must be numeric and exactly contain {length} digits",
    "dimensions": "The {_field_} field must be {width} pixels by {height} pixels",
    "email": "The {_field_} field must be a valid email",
    "excluded": "The {_field_} field is not a valid value",
    "ext": "The {_field_} field is not a valid file",
    "image": "The {_field_} field must be an image",
    "integer": "The {_field_} field must be an integer",
    "length": "The {_field_} field must be {length} long",
    "max_value": "The {_field_} field must be {max} or less",
    "max": "The {_field_} field may not be greater than {length} characters",
    "mimes": "The {_field_} field must have a valid file type",
    "min_value": "The {_field_} field must be {min} or more",
    "min": "The {_field_} field must be at least {length} characters",
    "numeric": "The {_field_} field may only contain numeric characters",
    "oneOf": "The {_field_} field is not a valid value",
    "regex": "The {_field_} field format is invalid",
    "required_if": "The {_field_} field is required",
    "required": "The {_field_} field is required",
    "size": "The {_field_} field size must be less than {size}KB"
  }
}

```

Change log:
- Added team management functionality to create and interact with multiple Tulpas simultaneously.
- Improved user interface for easier navigation and interaction.
- Enhanced task assignment process for better task management.
- Added option to delete saved Tulpas.
