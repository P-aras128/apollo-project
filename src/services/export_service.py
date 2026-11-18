
import pandas as pd
from pathlib import Path
from datetime import datetime
from config.settings import OUTPUT_DIR


class ExportService:

    def __init__(self):
        self.output_dir = Path(OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def prepare_data(self, companies, employees):

        rows = []

        for employee in employees:

            company = employee.get("company", {})
            if not isinstance(company, dict):
                company = {}

            row = {
                "Company Name": (
                    company.get("company_name")
                    or company.get("name")
                    or employee.get("organization_name")
                ),
                "Domain": (
                    company.get("domain")
                    or employee.get("domain")
                ),
                "Employee Name": (
                    employee.get("name")
                    or " ".join(filter(None, [
                        employee.get("first_name"),
                        employee.get("last_name")
                    ]))
                ),
                "Job Title": employee.get("title"),
                "Email": employee.get("email"),
                "Email Status": employee.get("email_status"),
                "LinkedIn URL": employee.get("linkedin_url")
            }

            rows.append(row)

        return pd.DataFrame(rows)

    def export_excel(self, dataframe):

        filename = (
            f"apollo_leads_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
        )

        file_path = self.output_dir / filename

        dataframe.to_excel(file_path, index=False)

        print(f"Excel exported successfully: {file_path}")

        return file_path

    def export_csv(self, dataframe):

        filename = (
            f"apollo_leads_{datetime.now():%Y%m%d_%H%M%S}.csv"
        )

        file_path = self.output_dir / filename

        dataframe.to_csv(
            file_path,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"CSV exported successfully: {file_path}")

        return file_path

    def export_all(self, companies, employees):

        dataframe = self.prepare_data(
            companies,
            employees
        )

        if dataframe.empty:
            print("No employee data available to export.")
            return None

        excel_file = self.export_excel(dataframe)
        csv_file = self.export_csv(dataframe)

        return {
            "excel": excel_file,
            "csv": csv_file
        }
 