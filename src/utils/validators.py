
import re
from urllib.parse import urlparse


class DataValidator:

    @staticmethod
    def validate_company_name(name):

        if not name or not isinstance(name, str):
            return False

        return len(name.strip()) >= 2

    @staticmethod
    def validate_domain(domain):

        if not domain or not isinstance(domain, str):
            return False

        domain = domain.strip().lower()

        if "://" in domain:
            domain = urlparse(domain).netloc

        domain = domain.removeprefix("www.")

        pattern = (
            r"^(?=.{1,253}$)"
            r"[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?"
            r"(?:\.[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?)+$"
        )

        return bool(re.match(pattern, domain))

    @staticmethod
    def validate_company(company):

        if not isinstance(company, dict):
            return False

        name = company.get("company_name")
        domain = company.get("domain")

        valid_name = DataValidator.validate_company_name(name)
        valid_domain = DataValidator.validate_domain(domain)

        return valid_name or valid_domain

    @staticmethod
    def validate_companies(companies):

        valid = []
        invalid = []

        for company in companies:

            if DataValidator.validate_company(company):
                valid.append(company)
            else:
                invalid.append(company)

        return {
            "valid": valid,
            "invalid": invalid
        }
 