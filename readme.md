# Running the project

I thought we might as well use a venv file for easier distribution between us. So, here's how to set it up if you've never used it (this is just followng the tutorial for the first part of the assignment, but ya).

1. In order to create a new virtual environment, cd into any of the assignment's [app](./app/) directory, then

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