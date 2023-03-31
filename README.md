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
# page_size limit = 100
users = client.list_users(page_size=25, page=1)
```
### Products
#### - List products
```python
# filter options: code, created_start, created_end, updated_start, updated_end, id, page_size, page
# date formats: 'yyyy-MM-dd' or 'yyyy-MM-ddTHH:mm:ssZ'
# id: It is possible to filter multiple ids at the same time separated by commas.
# page_size limit = 100
products = client.list_products(created_start="2023-01-01")
```
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
#### - List customers
```python
# filter options: identification, branch_office, created_start, created_end, updated_start, updated_end, page_size, page
# date formats: 'yyyy-MM-dd' or 'yyyy-MM-ddTHH:mm:ssZ'
# page_size limit = 100
customers = client.list_customers(created_start="2023-01-01")
```
#### - Create customer
```python
customer = client.create_customer(
    "Person", 
    "13", 
    ["Juan Carlos", "Rios"], 
    [{"first_name": "Juan", "last_name": "Rios", "email": "juan.rios@contact.com",}],
    [{"indicative": "57", "number": "3006113345", "extension": "132"}],
    {
        "address": "Calle 47 Bis A 28-55",
        "city": {"country_code": "co", "state_code": "19", "city_code": "19001"},
        "postal_code": "110911",
    },
    "1019300200",
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
# phones: list of dictionaries with the following structure:
#   [{"indicative": "57", "number": "3006003345", "extension": "132"}]
# address: object with the following structure:
#   {
#     "address": "Cra. 18 #79A - 42",
#     "city": {"country_code": "Co", "state_code": "19", "city_code": "19001"},
#     "postal_code": "110911"
#   }
# type: options are "Customer", "Supplier" or "Other"
# fiscal_responsibilities: options are "R-99-PN", "O-13", "O-15", "O-23" or "O-47"
# related_users: dictionary with two values "seller_id" and "collector_id"
#   Example: {"seller_id": 629, "collector_id": 629}
```
### Invoices
#### Create Invoice
```python
fv = client.create_invoice(
    {"id": 24446},
    "2023-02-02",
    {"identification": "1040570645", "branch_office": 0},
    1018,
    [{ "code": "DEX6360", "description": "Shirt", "quantity": 1, "price": 8000.00, "discount": 0}],
    [{"id": 9485, "value": 8000.00, "due_date": "2023-01-01"}] 
)
# document: document type id. Dict with the following structure: {"id": 24446} \n
# date: yyyy-MM-dd format \n
# customer: customer identification and branch_office - {"identification": "13832081", "branch_office": 0} \n
# seller: seller id \n
# items: list of items with the following structure: \n
# [
#     {
#         "code": "Item-1", # must be a valid code.
#         "description": "Camiseta de algodón",
#         "quantity": 1,
#         "price": 1069.77,
#         "discount": 0,
#         "taxes": [{"id": 13156}]
#     }
# ] \n
# payments: list with the following structure: [{"id": 5636, "value": 1273.03, "due_date": "2021-03-19"}] \n
# currency: only for foreign exchange currency: {"code": "USD", "exchange_rate": 3825.03} \n
# Note: The total payments must be equal to the total invoice.
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
#### - List document types
```python
# options are "FV", "NC" or "RC"
doc_types = client.list_document_types("FV")
```
#### - List payment types
```python
# options are "FV", "NC" or "RC"
payments = client.list_payment_types("FV")
```