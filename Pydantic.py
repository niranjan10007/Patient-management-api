from pydantic import BaseModel, Field, field_validator, model_validator , computed_fields
from typing import List, Dict, Annotated

class Patient(BaseModel):

    name: Annotated[str, Field(
        max_length=50,
        title='Name of the patient',
        description='Give the name of the patient in less than 50 characters'
    )]
    age: int
    weight: float = Field(gt=0)
    height:1.45
    email: str
    married: bool
    allergies: List[str]
    contact_detail: Dict[str, str]

    # 1️ Field Validator for single field
    @field_validator('email')
    def validate_email_domain(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Email domain not valid')
        return value

    # 2️ Model Validator (AFTER all fields validated)
    @model_validator(mode='after')
    def validate_emergency_contact(self):
        # If patient age > 60, emergency contact must exist
        if self.age > 60 and "emergency" not in self.contact_detail:
            raise ValueError('Patient older than 60 must have an emergency contact')
        return self
    @computed_fields
    @property
    def calculate_bmi(self):
        bmi=round(self.weight /(self.height**2),2)
        return bmi

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_detail)
    print(patient.email)

patient_info = {
    'name': 'Niranjan',
    'age': 50,
    'email': 'abc@hdfc.com',
    'weight': 21,
    'married': True,
    'allergies': ['Headache', 'cough'],
    'contact_detail': {'phone': '9999999999'}   # required field
}

# Create model instance
patient1 = Patient(**patient_info)

# Print data
insert_patient_data(patient1)
