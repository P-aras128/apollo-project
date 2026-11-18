
from src.services.company_service import CompanyService
from src.services.employee_service import EmployeeService
from src.services.email_enrichment import EmailEnrichmentService
from src.services.export_service import ExportService


def main():

    print("\n======================================")
    print("       APOLLO LEAD GENERATION")
    print("======================================")

    # Initialize services
    company_service = CompanyService()
    employee_service = EmployeeService()
    email_service = EmailEnrichmentService()
    export_service = ExportService()

    # Companies input
    companies = [
        {
            "company_name": "Google",
            "domain": "google.com"
        },
        {
            "company_name": "Microsoft",
            "domain": "microsoft.com"
        }
    ]

    # STEP 1: Company Search
    print("\n[1] COMPANY SEARCH STARTED\n")

    company_results = company_service.search_multiple_companies(
        companies
    )

    successful_companies = [
        result for result in company_results
        if not result.get("error")
    ]

    print(f"\nCompanies searched: {len(successful_companies)}")

    # STEP 2: Employee Search
    print("\n[2] EMPLOYEE SEARCH STARTED\n")

    employee_results = employee_service.search_multiple_companies(
        companies
    )

    all_employees = []

    for result in employee_results:

        if result.get("error"):
            continue

        company = result.get("company", {})
        response = result.get("response", {})

        people = response.get("people", [])

        for person in people:

            if not isinstance(person, dict):
                continue

            employee = person.copy()
            employee["_company"] = company

            all_employees.append(employee)

    print(f"\nTotal employees found: {len(all_employees)}")

    # STEP 3: Email Enrichment
    print("\n[3] EMAIL ENRICHMENT STARTED\n")

    enriched_employees = email_service.enrich_employees(
        all_employees
    )

    print(
        f"\nTotal enriched employees: "
        f"{len(enriched_employees)}"
    )

    # STEP 4: Attach company information
    for employee in enriched_employees:

        employee_name = (
            employee.get("name") or
            " ".join(filter(None, [
                employee.get("first_name"),
                employee.get("last_name")
            ]))
        ).strip().lower()

        linkedin = employee.get("linkedin_url")

        matched_company = None

        for original in all_employees:

            original_name = (
                original.get("name") or
                " ".join(filter(None, [
                    original.get("first_name"),
                    original.get("last_name")
                ]))
            ).strip().lower()

            if linkedin and original.get("linkedin_url") == linkedin:
                matched_company = original.get("_company")
                break

            if employee_name and original_name == employee_name:
                matched_company = original.get("_company")

        if matched_company:
            employee["company"] = matched_company

    # STEP 5: Export Excel and CSV
    print("\n[4] EXPORTING DATA\n")

    export_results = export_service.export_all(
        companies,
        enriched_employees
    )

    if export_results:
        print("\nExport completed successfully!")

    print("\n======================================")
    print("       AUTOMATION COMPLETED")
    print("======================================")


if __name__ == "__main__":
    main()
  