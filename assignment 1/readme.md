# Running the project

I thought we might as well use a venv file for easier distribution between us. So, here's how to set it up if you've never used it (this is just followng the tutorial for the first part of the assignment, but ya).

1. In order to create a new virtual environment, cd into [app](./app/) directory, then

   ```bash
   python -m venv .venv
   ```

   or simply py -m venv .venv (depends on your PATH vars : ) )

2. Activate the env file. From the app directory just write (this is assuming your own windows, no idea for unix/mac)

    ```bash
    .venv\Scripts\activate
    ```

3. Then install the dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run the project by using

   ```bash
   briefcase dev
   ```

   Rest of the commands are available [here](https://briefcase.readthedocs.io/en/latest/reference/commands/index.html#)

## Part 1

Laves udfra [Cloud based Project Assignment 1 Part 1-1.pdf](./Cloud%20based%20Project%20Assignment%201%20Part%201-1.pdf)

## Part 2

From the assignment "Part 2 of Assignment 2 is to describe a small healthcare process as text and then identify activities, roles and rules following the example here: [End-user Development with DCR Process Designer](https://absalon.ku.dk/courses/78169/pages/end-user-development-with-dcr-process-designer) and include the explanation of what you did in the hand-in.

You should then make the diagram in the DCR Design tool and include the link to your graph in the hand-in."
