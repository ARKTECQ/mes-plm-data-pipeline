#!/usr/bin/env python
# coding: utf-8

# In[92]:


import pandas as pd
import random
from faker import Faker
from pathlib import Path

fake = Faker()

Faker.seed(42)
random.seed(42)

# Paramaterized code

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BASE_PATH = PROJECT_ROOT / "data" / "raw"

PLM_PATH = BASE_PATH / "plm"
MES_PATH = BASE_PATH / "mes"

PLM_PATH.mkdir(parents=True, exist_ok=True)
MES_PATH.mkdir(parents=True, exist_ok=True)

NUM_PRODUCTS = 100
NUM_BOM = 700
NUM_ECN = 150
NUM_MACHINE_LOGS = 3000
NUM_ORDERS = 500
NUM_DOWNTIME = 300


# In[63]:


# Generate Product IDs

product_ids = []

for i in range(1, NUM_PRODUCTS + 1):
    product_ids.append(f"PROD-{i:03}")


# In[64]:


product_names = [
    "Widget Alpha",
    "Widget Beta",
    "Widget Gamma",
    "Widget Delta",
    "Gear Assembly",
    "Drive Shaft",
    "Bearing Housing",
    "Brake Disc",
    "Clutch Plate",
    "Engine Block",
    "Cylinder Head",
    "Axle Shaft",
    "Pulley Wheel",
    "Rotor Assembly",
    "Stator Unit",
    "Control Panel",
    "Hydraulic Pump",
    "Valve Body",
    "Roller Bearing",
    "Flexible Coupling",
    "Flywheel",
    "Crankshaft",
    "Piston Kit",
    "Camshaft",
    "Oil Pump",
    "Fuel Injector",
    "Timing Belt",
    "Cooling Fan",
    "Radiator",
    "Air Filter",
    "Exhaust Manifold",
    "Turbocharger",
    "Starter Motor",
    "Alternator",
    "Wheel Hub",
    "Steering Knuckle",
    "Suspension Arm",
    "Brake Caliper",
    "Shock Absorber",
    "Transmission Case",
    "Differential Gear",
    "Planetary Gear",
    "Universal Joint",
    "Seal Ring",
    "O-Ring",
    "Mounting Flange",
    "Fastener Kit",
    "Hex Bolt",
    "Lock Nut",
    "Flat Washer",
    "Chain Sprocket",
    "Roller Chain",
    "Linear Guide",
    "Servo Motor",
    "Stepper Motor",
    "PLC Module",
    "Sensor Module",
    "Pressure Sensor",
    "Temperature Sensor",
    "Flow Meter",
    "Solenoid Valve",
    "Electric Actuator",
    "Control Valve",
    "Hydraulic Cylinder",
    "Pneumatic Cylinder",
    "Air Compressor",
    "Vacuum Pump",
    "Heat Exchanger",
    "Boiler Tube",
    "Conveyor Roller",
    "Conveyor Belt",
    "Mixer Blade",
    "Impeller",
    "Filter Housing",
    "Spray Nozzle",
    "Manifold Block",
    "Electrical Connector",
    "Terminal Block",
    "Fuse Box",
    "Power Supply Unit",
    "Transformer Core",
    "Cooling Jacket",
    "Fan Blade",
    "Motor Shaft",
    "Housing Cover",
    "Gear Wheel",
    "Rack Gear",
    "Pinion Gear",
    "Support Bracket",
    "Mounting Plate",
    "Pipe Clamp",
    "Door Frame",
    "Chassis Frame",
    "Base Plate",
    "Machine Guard",
    "Inspection Cover",
    "Lubrication Unit",
    "Tool Holder",
    "Cutting Head",
    "Spindle Assembly"
]


# In[65]:


product_data = []

for i in range(NUM_PRODUCTS):

    file_name = product_names[i].lower().replace(" ", "_")
    cad_file = f"{file_name}_v1.step"

    row = {
        "product_id": product_ids[i],
        "product_name": product_names[i],
        "design_release_date": fake.date_between(
            start_date="-3y",
            end_date="today"
        ),
        "CAD_file_ref": cad_file
    }

    product_data.append(row)

product_df = pd.DataFrame(product_data)


# In[66]:


product_df.head()


# In[ ]:


product_df.to_csv(
    PLM_PATH / "product_metadata.csv",
    index=False #index is row numbers
)

print("product_metadata.csv created successfully")
print(product_df.shape)


# In[68]:


print("Current Working Directory:")
print(Path.cwd())

print("\nPLM Path:")
print(PLM_PATH.resolve())


# In[69]:


print(NUM_PRODUCTS)
print(len(product_names))
print(len(product_ids))


# In[70]:


#BOM.CSV
product_df = pd.read_csv(PLM_PATH / "product_metadata.csv")
product_df.head()


# In[71]:


components = [
    "COMP-001",
    "COMP-002",
    "COMP-003",
    "COMP-004",
    "COMP-005",
    "COMP-006",
    "COMP-007",
    "COMP-008",
    "COMP-009",
    "COMP-010",
    "COMP-011",
    "COMP-012",
    "COMP-013",
    "COMP-014",
    "COMP-015",
    "COMP-016",
    "COMP-017",
    "COMP-018",
    "COMP-019",
    "COMP-020",
    "COMP-021",
    "COMP-022",
    "COMP-023",
    "COMP-024",
    "COMP-025",
    "COMP-026",
    "COMP-027",
    "COMP-028",
    "COMP-029",
    "COMP-030"
]

versions = [
    "v1.0",
    "v1.1",
    "v2.0",
    "v2.1",
    "v3.0"
]


# In[72]:


bom_data = []

versions = [
    "v1.0",
    "v1.1",
    "v2.0",
    "v2.1",
    "v3.0"
]

for product_id in product_df["product_id"]:

    # Each product will have 5 to 8 unique components
    selected_components = random.sample(components, random.randint(5, 8))

    for component in selected_components:

        row = {
            "product_id": product_id,
            "component_id": component,
            "quantity": random.randint(1, 10),
            "component_version": random.choice(versions)
        }

        bom_data.append(row)

bom_df = pd.DataFrame(bom_data)


# In[73]:


bom_df.to_csv(
    PLM_PATH / "bom.csv",
    index=False
)

print("bom.csv created successfully")
print("Rows :", len(bom_df))


# In[74]:


bom_df.to_csv(
    PLM_PATH / "bom.csv",
    index=False
)

print("bom.csv created successfully")
print(bom_df.shape)


# In[75]:


print(bom_df.shape)
print()

print(bom_df.head())
print()

print(bom_df["product_id"].nunique())


# In[76]:


#ENCR.CSV
product_df = pd.read_csv(PLM_PATH / "product_metadata.csv")
product_df.head()


# In[77]:


change_types = [
    "Design Update",
    "Material Change",
    "Dimension Change",
    "Supplier Change",
    "Quality Improvement",
    "Cost Reduction",
    "Performance Enhancement",
    "Compliance Update"
]


# In[78]:


ecn_data = []

for i in range(NUM_ECN):

    row = {
        "change_id": f"ECN-{i+1:03d}",
        "product_id": random.choice(product_df["product_id"]),
        "change_type": random.choice(change_types),
        "request_date": fake.date_between(
            start_date="-2y",
            end_date="today"
        ),
       "approved_flag": random.choices(
    ["True", "False"],
    weights=[80, 20],
    k=1
)[0]
    }

    ecn_data.append(row)

ecn_df = pd.DataFrame(ecn_data)


# In[79]:


ecn_df.head()


# In[80]:


ecn_df.to_csv(
    PLM_PATH / "ecn_requests.csv",
    index=False
)

print("ecn_requests.csv created successfully")
print(ecn_df.shape)


# In[81]:


print(ecn_df.shape)
print()

print(ecn_df.head())
print()

print(ecn_df.isnull().sum())


# In[93]:


#Machine_logs.csv
machine_ids = [
    "M01",
    "M02",
    "M03",
    "M04",
    "M05",
    "M06",
    "M07",
    "M08",
    "M09",
    "M10"
]

status_list = [
    "Running",
    "Idle",
    "Maintenance"
]


# In[94]:


machine_logs = []

for i in range(NUM_MACHINE_LOGS):

    row = {
        "timestamp": fake.date_time_between(
            start_date="-1y",
            end_date="now"
        ),
        "machine_id": random.choice(machine_ids),
        "status": random.choices(
            ["Running", "Idle", "Maintenance"],
            weights=[80, 15, 5],
            k=1
        )[0],
        "cycle_time_ms": random.randint(800, 2500),
        "output_count": random.randint(1, 15),
        "defect_flag": random.choices(
            ["True", "False"],
            weights=[5, 95],
            k=1
        )[0]
    }

    machine_logs.append(row)

machine_logs_df = pd.DataFrame(machine_logs)


# In[84]:


machine_logs_df.head()


# In[96]:


machine_logs_df.to_csv(
    MES_PATH / "machine_logs.csv",
    index=False
)

print("machine_logs.csv created successfully")
print(machine_logs_df.shape)


# In[97]:


print(machine_logs_df.shape)
print()

print(machine_logs_df.head())
print()

print(machine_logs_df.isnull().sum())


# In[98]:


#product_orders.csv
product_df = pd.read_csv(PLM_PATH / "product_metadata.csv")
product_df.head()
print("Products in product_df:", len(product_df))
print("Unique product IDs:", product_df["product_id"].nunique())
print("First products:", product_df["product_id"].head(10).tolist())


# In[99]:



production_orders = []

# First, create at least one order for every product
for i, product_id in enumerate(product_df["product_id"], start=1):

    start_time = fake.date_time_between(
        start_date="-1y",
        end_date="now"
    )

    duration = random.randint(1, 8)
    end_time = start_time + pd.Timedelta(hours=duration)

    planned_qty = random.randint(100, 500)
    actual_qty = planned_qty - random.randint(0, 20)

    row = {
        "order_id": f"ORD-{i:04d}",
        "product_id": product_id,
        "start_time": start_time,
        "end_time": end_time,
        "planned_qty": planned_qty,
        "actual_qty": actual_qty
    }

    production_orders.append(row)


# Generate the remaining orders randomly
for i in range(NUM_PRODUCTS + 1, NUM_ORDERS + 1):

    start_time = fake.date_time_between(
        start_date="-1y",
        end_date="now"
    )

    duration = random.randint(1, 8)
    end_time = start_time + pd.Timedelta(hours=duration)

    planned_qty = random.randint(100, 500)
    actual_qty = planned_qty - random.randint(0, 20)

    row = {
        "order_id": f"ORD-{i:04d}",
        "product_id": random.choice(product_df["product_id"]),
        "start_time": start_time,
        "end_time": end_time,
        "planned_qty": planned_qty,
        "actual_qty": actual_qty
    }

    production_orders.append(row)

production_orders_df = pd.DataFrame(production_orders)



# In[89]:


production_orders_df.head()


# In[100]:


production_orders_df.to_csv(
    MES_PATH / "production_orders.csv",
    index=False
)

print("production_orders.csv created successfully")
print(production_orders_df.shape)
print("Total orders:", len(production_orders_df))
print("Unique products:", production_orders_df["product_id"].nunique())

missing_products = set(product_df["product_id"]) - set(
    production_orders_df["product_id"]
)

print("Products without orders:", missing_products)


# In[101]:


print(production_orders_df.shape)
print()

print(production_orders_df.head())
print()

print(production_orders_df.isnull().sum())


# In[102]:


#downtime.csv
reason_codes = [
    "Scheduled Maintenance",
    "Machine Failure",
    "Power Outage",
    "Tool Replacement",
    "Material Shortage",
    "Quality Inspection",
    "Operator Break",
    "Sensor Fault"
]


# In[103]:


downtime_events = []

for i in range(NUM_DOWNTIME):

    start_time = fake.date_time_between(
        start_date="-1y",
        end_date="now"
    )

    duration = random.randint(30, 240)

    end_time = start_time + pd.Timedelta(minutes=duration)

    row = {
        "event_id": f"DT-{i+1:03d}",
        "machine_id": random.choice(machine_ids),
        "start_time": start_time,
        "end_time": end_time,
        "reason_code": random.choice(reason_codes)
    }

    downtime_events.append(row)

downtime_df = pd.DataFrame(downtime_events)


# In[104]:


downtime_df.head()


# In[105]:


downtime_df.to_csv(
    MES_PATH / "downtime_events.csv",
    index=False
)

print("downtime_events.csv created successfully")
print(downtime_df.shape)


# In[106]:


print(downtime_df.shape)
print()

print(downtime_df.head())
print()

print(downtime_df.isnull().sum())


# In[ ]:




