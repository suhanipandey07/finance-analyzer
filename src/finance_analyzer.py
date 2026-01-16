import pandas as pd
import matplotlib.pyplot as plt

# ---------- 1. Read CSV ----------
file_name = input("Enter CSV file path (example: transactions.csv): ")
try:
    data = pd.read_csv(file_name)
except:
    print("File not found! Check the path.")
    exit()

print("\nHere is a preview of your data:")
print(data.head())

# ---------- 2. Check columns ----------
columns_needed = ["Date", "Description", "Amount", "Type", "Category"]
for col in columns_needed:
    if col not in data.columns:
        print("Your file must have these columns:", ", ".join(columns_needed))
        exit()

# ---------- 3. Calculate totals ----------
income_data = data[data["Type"].str.lower() == "income"]
expense_data = data[data["Type"].str.lower() == "expense"]

total_income = income_data["Amount"].sum()
total_expense = expense_data["Amount"].sum()
net_savings = total_income - total_expense

# ---------- 4. Highest & Lowest ----------
highest_income = income_data.loc[income_data["Amount"].idxmax()]
highest_expense = expense_data.loc[expense_data["Amount"].idxmax()]

# ---------- 5. Category-wise ----------
categories = expense_data["Category"].unique()
category_totals = {}
for cat in categories:
    cat_total = expense_data[expense_data["Category"] == cat]["Amount"].sum()
    category_totals[cat] = cat_total

# ---------- 6. Budget ----------
budget = float(input("\nSet your monthly budget limit: ₹"))

# ---------- 7. Display summary ----------
print("\n------ FINANCE SUMMARY ------")
print("Total Income  : ₹", total_income)
print("Total Expense : ₹", total_expense)
print("Net Savings   : ₹", net_savings)
print("Highest Income :", highest_income["Description"], "-", highest_income["Amount"])
print("Highest Expense:", highest_expense["Description"], "-", highest_expense["Amount"])

print("\nCategory-wise Expenses:")
for cat in categories:
    perc = round(category_totals[cat]/total_expense*100,1)
    print(cat, ":", category_totals[cat], "(", perc, "%)")

if total_expense > budget:
    print("\n⚠️ You have crossed your budget!")
else:
    print("\n✅ You are within your budget!")

# ---------- 8. Plot graphs ----------
# Save Pie Chart
plt.figure(figsize=(6,6))
plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
plt.title("Expenses by Category")
plt.savefig("category_expenses.png")
plt.close()

# Save Bar Chart
plt.figure(figsize=(6,4))
plt.bar(["Income","Expense"], [total_income, total_expense], color=["#27ae60","#c0392b"])
plt.title("Income vs Expense")
plt.ylabel("Amount (₹)")
plt.savefig("income_vs_expense.png")
plt.close()

# ---------- 9. Save Text Summary ----------
save_txt = input("\nDo you want to save summary as text file? yes/no: ")
if save_txt.lower() == "yes":
    f = open("finance_summary.txt", "w", encoding="utf-8")
    f.write("------ FINANCE SUMMARY ------\n")
    f.write("Total Income  : ₹ " + str(total_income) + "\n")
    f.write("Total Expense : ₹ " + str(total_expense) + "\n")
    f.write("Net Savings   : ₹ " + str(net_savings) + "\n")
    f.write("Highest Income : " + highest_income["Description"] + " - ₹ " + str(highest_income["Amount"]) + "\n")
    f.write("Highest Expense: " + highest_expense["Description"] + " - ₹ " + str(highest_expense["Amount"]) + "\n")
    f.write("Category-wise Expenses:\n")
    for cat in categories:
        f.write(cat + " : ₹ " + str(category_totals[cat]) + " (" + str(round(category_totals[cat]/total_expense*100,1)) + "%)\n")
    f.close()
    print("✅ Saved as 'finance_summary.txt'")

# ---------- 10. Save HTML Summary with Charts (Enhanced Look) ----------
save_html = input("\nDo you want to save summary as HTML file? yes/no: ")
if save_html.lower() == "yes":
    f = open("finance_summary.html", "w", encoding="utf-8")
    f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Finance Summary</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(to right, #ece9e6, #ffffff); margin: 0; padding: 0; }
        h1 { text-align: center; color: #2c3e50; margin-top: 20px; }
        .summary { background-color: #ffffff; padding: 25px; border-radius: 15px; width: 80%; max-width: 900px; margin: 30px auto; box-shadow: 0px 10px 25px rgba(0,0,0,0.1); }
        .summary p { font-size: 18px; margin: 12px 0; line-height: 1.5; }
        .income { color: #27ae60; font-weight: bold; }
        .expense { color: #c0392b; font-weight: bold; }
        .savings { color: #2980b9; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        table, th, td { border: 1px solid #ddd; }
        th, td { padding: 12px; text-align: center; }
        th { background-color: #34495e; color: #fff; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .budget-status { margin-top: 25px; font-size: 20px; font-weight: bold; padding: 15px; border-radius: 8px; text-align: center; }
        .within { background-color: #dff0d8; color: #3c763d; }
        .exceeded { background-color: #f2dede; color: #a94442; }
        img { display: block; margin: 20px auto; max-width: 100%; border-radius: 10px; box-shadow: 0px 5px 20px rgba(0,0,0,0.15); }
        .btn { display: inline-block; padding: 10px 20px; margin: 15px 5px 0 0; border-radius: 8px; text-decoration: none; color: #fff; background-color: #2980b9; font-weight: bold; transition: 0.3s; }
        .btn:hover { background-color: #1c5980; }
        h2 { color: #2c3e50; margin-top: 30px; }
    </style>
</head>
<body>
    <h1>Finance Summary</h1>
    <div class="summary">
""")
    f.write("<p>Total Income: <span class='income'>₹ " + str(total_income) + "</span></p>\n")
    f.write("<p>Total Expense: <span class='expense'>₹ " + str(total_expense) + "</span></p>\n")
    f.write("<p>Net Savings: <span class='savings'>₹ " + str(net_savings) + "</span></p>\n")
    f.write("<p>Highest Income: " + highest_income["Description"] + " - ₹ " + str(highest_income["Amount"]) + "</p>\n")
    f.write("<p>Highest Expense: " + highest_expense["Description"] + " - ₹ " + str(highest_expense["Amount"]) + "</p>\n")
    
    # Category table
    f.write("<h2>Category-wise Expenses</h2>\n<table>\n<tr><th>Category</th><th>Amount (₹)</th><th>Percentage</th></tr>\n")
    for cat in categories:
        perc = round(category_totals[cat]/total_expense*100,1)
        f.write("<tr><td>" + cat + "</td><td>" + str(category_totals[cat]) + "</td><td>" + str(perc) + "%</td></tr>\n")
    f.write("</table>\n")
    
    # Budget status
    status_class = "within" if total_expense <= budget else "exceeded"
    status_text = "✅ You are within your budget!" if total_expense <= budget else "⚠️ You have crossed your budget!"
    f.write("<div class='budget-status " + status_class + "'>" + status_text + "</div>\n")
    
    # Embed graphs
    f.write("<h2>Visualizations</h2>\n")
    f.write("<img src='category_expenses.png' alt='Expenses by Category'>\n")
    f.write("<img src='income_vs_expense.png' alt='Income vs Expense'>\n")
    
    f.write("</div></body></html>")
    f.close()
    print("✅ Saved as 'finance_summary.html'. Open in a browser to view.")
