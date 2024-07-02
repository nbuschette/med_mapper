# med_mapper
Given a medication name, the application will return rxcui and ndc mapping.

1. If program is setup in a venv, install dependencies from requirements.txt file.<br>
2. Run starter.py.<br>
3. Follow Tkinter GUI prompts.<br>
   a. Make sure to have a setup csv file that contains medication names in column A with no header.<br>
4. Output will be two csv files.<br>
   a. RXCUI.csv will contain rows of medication names in column A with additional columns for each associated rxcui.<br>
   b. NDC.csv will contain rows of rxcui in column A with additional columns for each associated ndc.<br>
