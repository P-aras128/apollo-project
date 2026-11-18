
from src.api.apollo_client import ApolloClient


class EmailEnrichmentService:

    def __init__(self):
        self.client = ApolloClient()

    def prepare_person(self, person):

        details = {}

        # Apollo Person ID
        if person.get("id"):
            details["id"] = person["id"]

        # Employee name
        if person.get("first_name"):
            details["first_name"] = person["first_name"]

        if person.get("last_name"):
            details["last_name"] = person["last_name"]

        if person.get("name"):
            details["name"] = person["name"]

        # Company information
        organization = person.get("organization") or {}

        domain = (
            organization.get("primary_domain")
            or organization.get("domain")
            or person.get("domain")
        )

        if domain:
            details["domain"] = domain

        if organization.get("name"):
            details["organization_name"] = organization["name"]

        # LinkedIn profile
        if person.get("linkedin_url"):
            details["linkedin_url"] = person["linkedin_url"]

        if person.get("email"):
            details["email"] = person["email"]

        if not details.get("id") and not (
            details.get("linkedin_url")
            or (
                details.get("first_name")
                and details.get("domain")
            )
            or details.get("email")
        ):
            return None

        return details

    def enrich_employees(self, employees):

        if not employees:
            return []

        results = []

        # Maximum 10 people per API request
        for start in range(0, len(employees), 10):

            batch = employees[start:start + 10]

            details = [
                self.prepare_person(person)
                for person in batch
            ]

            details = [
                person for person in details if person
            ]

            if not details:
                continue

            print(
                f"Enriching batch: {start + 1} "
                f"to {start + len(batch)}"
            )

            response = self.client.request(
                method="POST",
                endpoint="people/bulk_match",
                params={
                    "reveal_personal_emails": "false",
                    "reveal_phone_number": "false"
                },
                json_data={
                    "details": details
                }
            )

            matches = response.get("matches", [])

            for match in matches:

                if match:
                    results.append({
                        "name": match.get("name"),
                        "first_name": match.get("first_name"),
                        "last_name": match.get("last_name"),
                        "email": match.get("email"),
                        "email_status": match.get("email_status"),
                        "title": match.get("title"),
                        "linkedin_url": match.get("linkedin_url"),
                        "match_confidence": match.get("match_confidence")
                    })

        return results
  