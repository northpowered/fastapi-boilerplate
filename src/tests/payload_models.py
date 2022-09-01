from pydantic import BaseModel
from mimesis import Person

good_email_domains: list[str] = ['mydomain.com']
bad_email_domains: list[str] = ['mydomain.com1']


class UserModel(BaseModel):
    username: str
    password: str
    email: str  # Using str instead of EmailStr to test input validation in CLI and CRUD

    @classmethod
    def create(cls, good_emails: bool = True):
        person: Person = Person('en')
        domains: list[str] = good_email_domains
        if not good_emails:
            domains = bad_email_domains
        return UserModel(
            username=person.username(),
            password=person.password(),
            email=person.email(domains=domains, unique=True)
        )

    def to_cli_input(self):
        return f"{self.username}\n{self.password}\n{self.email}\n"


class RoleModel(BaseModel):
    name: str
    active: bool = True


class GroupModel(BaseModel):
    name: str
    active: bool = True
