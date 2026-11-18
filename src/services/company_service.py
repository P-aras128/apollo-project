
from src.api.apollo_client import ApolloClient
from urllib.parse import urlparse


class CompanyService:

    def __init__(self):
        self.client = ApolloClient()

    def clean_domain(self, domain):

        if not domain:
            return None

        domain = domain.strip().lower()

        if "://" in domain:
            domain = urlparse(domain).netloc

        return domain.removeprefix("www.")

    def search_company(
        self,
        company_name=None,
        domain=None,
        page=1,
        per_page=10
    ):

        params = {
            "page": page,
            "per_page": per_page
        }

        if company_name:
            params["q_organization_name"] = company_name.strip()

        if domain:
            params["q_organization_domains_list[]"] = (
                self.clean_domain(domain)
            )

        if not company_name and not domain:
            raise ValueError(
                "Company name or domain is required."
            )

        response = self.client.request(
            method="POST",
            endpoint="mixed_companies/search",
            params=params
        )

        return response

    def search_multiple_companies(self, companies):

        results = []

        for company in companies:

            name = company.get("company_name")
            domain = company.get("domain")

            if not name and not domain:
                continue

            print(f"Searching company: {name or domain}")

            try:
                response = self.search_company(
                    company_name=name,
                    domain=domain
                )

                results.append({
                    "input": company,
                    "response": response
                })

            except Exception as error:

                print(f"Search failed: {error}")

                results.append({
                    "input": company,
                    "error": str(error)
                })

        return results
 