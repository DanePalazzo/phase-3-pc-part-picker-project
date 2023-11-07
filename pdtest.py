import pandas as pd
cpu_df = pd.read_csv("csv_data/CPU_DF.csv")
case_df = pd.read_csv("csv_data/Case_DF.csv")
cpu_cooler_df = pd.read_csv("csv_data/CPU_Cooler_DF.csv")
gpu_df = pd.read_csv("csv_data/GPU_DF.csv")
motherboard_df = pd.read_csv("csv_data/Motherboard_DF.csv")
power_supply_df = pd.read_csv("csv_data/Power_Supply_DF.csv")
ram_df = pd.read_csv("csv_data/RAM_DF.csv")
storage_df = pd.read_csv("csv_data/Storage_DF.csv")

# print(gpu_df)

case_df.columns = [
    "name",
    "type", 
    "color", 
    "price",
    ]
# print(case_df)


cpu_df.columns = [
    "name",
    "core_count", 
    "performance_clock", 
    "performance_bost_clock", 
    "tdp", 
    "integrated_graphics", 
    "smt", 
    "socket", 
    "price"
    ]
# print(cpu_df)
# print(cpu_df.at[1, "name"])

cpu_cooler_df.columns = [
    "name",
    "fan_rpm",
    "noise_level",
    "radiator_size",
    "price"
]
print(cpu_cooler_df.at[1, "radiator_size"])

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
# print(gpu_df.at[1, "name"])
# print(gpu_df.name[1])

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