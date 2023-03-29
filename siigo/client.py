import json

import requests

from siigo.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    URL = "https://api.siigo.com/"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, email: str = None, access_key: str = None, token: str = None):
        self.email = email
        self.access_key = access_key
        if token is not None:
            self.headers.update(Authorization=token)

    def generate_token(self):
        body = {"username": self.email, "access_key": self.access_key}
        return self.post("auth", data=json.dumps(body))

    def set_token(self, access_token):
        self.headers.update(Authorization=access_token)

    def list_users(self, page_size: str = None, page: str = None):
        args = locals()
        params = {}
        for arg in args:
            if args[arg] is not None and arg != "self":
                params.update({arg: args[arg]})
        return self.get("v1/users", params=params)

    def list_products(
        self,
        code: str = None,
        created_start: str = None,
        created_end: str = None,
        updated_start: str = None,
        updated_end: str = None,
        id: str = None,
        page_size: str = None,
        page: str = None,
    ):
        """
        date formats: 'yyyy-MM-dd' or 'yyyy-MM-ddTHH:mm:ssZ'
        id: Is possible to filter multiple ids at the same time separated by commas.
        page_size limit = 100
        """
        args = locals()
        params = {}
        for arg in args:
            if args[arg] is not None and arg != "self":
                params.update({arg: args[arg]})
        return self.get("v1/products", params=params)

    def create_product(
        self,
        code: str,
        name: str,
        account_group: int,
        type: str,
        stock_control: bool = None,
        active: bool = None,
        tax_classification: str = None,
        tax_included: bool = None,
        tax_consumption_value: int = None,
        taxes: list = None,
        prices: list = None,
        unit: str = None,
        unit_label: str = None,
        reference: str = None,
        description: str = None,
        additional_fields: dict = None,
    ):
        """
        Request attributes: \n
        code: must be a unique value \n
        account_group: account group id, get list from: list_account_groups() \n
        type: options are 'Product', 'Service' or 'ConsumerGood' \n
        tax_classification: options are 'Taxed', 'Exempt' or 'Excluded' \n
        taxes: list of dictionaries with the following structure:
        [{"id": "1234"}] \n
        prices: list of dictionaries with the following structure: \n
        [
            {
                "currency_code": "COP",
                "price_list": [{"position": 1,"value": 12000}]
            }
        ]
        unit: check siigo measure unit codes: https://siigoapi.docs.apiary.io/#reference/productos/crear-producto/crear-producto \n
        additional_fields: current options are: barcode, brand, tariff and model. Example: \n
        {"barcode": "B0123", "brand": "Gef", "tariff": "151612", "model": "Loiry"}
        """
        args = locals()
        body = {}
        for arg in args:
            if args[arg] is not None and arg != "self":
                body.update({arg: args[arg]})
        return self.post("v1/products", data=json.dumps(body))

    def list_customers(
        self,
        identification: str = None,
        branch_office: int = None,
        created_start: str = None,
        created_end: str = None,
        updated_start: str = None,
        updated_end: str = None,
        page_size: str = None,
        page: str = None,
    ):
        """
        date formats: 'yyyy-MM-dd' or 'yyyy-MM-ddTHH:mm:ssZ'.
        page_size limit = 100
        """
        args = locals()
        params = {}
        for arg in args:
            if args[arg] is not None and arg != "self":
                params.update({arg: args[arg]})
        return self.get("v1/customers", params=params)

    def create_customer(
        self,
        person_type: str,
        id_type: str,
        name: list,
        identification: str,
        contacts: list,
        check_digit: str = None,
        type: str = None,
        commercial_name: str = None,
        branch_office: int = None,
        active: bool = None,
        vat_responsible: bool = None,
        fiscal_responsibilities: list = None,
        address: dict = None,
        phones: list = None,
        comments: str = None,
        related_users: dict = None,
    ):
        """
        Request attributes: \n
        person_type: options are "Person" or "Company" \n
        id_type: check siigo id types: https://siigoapi.docs.apiary.io/#reference/clientes/crear-cliente/crear-cliente \n
        name: if person type is "Company" list with just one value, if person type is "Person" list with two values \n
        contacts: list of dictionaries with the following structure: \n
        [
            {
            "first_name": "Marcos",
            "last_name": "Castillo",
            "email": "marcos.castillo@contacto.com",
            "phone": {"indicative": "57", "number": "3006003345", "extension": "132"}
            }
        ]
        type: options are "Customer", "Supplier" or "Other" \n
        fiscal_responsibilities: options are "R-99-PN", "O-13", "O-15", "O-23" or "O-47" \n
        address: object with the following structure: \n
        {
            "address": "Cra. 18 #79A - 42",
            "city": {"country_code": "Co", "state_code": "19", "city_code": "19001"},
            "postal_code": "110911"
        } \n
        phones: list of dictionaries with the following structure:
        [{"indicative": "57", "number": "3006003345", "extension": "132"}] \n
        related_users: dictionary with two values "seller_id" and "collector_id",
        Example: {"seller_id": 629, "collector_id": 629}
        """
        args = locals()
        body = {}
        for arg in args:
            if args[arg] is not None and arg != "self":
                body.update({arg: args[arg]})
        return self.post("v1/customers", data=json.dumps(body))

    def create_invoice(
        self,
        document: dict,
        date: str,
        customer: dict,
        seller: int,
        items: list,
        payments: list,
        cost_center: int = None,
        currency: dict = None,
        observations: str = None,
        additional_fields: dict = None,
    ):
        """
        document: document type id. Dict with the following structure: {"id": 24446} \n
        date: yyyy-MM-dd format \n
        customer: customer identification and branch_office - {"identification": "13832081", "branch_office": 0} \n
        seller: seller id \n
        items: list of items with the following structure: \n
        [
            {
                "code": "Item-1", # must be a valid code.
                "description": "Camiseta de algodón",
                "quantity": 1,
                "price": 1069.77,
                "discount": 0,
                "taxes": [{"id": 13156}]
            }
        ] \n
        payments: list with the following structure: [{"id": 5636, "value": 1273.03, "due_date": "2021-03-19"}] \n
        currency: only for foreign exchange currency: {"code": "USD", "exchange_rate": 3825.03} \n
        Note: The total payments must be equal to the total invoice.
        """
        args = locals()
        body = {}
        for arg in args:
            if args[arg] is not None and arg != "self":
                body.update({arg: args[arg]})
        return self.post("v1/invoices", data=json.dumps(body))

    def list_group_accounts(self):
        return self.get("v1/account-groups")

    def list_taxes(self):
        return self.get("v1/taxes")

    def list_price_lists(self):
        return self.get("v1/price-lists")

    def list_cost_centers(self):
        return self.get("v1/cost-centers")

    def list_document_types(self, doc_type: str):
        """
        doc_type: options are "FV", "NC" or "RC"
        """
        params = {"type": doc_type}
        return self.get("v1/document-types", params=params)

    def list_payment_types(self, doc_type: str):
        """
        doc_type: options are "FV", "NC" or "RC"
        """
        params = {"document_type": doc_type}
        return self.get("v1/payment-types", params=params)

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def put(self, endpoint, **kwargs):
        response = self.request("PUT", endpoint, **kwargs)
        return self.parse(response)

    def patch(self, endpoint, **kwargs):
        response = self.request("PATCH", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, headers=None, **kwargs):

        if headers:
            self.headers.update(headers)
        return requests.request(method, self.URL + endpoint, headers=self.headers, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r
