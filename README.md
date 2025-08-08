# Odoo-Py - Python Library for Odoo ERP Integration

A complete Python library for Odoo ERP integration, specifically developed for pharmaceutical automation and e-commerce operations.

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Available Models](#available-models)
- [Usage Guide](#usage-guide)
- [Practical Examples](#practical-examples)
- [API Reference](#api-reference)
- [Error Handling](#error-handling)

## 🔧 Installation

```bash
pip install odoo-py
```

### Dependencies

```bash
pip install environs xmlrpc
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project with the following variables:

```env
ODOO_URL=https://your-odoo.com
ODOO_DB=your_database
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password
ODOO_LANGUAGE=pt_PT
```

### Basic Configuration

```python
from odoo import OdooIntegration

# Using environment variables
odoo = OdooIntegration()

# Or manual configuration
odoo = OdooIntegration(
    odoo_url="https://your-odoo.com",
    odoo_db="your_database",
    odoo_username="your_username",
    odoo_password="your_password",
    odoo_language="pt_PT"
)
```

## 🏗️ Available Models

### Core

- **`OdooIntegration`** - Base class for all integrations
- **`PartnerModel`** - Partner/contact management
- **`SaleOrderModel`** - Sales orders
- **`PurchaseOrderModel`** - Purchase orders
- **`ProductModel`** - Products
- **`StockModel`** - Stock and warehouse management

### Support

- **`CountryModel`** - Countries and states
- **`CompanyModel`** - Companies
- **`AccountMoveModel`** - Accounting moves/invoices
- **`UserModel`** - Users
- **`PaymentTermModel`** - Payment terms

### Specialized

- **`ProductTemplateModel`** - Product templates
- **`ProductCategoryModel`** - Product categories
- **`PartnerCategoryModel`** - Partner categories
- **`CRMTagModel`** - CRM tags
- **`AnalyticAccountModel`** - Analytic accounts
- **`AccountTaxModel`** - Taxes
- **`AccountInvoiceModel`** - Invoices

## 🎯 Usage Guide

### 1. Partner/Contact Management

```python
from odoo import PartnerModel

partner_model = PartnerModel()

# Search partner by VAT/NIF
filter_partner = [["vat", "=", "123456789"], ["is_company", "=", True]]
partners = partner_model.get_and_read_partners_by_any_filter(
    filter=filter_partner, 
    fields=["id", "name", "email"]
)

# Create new partner
partner_data = {
    "name": "Central Pharmacy",
    "street": "Main Street, 123",
    "city": "Lisbon",
    "state_id": 1,
    "country_id": 181,  # Portugal
    "zip": "1000-001",
    "vat": "123456789",
    "phone": "+351912345678",
    "email": "contact@centralpharmacy.pt",
    "is_company": True,
    "lang": "pt_PT"
}
partner_id = partner_model.create_partner_from_scratch(partner_data)

# Update partner
partner_model.update_partner(partner_id, {"phone": "+351987654321"})
```

### 2. Sales Orders

```python
from odoo import SaleOrderModel

sale_model = SaleOrderModel()

# Create sales order
sale_order_data = {
    "partner_id": 123,
    "company_id": 1,
    "warehouse_id": 1,
    "analytic_account_id": 1,
    "origin": "WEB-001",
    "client_order_ref": "REF-2024-001"
}
sale_order_id = sale_model.create_sale_order(sale_order_data)

# Add line to order
sale_line_data = {
    "order_id": sale_order_id,
    "product_id": 456,
    "product_uom_qty": 10,
    "price_unit": 15.50,
    "discount": 5.0
}
sale_model.create_sale_order_line(sale_line_data)

# Confirm order
sale_model.confirm_sale_order(sale_order_id)

# Certify order (if needed)
sale_model.certify_sale_order(sale_order_id)

# Create invoice
sale_model.create_invoice_from_sale_order(sale_order_id)
```

### 3. Stock Management

```python
from odoo import StockModel

stock_model = StockModel()

# Search warehouse by name
warehouse_id = stock_model.get_warehouse_id_by_name("Main Warehouse", company_id=1)

# Create product lot
lot_id = stock_model.create_product_lot(
    product_id=123,
    serie_number="LOT2024001",
    company_id=1,
    expiration_date="2025-12-31",
    removal_date="2025-11-30",
    alert_date="2025-10-31",
    use_date="2025-09-30"
)

# Validate picking/delivery
picking_ids = stock_model.get_picking_id_list_by_sale_order_id(sale_order_id)
for picking_id in picking_ids:
    stock_model.validate_picking(picking_id)
```

### 4. Products

```python
from odoo import ProductModel

product_model = ProductModel()

# Search product by reference
try:
    product_id = product_model.get_product_id_by_reference("REF-PROD-001")
    product_data = product_model.get_product_by_id(product_id)
    print(f"Product found: {product_data[0]['name']}")
except ProductNotFoundError:
    print("Product not found")
```

## 📚 Practical Examples

### Example 1: Create Contact and Complete Order

```python
from odoo import PartnerModel, SaleOrderModel, CompanyModel, StockModel
from odoo import CountryModel, AnalyticAccountModel, PaymentTermModel

def create_complete_order():
    # Initialize models
    partner_model = PartnerModel()
    sale_model = SaleOrderModel()
    country_model = CountryModel()
    company_model = CompanyModel()
    stock_model = StockModel()
    analytic_model = AnalyticAccountModel()
    payment_model = PaymentTermModel()
    
    # 1. Get necessary IDs
    country_id = country_model.get_country_id_by_name("Portugal")
    state_id = country_model.get_country_state_id_by_name("Lisboa")
    company_id = company_model.get_company_id_by_name("ADDO PHARM")
    warehouse_id = stock_model.get_warehouse_id_by_name("Central Warehouse", company_id)
    analytic_id = analytic_model.get_analytic_account_id_by_name("Online Sales")
    payment_term_id = payment_model.get_payment_term_id_by_name("30 days")
    
    # 2. Create contact
    contact_data = {
        "name": "New Pharmacy",
        "street": "Liberty Avenue, 200",
        "city": "Lisbon",
        "state_id": state_id,
        "country_id": country_id,
        "zip": "1000-200",
        "vat": "987654321",
        "phone": "+351911223344",
        "email": "contact@newpharmacy.pt",
        "is_company": True,
        "x_studio_tipo_de_contacto_1": "Farmácia",
        "x_studio_cdigo_anf_1": "ANF001",
        "x_studio_nome_da_farmcia_1": "New Pharmacy",
        "lang": "pt_PT"
    }
    partner_id = partner_model.create_partner_from_scratch(contact_data)
    
    # 3. Create sales order
    sale_data = {
        "partner_id": partner_id,
        "company_id": company_id,
        "warehouse_id": warehouse_id,
        "analytic_account_id": analytic_id,
        "payment_term_id": payment_term_id,
        "origin": "WEB-2024-001",
        "client_order_ref": "NEW-PHARM-001"
    }
    sale_order_id = sale_model.create_sale_order(sale_data)
    
    # 4. Add products
    products = [
        {"product_id": 123, "qty": 5, "price": 12.50},
        {"product_id": 124, "qty": 2, "price": 35.00}
    ]
    
    for product in products:
        line_data = {
            "order_id": sale_order_id,
            "product_id": product["product_id"],
            "product_uom_qty": product["qty"],
            "price_unit": product["price"]
        }
        sale_model.create_sale_order_line(line_data)
    
    # 5. Confirm order
    sale_model.confirm_sale_order(sale_order_id)
    
    return {
        "partner_id": partner_id,
        "sale_order_id": sale_order_id,
        "message": "Order created successfully!"
    }

# Execute example
result = create_complete_order()
print(result)
```

### Example 2: Purchase Order Processing

```python
from odoo import PurchaseOrderModel, PartnerModel, StockModel

def process_purchase_order():
    purchase_model = PurchaseOrderModel()
    partner_model = PartnerModel()
    stock_model = StockModel()
    
    # Search supplier
    supplier_filter = [["supplier_rank", ">", 0], ["name", "ilike", "Supplier XYZ"]]
    suppliers = partner_model.get_and_read_partners_by_any_filter(
        filter=supplier_filter,
        fields=["id", "name"]
    )
    
    if not suppliers:
        print("Supplier not found")
        return
    
    supplier_id = suppliers[0]["id"]
    
    # Create purchase order
    purchase_data = {
        "partner_id": supplier_id,
        "company_id": 1,
        "payment_term_id": 1,
        "picking_type_id": 1,
        "partner_ref": "PO-2024-001"
    }
    
    purchase_id = purchase_model.create_purchase_order(purchase_data)
    
    # Add lines
    line_data = {
        "order_id": purchase_id,
        "product_id": 789,
        "product_qty": 100,
        "price_unit": 8.75
    }
    purchase_model.create_purchase_order_line(line_data)
    
    return purchase_id

purchase_id = process_purchase_order()
print(f"Purchase order created: {purchase_id}")
```

### Example 3: Invoice Management

```python
from odoo import AccountMoveModel, SaleOrderModel

def process_invoice(sale_order_id):
    sale_model = SaleOrderModel()
    account_model = AccountMoveModel()
    
    # Create invoice from order
    sale_model.create_invoice_from_sale_order(sale_order_id)
    
    # Get created invoice ID
    invoice_id = sale_model.get_invoice_id_from_sale_order(sale_order_id)
    
    # Add footer notes
    footer_notes = "Thank you for your preference! Validity: 30 days"
    account_model.invoice_insert_footer_notes(invoice_id, footer_notes)
    
    # Confirm invoice
    account_model.confirm_invoice_purchase_order(invoice_id)
    
    return invoice_id
```

## 📖 API Reference

### OdooIntegration (Base Class)

#### Main Methods

- **`search(model, search_params)`** - Search records
- **`search_read(model, search_params, fields, limit, offset)`** - Search and read records
- **`search_count(model, search_params)`** - Count records
- **`read(model, ids, fields)`** - Read specific records
- **`create(model, data)`** - Create new records
- **`update(model, object_id, data)`** - Update records
- **`execute_action(model, action_type, object_id, extra_context)`** - Execute actions

### PartnerModel

#### Specific Methods

- **`get_partner_by_id(partner_id, fields=None)`**
- **`get_partner_id_by_name(partner_name)`**
- **`create_partner_from_scratch(partner_data)`**
- **`update_partner(partner_id, partner_data)`**
- **`get_and_read_all_partners(fields=None, limit=10, offset=0)`**
- **`get_and_read_partners_by_any_filter(filter, fields=None, limit=10, offset=0)`**
- **`count_partners_by_any_filter(filter=None)`**
- **`action_archive_partner(partner_id)`**

### SaleOrderModel

#### Specific Methods

- **`get_sale_order_by_id(sale_order_id, fields=None)`**
- **`get_sale_order_by_state(state)`**
- **`create_sale_order(sale_order_data)`**
- **`create_sale_order_line(sale_order_line_data)`**
- **`confirm_sale_order(sale_order_id)`**
- **`certify_sale_order(sale_order_id)`**
- **`create_invoice_from_sale_order(sale_order_id)`**
- **`get_invoice_id_from_sale_order(sale_order_id)`**

### PurchaseOrderModel

#### Specific Methods

- **`get_purchase_order_by_id(purchase_order_id, fields=None)`**
- **`get_purchase_order_by_state(state)`**
- **`create_purchase_order(purchase_order_data)`**
- **`create_purchase_order_line(purchase_order_line_data)`**
- **`create_invoice_from_purchase_order(purchase_order_id)`**

### StockModel

#### Specific Methods

- **`get_warehouse_id_by_name(warehouse_name, company_id)`**
- **`create_product_lot(product_id, serie_number, company_id, expiration_date, ...)`**
- **`get_product_lot_id_by_serie_name_and_product_id(serie_name, product_id, company_id)`**
- **`validate_picking(picking_id)`**
- **`get_picking_id_list_by_sale_order_id(sale_order_id)`**
- **`get_picking_id_list_by_purchase_order_id(purchase_order_id)`**

### ProductModel

#### Specific Methods

- **`get_product_by_id(product_id)`**
- **`get_product_id_by_reference(reference_id)`**

### CountryModel

#### Specific Methods

- **`get_country_id_by_code(country_code)`**
- **`get_country_id_by_name(country_name)`**
- **`get_country_state_id_by_name(state_name)`**

### CompanyModel

#### Specific Methods

- **`get_company_by_id(company_id)`**
- **`get_company_id_by_name(company_name)`**

### AccountMoveModel

#### Specific Methods

- **`get_invoice_by_id(invoice_id)`**
- **`create_account_move(account_move_data)`**
- **`update_account_move(account_move_id, data)`**
- **`invoice_insert_footer_notes(invoice_id, notes)`**
- **`confirm_invoice_purchase_order(invoice_id)`**

## 🔍 Common Filters

### Filter Examples

```python
# Search by VAT
filter_vat = [["vat", "=", "123456789"]]

# Search active companies
filter_companies = [["is_company", "=", True], ["active", "=", True]]

# Search by date
filter_date = [["create_date", ">=", "2024-01-01"]]

# Multiple conditions (AND)
filter_complex = [
    ["vat", "=", "123456789"], 
    ["is_company", "=", True],
    ["active", "=", True]
]

# OR conditions
filter_or = ["|", ["name", "ilike", "Pharmacy"], ["name", "ilike", "Clinic"]]

# Available operators
# =, !=, >, >=, <, <=, like, ilike, in, not in
```

### Pharmacy-Specific Filters

```python
# Search pharmacies
filter_pharmacy = [
    ["x_studio_tipo_de_contacto_1", "=", "Farmácia"],
    ["is_company", "=", True]
]

# Search by ANF code
filter_anf = [["x_studio_cdigo_anf_1", "=", "12345"]]

# Sales orders in specific state
filter_sale_orders = [["state", "in", ["draft", "sent", "sale"]]]

# Products with low stock
filter_low_stock = [["qty_available", "<=", 10]]
```

## ⚠️ Error Handling

### Custom Exceptions

```python
from odoo.exceptions import ProductNotFoundError, LotProductNotFoundError, TooManyLotProducError

try:
    product_id = product_model.get_product_id_by_reference("REF-001")
except ProductNotFoundError as e:
    print(f"Product not found: {e}")

try:
    lot_id = stock_model.get_product_lot_id_by_serie_name_and_product_id("LOT001", 123)
except LotProductNotFoundError as e:
    print(f"Lot not found: {e}")
except TooManyLotProducError as e:
    print(f"Multiple lots found: {e}")
```

### Generic Error Handling

```python
import xmlrpc.client

try:
    partner_id = partner_model.create_partner_from_scratch(partner_data)
except xmlrpc.client.Fault as e:
    print(f"Odoo error: {e.faultString}")
    if "already exists" in e.faultString:
        print("Duplicate record")
    elif "access denied" in e.faultString:
        print("Insufficient permissions")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Retry Logic Example

```python
import time
from functools import wraps

def retry_on_error(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry_on_error(max_retries=3)
def create_partner_with_retry(partner_data):
    partner_model = PartnerModel()
    return partner_model.create_partner_from_scratch(partner_data)
```

## 🔐 Security

### Best Practices

1. **Never commit credentials** to code
2. **Use environment variables** for sensitive configuration
3. **Validate data** before sending to Odoo
4. **Implement retry logic** for critical operations
5. **Log important operations** for auditing

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_safe_partner(partner_data):
    # Validate required fields
    required_fields = ["name", "vat"]
    for field in required_fields:
        if not partner_data.get(field):
            raise ValueError(f"Required field missing: {field}")
    
    # Validate Portuguese VAT
    vat = partner_data["vat"]
    if not vat.isdigit() or len(vat) != 9:
        raise ValueError("VAT must have 9 numeric digits")
    
    # Sanitize data
    partner_data["name"] = partner_data["name"].strip()
    partner_data["email"] = partner_data.get("email", "").lower().strip()
    
    logger.info(f"Creating partner: {partner_data['name']} - VAT: {vat}")
    
    try:
        partner_model = PartnerModel()
        partner_id = partner_model.create_partner_from_scratch(partner_data)
        logger.info(f"Partner created successfully. ID: {partner_id}")
        return partner_id
    except Exception as e:
        logger.error(f"Error creating partner: {e}")
        raise
```

## 🚀 Performance

### Optimization Tips

```python
# 1. Use specific fields in queries
fields = ["id", "name", "vat"]  # Only necessary fields
partners = partner_model.get_and_read_partners_by_any_filter(
    filter=filter_data, 
    fields=fields,
    limit=100
)

# 2. Batch operations when possible
partner_data_list = [partner1_data, partner2_data, partner3_data]
# Instead of creating one by one, use create with list (when supported)

# 3. Cache frequently used data
country_cache = {}

def get_cached_country_id(country_name):
    if country_name not in country_cache:
        country_model = CountryModel()
        country_cache[country_name] = country_model.get_country_id_by_name(country_name)
    return country_cache[country_name]

# 4. Use limit and offset for pagination
offset = 0
limit = 100
while True:
    partners = partner_model.get_and_read_all_partners(
        fields=["id", "name"], 
        limit=limit, 
        offset=offset
    )
    if not partners:
        break
    
    # Process partners
    for partner in partners:
        process_partner(partner)
    
    offset += limit
```

## 🧪 Testing

### Unit Test Example

```python
import unittest
from unittest.mock import Mock, patch
from odoo import PartnerModel

class TestPartnerModel(unittest.TestCase):
    
    def setUp(self):
        self.partner_model = PartnerModel()
    
    @patch('odoo._integration.xmlrpc.client.ServerProxy')
    def test_create_partner_success(self, mock_proxy):
        # Mock Odoo response
        mock_proxy.return_value.execute_kw.return_value = [123]
        
        partner_data = {
            "name": "Test Pharmacy",
            "vat": "123456789"
        }
        
        result = self.partner_model.create_partner_from_scratch(partner_data)
        self.assertEqual(result, [123])
    
    @patch('odoo._integration.xmlrpc.client.ServerProxy')
    def test_get_partner_not_found(self, mock_proxy):
        # Mock empty response
        mock_proxy.return_value.execute_kw.return_value = []
        
        with self.assertRaises(Exception) as context:
            self.partner_model.get_partner_id_by_name("Does Not Exist")
        
        self.assertIn("not found", str(context.exception))

if __name__ == '__main__':
    unittest.main()
```

## 📦 Deployment

### Example Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH="/app"

CMD ["python", "main.py"]
```

### requirements.txt

```txt
odoo-py
environs
pymssql
```

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, open an issue on GitHub or contact the development team.

---

**Developed with ❤️ for pharmaceutical automation**