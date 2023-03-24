# siigo-python
![](https://img.shields.io/badge/version-0.1.0-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*siigo-python* is an API wrapper for Siigo (accounting software), written in Python

## Installing
```
pip install siigo-python
```
## Usage
* If you don't have an access token:
```python
from siigo.client import Client
client = Client(email, access_key)
```
1. **Generate access token**
```python
response = client.generate_token()
```
2. **Set token**
```python
client.set_token(access_token)
```
* If you already have an access token:
```python
from siigo.client import Client
client = Client(token=access_token)
```
### Users
#### - List users
```python
users = client.list_users()
```
### Products
#### - Create product
```python
product = client.create_product("AAAAA111233", "PS6", 1254, "Product")
# code: must be a unique value
# account_group: account group id, get list from: list_account_groups()
# type: options are 'Product', 'Service' or 'ConsumerGood'
# tax_classification: options are 'Taxed', 'Exempt' or 'Excluded'
# taxes: list of dictionaries with the following structure:
#   [{"id": "1234"}]
# prices: list of dictionaries with the following structure:
#   [{"currency_code": "COP", "price_list": [{"position": 1,"value": 12000}]}]
# unit: check siigo measure unit codes: https://siigoapi.docs.apiary.io/#reference/productos/crear-producto/crear-producto
# additional_fields: current options are: barcode, brand, tariff and model. Example:
#   {"barcode": "B0123", "brand": "Gef", "tariff": "151612", "model": "Loiry"}
```
### Customers
#### - Create customer
```python
customer = client.create_customer(
    "Person", 
    "13", 
    ["Juan Carlos", "Rios"], 
    "1019300200",
    [{"first_name": "Juan", "last_name": "Rios", "email": "juan.rios@contact.com",}]
)
# person_type: options are "Person" or "Company"
# id_type: check siigo id types: https://siigoapi.docs.apiary.io/#reference/clientes/crear-cliente/crear-cliente
# name: if person type is "Company" list with just one value, if person type is "Person" list with two values
# contacts: list of dictionaries with the following structure:
#   [
#     {
#     "first_name": "Marcos",
#     "last_name": "Castillo",
#     "email": "marcos.castillo@contacto.com", 
#     "phone": {"indicative": "57", "number": "3006003345", "extension": "132"}
#     }
#   ]
# type: options are "Customer", "Supplier" or "Other"
# fiscal_responsibilities: options are "R-99-PN", "O-13", "O-15", "O-23" or "O-47"
# address: object with the following structure:
#   {
#     "address": "Cra. 18 #79A - 42",
#     "city": {"country_code": "Co", "state_code": "19", "city_code": "19001"},
#     "postal_code": "110911"
#   }
# phones: list of dictionaries with the following structure:
#   [{"indicative": "57", "number": "3006003345", "extension": "132"}]
# related_users: dictionary with two values "seller_id" and "collector_id"
#   Example: {"seller_id": 629, "collector_id": 629}
```
### Catalogues
#### - List group accounts
```python
groups = client.list_group_accounts()
```
#### - List taxes
```python
taxes = client.list_taxes()
```
#### - List price lists
```python
price_lists = client.list_price_lists()
```
#### - List cost centers
```python
cost_centers = client.list_cost_centers()
```