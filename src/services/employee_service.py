
from src.api.apollo_client import ApolloClient


class EmployeeService:

    def __init__(self):
        self.client = ApolloClient()

    def search_employees(
        self,
        domain,
        titles=None,
        seniorities=None,
        page=1,
        per_page=10
    ):

        if not domain:
            raise ValueError("Company domain is required.")

        if titles is None:
            titles = [
                "CEO",
                "Founder",
                "Co-Founder",
                "Managing Director",
                "Director",
                "Manager",
                "VP"
            ]

        if seniorities is None:
            seniorities = [
                "owner",
                "founder",
                "c_suite",
                "vp",
                "director",
                "manager"
            ]

        params = {
            "q_organization_domains_list[]": domain.strip().lower(),
            "person_titles[]": titles,
            "person_seniorities[]": seniorities,
            "page": page,
            "per_page": per_page
        }

        response = self.client.request(
            method="POST",
            endpoint="mixed_people/api_search",
            params=params
        )

        return response

    def search_multiple_companies(
        self,
        companies,
        titles=None,
        seniorities=None
    ):

        results = []

        for company in companies:

            domain = company.get("domain")

            if not domain:
                print(
                    f"Skipping {company.get('company_name', 'Unknown')}: "
                    "Domain missing."
                )
                continue

            print(f"Searching employees: {domain}")

            try:

                response = self.search_employees(
                    domain=domain,
                    titles=titles,
                    seniorities=seniorities
                )

                results.append({
                    "company": company,
                    "response": response
                })

            except Exception as error:

                print(f"Employee search failed: {error}")

                results.append({
                    "company": company,
                    "error": str(error)
                })

        return results
 