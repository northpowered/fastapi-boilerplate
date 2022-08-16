from pydantic import BaseModel, EmailStr, ValidationError, EmailError
from typing import Optional
from email_validator import validate_email


# class Foo(BaseModel):
#     email: Optional[EmailStr]


# try:
#     #f2 = Foo(email='wdseded@efef.mm71')
#     EmailStr.validate('dewff@wsfe33.local')

# except ValidationError as ex:
#     print('wrong!')
# except EmailError as ex:
#     print('emailerror')
# else:
#     print(1)



validation = validate_email("dewff@wsfe33.mm71",check_deliverability=False)
print(validation)