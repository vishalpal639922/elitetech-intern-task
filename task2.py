import pandas as pd
from fpdf import FPDF

# Load CSV data
data = pd.read_csv("E:\Silon\python2025\data.csv")

# Data analysis
summary = data.groupby("Department")["Salary"].agg(["count", "mean", "min", "max"]).reset_index()
summary.columns = ["Department", "Employee Count", "Average Salary", "Min Salary", "Max Salary"]

# PDF report class
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Company Employee Salary Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_summary_table(self, data):
        self.set_font("Arial", "B", 12)
        col_widths = [40, 40, 40, 35, 35]
        headers = data.columns.tolist()

        # Add headers
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, border=1, align="C")
        self.ln()

        # Add data rows
        self.set_font("Arial", "", 12)
        for _, row in data.iterrows():
            self.cell(col_widths[0], 10, row["Department"], border=1)
            self.cell(col_widths[1], 10, str(row["Employee Count"]), border=1, align="C")
            self.cell(col_widths[2], 10, f"{row['Average Salary']:.2f}", border=1, align="R")
            self.cell(col_widths[3], 10, f"{row['Min Salary']:.2f}", border=1, align="R")
            self.cell(col_widths[4], 10, f"{row['Max Salary']:.2f}", border=1, align="R")
            self.ln()

# Generate PDF
pdf = PDFReport()
pdf.add_page()
pdf.add_summary_table(summary)
pdf.output("salary_report.pdf")

print("PDF report generated: salary_report.pdf")
