from data import Computer, CPU, GPU, Motherboard, RAM, Storage, CPU_Cooler, Power_Supply, Case, engine, Base
from sqlalchemy import Column
import pandas as pd
from sqlalchemy.orm import Session

cpu_df = pd.read_csv("csv_data/CPU_DF.csv")
case_df = pd.read_csv("csv_data/Case_DF.csv")
cpu_cooler_df = pd.read_csv("csv_data/CPU_Cooler_DF.csv")
gpu_df = pd.read_csv("csv_data/GPU_DF.csv")
motherboard_df = pd.read_csv("csv_data/Motherboard_DF.csv")
power_supply_df = pd.read_csv("csv_data/Power_Supply_DF.csv")
ram_df = pd.read_csv("csv_data/RAM_DF.csv")
storage_df = pd.read_csv("csv_data/Storage_DF.csv")

case_df.columns = [
    "name",
    "type", 
    "color",
    "l_motherboard_ff",
    "l_ps_ff",
    "price"
    ]
# print(case_df)


cpu_df.columns = [
    "name",
    "core_count", 
    "performance_clock", 
    "performance_boost_clock", 
    "tdp", 
    "integrated_graphics", 
    "smt", 
    "socket", 
    "price"
    ]
# print(cpu_df)
# print(cpu_df.name[1])

cpu_cooler_df.columns = [
    "name",
    "fan_rpm",
    "noise_level",
    "radiator_size",
    "price"
]
# print(cpu_cooler_df)

gpu_df.columns = [
    "name",
    "chipset",
    "memory",
    "core_clock",
    "boost_clock",
    "length",
    "tdp",
    "price"
]
# print(gpu_df)

motherboard_df.columns = [
    "name",
    "socket",
    "form_factor",
    "memory_max",
    "memory_slots",
    "ddr",
    "price"
]
# print(motherboard_df)

power_supply_df.columns = [
    "name",
    "ps_type",
    "efficiency_rating",
    "wattage",
    "modular",
    "price"
]
# print(power_spupply_df)

ram_df.columns = [
    "name",
    "speed",
    "modules",
    "price_per_gb",
    "ddr",
    "price"
]
# print(ram_df)

storage_df.columns = [
    "name",
    "capacity",
    "price_per_gb",
    "type",
    "cache",
    "form_factor",
    "interface",
    "price"
]
# print(storage_df)

def is_number(value):
    try:
        float(value)  # Convert to float first, which can handle NaN values
        return True
    except (ValueError, TypeError):
        return False

CPU.__table__.drop(engine)
GPU.__table__.drop(engine)
Motherboard.__table__.drop(engine)
RAM.__table__.drop(engine)
Storage.__table__.drop(engine)
CPU_Cooler.__table__.drop(engine)
Power_Supply.__table__.drop(engine)
Case.__table__.drop(engine)
Computer.__table__.drop(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    all_cpu = []
    for i in range(len(cpu_df.name)):
        cpu = CPU(
            name=cpu_df.at[i, 'name'],
            core_count=int(cpu_df.at[i, 'core_count']),
            performance_clock=float(cpu_df.at[i, 'performance_clock']),
            performance_boost_clock=float(cpu_df.at[i, 'performance_boost_clock']),
            tdp=int(cpu_df.at[i, 'tdp']),
            integrated_graphics=cpu_df.at[i, 'integrated_graphics'],
            smt=cpu_df.at[i, 'smt'] == 'True',
            socket=cpu_df.at[i, 'socket'],
            price=float(cpu_df.at[i, 'price']),
        )
        all_cpu.append(cpu)
    
    all_gpu = []
    for i in range(len(gpu_df.name)):
        if type(gpu_df.at[i, "core_clock"]) is int:
            boost_clock_v = int(gpu_df.at[i, "core_clock"])
        else:
            boost_clock_v = None
        gpu = GPU(
            name = gpu_df.at[i, "name"],
            chipset = gpu_df.at[i, "chipset"],
            memory = int(gpu_df.at[i, "memory"]),
            core_clock = int(gpu_df.at[i, "core_clock"]),
            boost_clock = boost_clock_v,
            length = int(gpu_df.at[i, "length"]),
            tdp = int(gpu_df.at[i, "tdp"]),
            price = float(gpu_df.at[i, "price"])                
        )
        all_gpu.append(gpu)

    all_motherboard = []
    for i in range(len(motherboard_df.name)):
        motherboard = Motherboard(
            name = motherboard_df.at[i, "name"],
            socket = motherboard_df.at[i, "socket"],
            form_factor = motherboard_df.at[i, "form_factor"],
            memory_max = int(motherboard_df.at[i, "memory_max"]),
            memory_slots = int(motherboard_df.at[i, "memory_slots"]),
            ddr = motherboard_df.at[i, "ddr"],
            price = float(motherboard_df.at[i, "price"])
        )
        all_motherboard.append(motherboard)

    all_ram = []
    for i in range(len(ram_df.name)):
        ram = RAM(
            name = ram_df.at[i, "name"],
            speed = int(ram_df.at[i, "speed"]),
            modules = ram_df.at[i, "modules"],
            price_per_gb = float(ram_df.at[i, "price_per_gb"]),
            ddr = ram_df.at[i, "ddr"],
            price = float(ram_df.at[i, "price"])
        )
        all_ram.append(ram)

    all_storage = []
    for i in range(len(storage_df.name)):
        cache_v = pd.to_numeric(storage_df.at[i, "cache"])
        if pd.isna(cache_v):
            cache_v = None
        else:
            cache_v = int(cache_v)
        storage = Storage(
            name = storage_df.at[i, "name"],
            capacity = storage_df.at[i, "capacity"],
            price_per_gb = float(storage_df.at[i, "price_per_gb"]),
            type = storage_df.at[i, "type"],
            cache = cache_v,
            form_factor = storage_df.at[i, "form_factor"],
            interface = storage_df.at[i, "interface"],
            price = float(storage_df.at[i, "price"]),
        )
        all_storage.append(storage)
    
    all_cpu_cooler = []
    for i in range(len(cpu_cooler_df.name)):
        radiator_size_v = pd.to_numeric(cpu_cooler_df.at[i, "radiator_size"])
        if pd.isna(radiator_size_v):
            radiator_size_v = None
        else:
            radiator_size_v = int(radiator_size_v)
        fan_rpm_v = cpu_cooler_df.at[i, "fan_rpm"]
        if pd.isna(fan_rpm_v) or not isinstance(fan_rpm_v, str):
            fan_rpm_v = None
        noise_level_v = cpu_cooler_df.at[i, "noise_level"]
        if pd.isna(noise_level_v) or not isinstance(noise_level_v, str):
            noise_level_v = None
        cpu_cooler = CPU_Cooler(
            name = cpu_cooler_df.at[i, "name"],
            fan_rpm = fan_rpm_v,
            noise_level = noise_level_v,
            radiator_size = radiator_size_v,
            price = float(cpu_cooler_df.at[i, "price"])
        )
        all_cpu_cooler.append(cpu_cooler)

    all_power_supply = []
    for i in range(len(power_supply_df.name)):
        power_supply = Power_Supply(
            name = power_supply_df.at[i, "name"],
            ps_type = power_supply_df.at[i, "ps_type"],
            efficiency_rating = power_supply_df.at[i, "efficiency_rating"],
            wattage = int(power_supply_df.at[i, "wattage"]),
            modular = power_supply_df.at[i, "modular"],
            price = float(power_supply_df.at[i, "price"])
        )
        all_power_supply.append(power_supply)

    all_case = []
    for i in range(len(case_df.name)):
        case = Case(
            name = case_df.at[i, "name"],
            type = case_df.at[i, "type"],
            color = case_df.at[i, "color"],
            l_motherboard_ff = case_df.at[i, "l_motherboard_ff"],
            l_ps_ff = case_df.at[i, "l_ps_ff"],
            price = float(case_df.at[i, "price"])
        )
        all_case.append(case)

    session.add_all(all_cpu)
    session.add_all(all_gpu)
    session.add_all(all_motherboard)
    session.add_all(all_ram)
    session.add_all(all_storage)
    session.add_all(all_cpu_cooler)
    session.add_all(all_power_supply)
    session.add_all(all_case)

    computer = Computer(
        name = "Name_Here",
        cpu = None,
        gpu = None,
        motherboard = None,
        ram = None,
        storage = None,
        cpu_cooler = None,
        case = None
    )

    session.add(computer)
    session.commit()

Base.metadata.create_all(engine)

computer_name = "Name_Here"
search_cpu = "AMD Ryzen 7 5800X3D"
with Session(engine) as session:
    computer = session.query(Computer).filter_by(name=computer_name).first()
    n_cpu = session.query(CPU).filter_by(id=55).first()
    computer.cpu = n_cpu

    session.add(computer)
    session.commit()