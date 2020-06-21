# FinanceAutomator
Automates personal finance-tracking by maintaining a xlsx-file into which the users monthly incomes and expenses are logged.

Program flow:

1. User gives the program an uri into a directory containing his bank account events of the past month. The file must be in .csv-format with the following columns in this order: Date;Sender/Receiver;Description;Reference/Message;Amount.
2. User gives the program a location into which he wishes the xlsx-file to be saved.
3. User gives the program a category for which he wishes a value to be calculated, for example "groceries".
4. User gives the program tags, that is, strings that appear in the Sender/Receiver column of the transactions, in order for the program to recognise transactions belonging to this category.
5. Program calculates values for all given categories and the default ones (total income, total expenses, other income, other expenses) and writes the results into an xlsx-file named "talousseuranta_<number_of_month>.xlsx"
6. Upon next run the program remebers the user's settings, but gives an option to edit them. 
7. New values are added into the xlsx-file by replacing the transactions file of the previous month with the one of the current one and running the program again.
