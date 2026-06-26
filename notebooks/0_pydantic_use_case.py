
from pydantic import BaseModel, StrictInt, Field, field_validator, model_validator
from typing import List, Literal

class myHome(BaseModel):
    floor : StrictInt = Field( ..., gt= 8, lt= 16,description = "Floor of the property")
    address : str = Field( ...,description = "Which Floor")
    dag_no: List[int]
    is_tax_clear : bool = False
    tax_payment_mode : Literal["UPI", "Cash"]

    @field_validator("dag_no")
    def check_Valid_Dag_No(cls, value):
        hasError = False
        for item in value:
            if item == 20678:
                hasError = True
                break
        if(hasError) :
            raise ValueError("This is Invalid Dag no")
    
    @model_validator(mode="after")
    def check_Address(self):
        if len(self.address) > 20 or len(self.address) < 5:
            raise ValueError("Address is not valid")


    
home = myHome(address = "Kolkata, West Bengal.", floor=  12, tax_payment_mode= "Cash",dag_no=[20135,20688,678])

print(home.floor , home.address, home.is_tax_clear, home.dag_no,home.tax_payment_mode)
    
