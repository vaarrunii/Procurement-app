import csv
import io
import random
from datetime import date, timedelta

# --- Configuration Parameters ---
NUM_SUPPLIERS = 20
NUM_CATEGORIES = 20
NUM_POS_PER_YEAR = 50 # Generates approximately 250 POs over 5 years
NUM_SPEND_ENTRIES_PER_YEAR = 80 # Generates approximately 400 spend entries over 5 years
NUM_PRODUCTS_PRICED = 100 # Total unique product pricing entries
NUM_CONTRACTS = 20 # Total contracts generated
NUM_DISCOUNTS = 30 # Total discounts generated
NUM_ALTERNATE_SUPPLIERS_ENTRIES = 20 # Total alternate supplier pairings

START_DATE = date(2020, 7, 1) # Data starts from July 1, 2020
END_DATE = date(2025, 6, 24) # Data ends on current date

# --- Helper Functions ---
def random_date(start, end):
    """Generates a random date between start and end dates."""
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_csv_string(header, data):
    """Converts a list of lists into a CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(header)
    writer.writerows(data)
    return output.getvalue()

# --- Core Data Definitions (Expanded for Realism) ---

# Supplier Names & Domains
supplier_names = [
    "Steel Dynamics Inc.", "RubberPro Components", "Hydraulic Solutions Ltd.", "Logistics Express Pvt. Ltd.",
    "Office Supply Co.", "Precision Machining Works", "Global Fasteners Inc.", "IT Solutions India",
    "Cleaning Services Pvt. Ltd.", "PowerGen Energy Solutions", "Brake Material Innovators", "Advanced Casting Corp.",
    "Sensor Tech Global", "Bearing Dynamics Corp.", "Elastomer Seals Inc.", "Metal Fab Solutions",
    "Tool & Die Specialists", "Chemicals Unlimited", "Packaging Pro Solutions", "Security Services Co.",
    "Brake Lining Specialists", "Automotive Springs Pvt. Ltd."
]
supplier_domains = [
    "steel-dynamics.com", "rubberpro.com", "hydraulicsol.com", "logisticsexp.com",
    "officesupply.com", "precisionmachining.com", "globalfasteners.com", "itsolutions.in",
    "cleaningservices.com", "powergen.com", "brakeinnovators.com", "advancedcasting.com",
    "sensortech.com", "bearingdynamics.com", "elastomerseals.com", "metalfab.com",
    "toolanddie.com", "chemicalsunlimited.com", "packagingpro.com", "securityco.com",
    "brakelinings.com", "autosprings.com"
]

# Supplier Data Generation
suppliers_data = []
for i in range(1, NUM_SUPPLIERS + 1):
    name = supplier_names[i-1] if i-1 < len(supplier_names) else f"Supplier {i}"
    domain = supplier_domains[i-1] if i-1 < len(supplier_domains) else f"supplier{i}.com"
    email = f"contact@{domain}"
    phone = f"98{random.randint(10000000, 99999999)}"
    address = f"{random.randint(100, 999)} Industrial Rd, {random.choice(['Pune', 'Chennai', 'Gurgaon', 'Bangalore'])}"
    gstin = f"27ABCDE{random.randint(1000, 9999)}F{random.randint(1,9)}Z{random.randint(0,9)}"
    pan = f"ABCDE{random.randint(1000, 9999)}{chr(random.randint(65,90))}"
    score = round(random.uniform(7.0, 9.5), 1)
    type_ = random.choice(["Direct", "Indirect"])
    # Simulate some suppliers becoming inactive over time
    is_active = random.choices([True, False], weights=[0.9, 0.1], k=1)[0] if i > NUM_SUPPLIERS * 0.7 else True
    share_of_business = round(random.uniform(0.01, 0.30), 2) if is_active else 0.00
    lead_time_days = random.randint(5, 45)
    base_currency = random.choice(["INR", "INR", "INR", "USD", "EUR"]) # More INR
    unit_of_measure = random.choice(["KG", "PCS", "LITRE", "METER", "SERVICE", "UNIT"])
    suppliers_data.append([
        i, name, email, phone, address, gstin, pan, score, type_, is_active,
        share_of_business, lead_time_days, base_currency, unit_of_measure
    ])

# Category Data (Hierarchical structure)
categories_data = [
    [1, "Raw Materials", None], [2, "Components", None], [3, "Services", None], [4, "Manufacturing Equipment", None],
    [5, "Steel Alloys", 1], [6, "Rubber & Polymers", 1], [7, "Casting Materials", 1], [8, "Chemicals & Fluids", 1],
    [9, "Brake Caliper Sub-Assemblies", 2], [10, "Brake Pad & Lining Components", 2], [11, "Brake Disc & Drum Components", 2],
    [12, "Hydraulic System Parts", 2], [13, "Fasteners & Hardware", 2], [14, "Sensors & Electronics", 2],
    [15, "Machining & Fabrication", 3], [16, "Logistics & Shipping", 3], [17, "IT & Software Services", 3],
    [18, "Facility Maintenance", 3], [19, "Utilities", 3], [20, "Testing & Certification", 3]
]

# Product Names (Specific for Brake Manufacturing)
product_names_list = [
    "High Carbon Steel Blanks (Front Disc)", "Ductile Iron Ingots (Rear Drum)", "Aluminum Billets (Caliper)",
    "EPDM Rubber Granules (Seal Grade)", "Silicon Carbide Abrasives (Grinding)", "Copper Brake Line Tubing (1/4\")",
    "DOT4 Brake Fluid Base Stock", "Brake Caliper Housing (Front Left)", "Brake Caliper Housing (Front Right)",
    "Brake Pad Backing Plates (Ceramic)", "Brake Disc Casting (Ventilated)", "Hydraulic Brake Hose Assembly (Rear)",
    "ABS Wheel Speed Sensor (Front)", "Brake Master Cylinder Assembly", "Wheel Bearing Unit (Front Axle)",
    "Caliper Piston Seal Kit", "Dust Boot (Caliper Pin)", "Bleeder Screw (M10x1.0)", "Brake Pad Retainer Spring",
    "Ceramic Brake Pad Friction Material Mix", "Semi-Metallic Brake Pad Friction Material Mix",
    "Brake Caliper Piston (Phenolic)", "Caliper Guide Pin (Stainless Steel)", "Brake Rotor Hat (Aluminum)",
    "Drum Brake Shoe Assembly", "Parking Brake Cable Assembly", "Hydraulic Control Unit (HCU) Valve",
    "Brake Booster Diaphragm", "Vacuum Hose (Brake Booster)", "Brake Pedal Assembly Sensor",
    "Brake Light Switch", "Brake Caliper Bleeder Valve Cap", "Brake Caliper Repair Kit (Front)",
    "Wheel Stud (M12x1.5)", "Lug Nut (M12x1.5)", "Anti-Rattle Clip (Brake Pad)", "Brake Assembly Lubricant (High Temp)",
    "Brake Cleaner Spray (Non-Chlorinated)", "Degreaser (Industrial Strength)", "CNC Machining Oil",
    "Heat Treatment Services (Quenching)", "Powder Coating Service (Black)", "Assembly Line Conveyor Belt",
    "Forklift Maintenance Service", "ERP Software License (Annual)", "Cybersecurity Consulting Service",
    "Factory Floor Cleaning Chemicals", "Waste Disposal Services (Hazardous)", "Energy Audit Services",
    "Protective Eyewear", "Hearing Protection Ear Plugs", "Nitrile Gloves (Industrial)",
    "Welding Electrodes (E7018)", "Grinding Discs (4.5 inch)", "Pallets (Wooden, Standard)", "Stretch Wrap Film",
    "Brake Line Connector (Brass)", "Pressure Modulator Valve", "Wear Indicator Sensor", "Brake Fluid Reservoir",
    "Propulsion Shaft Flange", "Differential Oil Seal", "Axle Nut (Self-Locking)", "Spindle Nut Washer",
    "Brake Pad Shim Kit", "Caliper Hardware Kit", "Wheel Cylinder Rebuild Kit", "Return Spring Kit (Drum Brake)"
]

# Map categories to supplier types for more realistic PO/Spend generation
category_supplier_type_map = {
    1: ["Direct"], 2: ["Direct"], 3: ["Indirect"], 4: ["Indirect"], # Parent categories
    5: ["Direct"], 6: ["Direct"], 7: ["Direct"], 8: ["Direct"], # Raw Materials
    9: ["Direct"], 10: ["Direct"], 11: ["Direct"], 12: ["Direct"], 13: ["Direct"], 14: ["Direct"], # Components
    15: ["Indirect", "Direct"], 16: ["Indirect"], 17: ["Indirect"], 18: ["Indirect"], 19: ["Indirect"], 20: ["Indirect", "Direct"] # Services
}

# Get active supplier IDs for linking
active_supplier_ids = [s[0] for s in suppliers_data if s[9] == True]
direct_supplier_ids = [s[0] for s in suppliers_data if s[8] == "Direct" and s[9] == True]
indirect_supplier_ids = [s[0] for s in suppliers_data if s[8] == "Indirect" and s[9] == True]


# --- 1. Supplier Table ---
supplier_header = [
    "id", "name", "contact_email", "phone", "address", "gstin", "pan", "score", "type",
    "is_active", "share_of_business", "lead_time_days", "base_currency", "unit_of_measure"
]
supplier_csv = generate_csv_string(supplier_header, suppliers_data)
print("#### `supplier.csv`\n```csv\n" + supplier_csv + "```\n")


# --- 2. Category Table ---
category_header = ["id", "name", "parent"]
category_csv = generate_csv_string(category_header, categories_data)
print("#### `category.csv`\n```csv\n" + category_csv + "```\n")


# --- 3. PurchaseOrder Table ---
po_data = []
po_id = 1
for current_year in range(START_DATE.year, END_DATE.year + 1):
    year_start = date(current_year, 1, 1)
    year_end = date(current_year, 12, 31)
    # Adjust start/end dates for the first/last partial years
    if current_year == START_DATE.year:
        year_start = START_DATE
    if current_year == END_DATE.year:
        year_end = END_DATE

    for _ in range(NUM_POS_PER_YEAR):
        issue_d = random_date(year_start, year_end)
        
        # Select supplier, prioritizing direct for POs
        supplier_id_for_po = random.choice(direct_supplier_ids + random.choices(indirect_supplier_ids, k=2)) # Mix in some indirect for services/equipment POs
        
        # Find relevant categories for the selected supplier type
        supplier_type = next((s[8] for s in suppliers_data if s[0] == supplier_id_for_po), None)
        valid_categories_for_po = [
            c[0] for c in categories_data
            if c[2] is not None and supplier_type in category_supplier_type_map.get(c[0], [])
        ]
        category_id = random.choice(valid_categories_for_po) if valid_categories_for_po else random.choice([c[0] for c in categories_data if c[2] is not None])

        amount = round(random.uniform(5000.00, 750000.00), 2) # Wider range for manufacturing POs
        status_options = ["Issued"] * 3 + ["Delivered"] * 5 + ["Cancelled"] * 1 # More likely to be delivered
        status = random.choice(status_options)
        
        # For older POs, status is more likely to be Delivered or Cancelled
        if issue_d < END_DATE - timedelta(days=90 * 2): # If PO is old
            status = random.choices(["Delivered", "Cancelled"], weights=[0.9, 0.1], k=1)[0]
        
        # If PO date is in the future relative to current generation date, mark as Issued
        if issue_d > END_DATE:
            status = "Issued"

        po_data.append([
            po_id, f"PO-{issue_d.year}-{po_id:05d}", supplier_id_for_po, category_id, amount, issue_d, status
        ])
        po_id += 1

po_header = ["id", "po_number", "supplier", "category", "amount", "issue_date", "status"]
po_csv = generate_csv_string(po_header, po_data)
print("#### `purchaseorder.csv`\n```csv\n" + po_csv + "```\n")


# --- 4. Invoice Table ---
invoice_data = []
invoice_id = 1
for po in po_data:
    po_status = po[6]
    po_issue_date = po[5]
    po_amount = po[4]
    po_supplier_id = po[2]

    # Don't generate invoices for POs too far in the future
    if po_issue_date > END_DATE + timedelta(days=30):
        continue

    # Only generate invoices for Issued or Delivered POs
    if po_status in ["Issued", "Delivered"]:
        invoice_date = po_issue_date + timedelta(days=random.randint(5, 45))
        # Ensure invoice date isn't in the far future
        if invoice_date > END_DATE + timedelta(days=30):
            invoice_date = random_date(po_issue_date, END_DATE) # Cap at current data end
            if invoice_date < po_issue_date: # Ensure invoice date is after PO
                 invoice_date = po_issue_date + timedelta(days=1)


        due_date = invoice_date + timedelta(days=random.choice([30, 45, 60]))
        paid_date = '' # Placeholder for NULL
        invoice_status = "Pending"

        # Simulate payment based on age and PO status
        if po_status == "Delivered":
            if random.random() < 0.90: # 90% chance of being paid if delivered
                payment_days = random.randint(1, (due_date - invoice_date).days + 15) # Allow some overdue
                temp_paid_date = invoice_date + timedelta(days=payment_days)

                if temp_paid_date <= END_DATE: # Only record paid date if it's within the data range
                    paid_date = temp_paid_date
                    if temp_paid_date > due_date:
                        invoice_status = "Overdue"
                    else:
                        invoice_status = "Paid"
                else:
                    # If it would be paid in the future, it's still pending/overdue
                    if END_DATE > due_date:
                        invoice_status = "Overdue"
                    else:
                        invoice_status = "Pending"
            else:
                 # Even if delivered, a small chance of remaining pending/overdue
                 if END_DATE > due_date:
                    invoice_status = "Overdue"
                 else:
                    invoice_status = "Pending"
        else: # If PO is just 'Issued' and not yet delivered
             if END_DATE > due_date:
                invoice_status = "Overdue"
             else:
                invoice_status = "Pending"

        invoice_data.append([
            invoice_id,
            f"INV-{invoice_date.year}-{invoice_id:06d}",
            po_supplier_id,
            po[0], # purchase_order ID
            invoice_date,
            due_date,
            paid_date if paid_date else '', # Empty string for NULL
            po_amount, # Amount usually matches PO
            invoice_status
        ])
        invoice_id += 1

invoice_header = [
    "id", "invoice_number", "supplier", "purchase_order", "invoice_date",
    "due_date", "paid_date", "amount", "status"
]
invoice_csv = generate_csv_string(invoice_header, invoice_data)
print("#### `invoice.csv`\n```csv\n" + invoice_csv + "```\n")


# --- 5. SpendEntry Table ---
spend_data = []
spend_id = 1
for current_year in range(START_DATE.year, END_DATE.year + 1):
    year_start = date(current_year, 1, 1)
    year_end = date(current_year, 12, 31)
    if current_year == START_DATE.year:
        year_start = START_DATE
    if current_year == END_DATE.year:
        year_end = END_DATE

    for _ in range(NUM_SPEND_ENTRIES_PER_YEAR):
        spend_date = random_date(year_start, year_end)
        
        # Select supplier, prioritizing indirect for general spend entries
        supplier_id_for_spend = random.choice(indirect_supplier_ids * 3 + direct_supplier_ids * 1) # More indirect
        
        # Find relevant categories for the selected supplier type
        supplier_type = next((s[8] for s in suppliers_data if s[0] == supplier_id_for_spend), None)
        valid_categories_for_spend = [
            c[0] for c in categories_data
            if c[2] is not None and supplier_type in category_supplier_type_map.get(c[0], [])
        ]
        category_id = random.choice(valid_categories_for_spend) if valid_categories_for_spend else random.choice([c[0] for c in categories_data if c[2] is not None])
        
        amount = round(random.uniform(100.00, 75000.00), 2) # Wider range for spend
        cost_center = random.choice([f"PROD{random.randint(1,3):03d}", f"RND{random.randint(1,1):03d}", f"ADM{random.randint(1,2):03d}", f"IT{random.randint(1,2):03d}", f"LOG{random.randint(1,1):03d}", f"SALES{random.randint(1,1):03d}"])
        
        # Make description more specific based on category
        desc_lookup = {
            15: "CNC machining charges", 16: "Freight and logistics costs", 17: "Software license fees",
            18: "Factory maintenance services", 19: "Monthly electricity bill", 20: "Product quality testing",
            # General descriptions for parent categories if a specific child isn't picked
            3: "General services expenditure", 4: "Minor equipment purchase",
            # Catch-all
            None: "Miscellaneous operational expense"
        }
        description = desc_lookup.get(category_id, f"Purchase of {categories_data[category_id-1][1].lower()} item/service.")

        spend_data.append([
            spend_id, category_id, supplier_id_for_spend, spend_date, amount, cost_center, description
        ])
        spend_id += 1

spend_header = ["id", "category", "supplier", "date", "amount", "cost_center", "description"]
spend_csv = generate_csv_string(spend_header, spend_data)
print("#### `spendentry.csv`\n```csv\n" + spend_csv + "```\n")


# --- 6. SupplierProductPricing Table ---
product_pricing_data = []
product_pricing_id = 1
for _ in range(NUM_PRODUCTS_PRICED):
    supplier_id_for_pricing = random.choice(direct_supplier_ids) # Only direct suppliers for product pricing
    product_name_choice = random.choice(product_names_list)
    price = round(random.uniform(10.00, 25000.00), 2) # Wider price range
    currency = next((s[13] for s in suppliers_data if s[0] == supplier_id_for_pricing), "INR") # Use supplier's base currency
    
    # Logic to infer a more appropriate UOM from product name
    unit_of_measure = "PCS" # Default
    if "steel" in product_name_choice.lower() or "iron" in product_name_choice.lower() or "granules" in product_name_choice.lower() or "material mix" in product_name_choice.lower():
        unit_of_measure = "KG"
    elif "fluid" in product_name_choice.lower() or "lubricant" in product_name_choice.lower() or "chemical" in product_name_choice.lower():
        unit_of_measure = "LITRE"
    elif "assembly" in product_name_choice.lower() or "kit" in product_name_choice.lower() or "sensor" in product_name_choice.lower() or "unit" in product_name_choice.lower() or "housing" in product_name_choice.lower():
        unit_of_measure = "PCS"
    elif "hose" in product_name_choice.lower() or "tubing" in product_name_choice.lower():
        unit_of_measure = "METER"
    elif "service" in product_name_choice.lower():
        unit_of_measure = "SERVICE"
    elif "plates" in product_name_choice.lower() or "casting" in product_name_choice.lower():
        unit_of_measure = "PCS" # Could be KG, but PCS is also common for finished parts

    product_pricing_data.append([
        product_pricing_id, supplier_id_for_pricing, product_name_choice, price, currency, unit_of_measure
    ])
    product_pricing_id += 1

product_pricing_header = ["id", "supplier", "product_name", "price", "currency", "unit_of_measure"]
product_pricing_csv = generate_csv_string(product_pricing_header, product_pricing_data)
print("#### `supplierproductpricing.csv`\n```csv\n" + product_pricing_csv + "```\n")


# --- 7. SupplierContract Table ---
contract_data = []
contract_id = 1
for _ in range(NUM_CONTRACTS):
    supplier_id_for_contract = random.choice(active_supplier_ids)
    start_d = random_date(START_DATE, END_DATE - timedelta(days=90)) # Contracts usually start before end date
    end_d = start_d + timedelta(days=random.choice([365, 730, 1095, 1460])) # 1, 2, 3, or 4 year contracts
    
    # Ensure contract end date doesn't extend too far beyond END_DATE for relevance
    if end_d > END_DATE + timedelta(days=365):
        end_d = END_DATE + timedelta(days=random.randint(0, 365)) # Cap contracts to finish within a year of END_DATE

    contract_name = random.choice([
        "Annual Supply Agreement for Raw Materials", "Framework Agreement for IT Services", "Master Purchase Agreement (Components)",
        "Volume Discount Contract for Elastomers", "Maintenance & Support Contract (Machinery)", "Component Sourcing Contract (Tier 1)",
        "Logistics Services Master Agreement", "Chemical Supply & Disposal Agreement"
    ])
    terms = f"Standard terms, Payment terms {random.choice(['Net 30', 'Net 45', 'Net 60'])}, annual review clause, auto-renewal option."
    contract_data.append([
        contract_id, supplier_id_for_contract, contract_name, start_d, end_d, terms
    ])
    contract_id += 1

contract_header = ["id", "supplier", "contract_name", "start_date", "end_date", "terms"]
contract_csv = generate_csv_string(contract_header, contract_data)
print("#### `suppliercontract.csv`\n```csv\n" + contract_csv + "```\n")


# --- 8. SupplierDiscount Table ---
discount_data = []
discount_id = 1
# Get a list of (supplier_id, product_name) from existing pricing to link discounts
available_priced_products = [(p[1], p[2]) for p in product_pricing_data]

for _ in range(NUM_DISCOUNTS):
    if not available_priced_products: continue # Skip if no products exist to discount

    supplier_id_for_discount, product_name_for_discount = random.choice(available_priced_products)
    discount_percent = round(random.uniform(1.00, 15.00), 2) # Wider discount range
    valid_from = random_date(START_DATE, END_DATE - timedelta(days=90))
    valid_to = valid_from + timedelta(days=random.choice([90, 180, 270, 365]))

    # Ensure discount valid_to doesn't extend too far beyond END_DATE
    if valid_to > END_DATE + timedelta(days=60):
        valid_to = END_DATE + timedelta(days=random.randint(0, 60))

    discount_data.append([
        discount_id, supplier_id_for_discount, product_name_for_discount, discount_percent, valid_from, valid_to
    ])
    discount_id += 1

discount_header = ["id", "supplier", "product_name", "discount_percent", "valid_from", "valid_to"]
discount_csv = generate_csv_string(discount_header, discount_data)
print("#### `supplierdiscount.csv`\n```csv\n" + discount_csv + "```\n")


# --- 9. AlternateSupplier Table ---
alternate_supplier_data = []
alternate_supplier_id = 1
# Products that might have alternate suppliers (a subset of all products)
products_for_alternates = random.sample(product_names_list, min(len(product_names_list), NUM_ALTERNATE_SUPPLIERS_ENTRIES * 3))

for product in products_for_alternates:
    primary_s_id = random.choice(direct_supplier_ids)
    
    # Try to find an alternate that is not the primary and is also direct
    alt_s_candidates = [s for s in direct_supplier_ids if s != primary_s_id]
    if not alt_s_candidates: continue # Skip if no distinct alternate available

    alternate_s_id = random.choice(alt_s_candidates)
    lead_time = random.randint(7, 90) # Wider lead time range for alternate

    alternate_supplier_data.append([
        alternate_supplier_id, product, primary_s_id, alternate_s_id, lead_time
    ])
    alternate_supplier_id += 1
    if alternate_supplier_id > NUM_ALTERNATE_SUPPLIERS_ENTRIES: # Cap the number of entries
        break

alternate_supplier_header = ["id", "product_name", "primary_supplier", "alternate_supplier", "lead_time_days"]
alternate_supplier_csv = generate_csv_string(alternate_supplier_header, alternate_supplier_data)
print("#### `alternatesupplier.csv`\n```csv\n" + alternate_supplier_csv + "```\n")