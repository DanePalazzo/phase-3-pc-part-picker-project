from data import *

def create_computer(name):
    if isinstance(name, str):
        with Session(engine) as session:
            n_computer = Computer(name=f"{name}")
            session.add(n_computer)
            session.commit()
            return n_computer
    else:
        raise Exception("Name must be a string")

with Session(engine) as session:
    n_cpu = session.query(CPU).filter_by(id=55).first()

# print(n_cpu)
# create_computer("Test_Computer")

def find_part(part_attr, f_id):
    attr_to_class = {
        'cpu': CPU,
        'gpu': GPU,
        'motherboard': Motherboard,
        'ram': RAM,
        'storage': Storage,
        'cpu_cooler': CPU_Cooler,
        'power_supply': Power_Supply,
        'case': Case
    }
    f_class = attr_to_class[part_attr]
    if f_class is None:
        raise ValueError(f"Unknown part type: {part_attr}")
    
    with Session(engine) as session:
        f_part = session.query(f_class).filter_by(id=f_id).first()
        return f_part
    
# print(find_part('cpu', 55))

def current_computer(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        return c_computer

def add_to_computer(c_id, part_attr, f_id):
    c_part = find_part(part_attr, f_id)
    c_computer = current_computer(c_id)
    c_computer.add_part(c_part)

# add_to_computer(2, 'cpu', 69)
# add_to_computer(10, "motherboard", 99)

def remove_from_computer(c_id, part_attr):
    c_computer = current_computer(c_id)
    c_computer.remove_part(part_attr)

# remove_from_computer(10, "motherboard")

# def valid_cpu_parts(c_id):
#     with Session(engine) as session:
#         c_computer = session.query(Computer).filter_by(id=c_id).first()
#         if not c_computer:
#             raise ValueError(f"No computer found with id {c_id}")
#         if c_computer.motherboard:
#             all_valid_cpus = session.query(CPU).filter_by(socket=c_computer.motherboard.socket).all()
#             return [cpu for cpu in all_valid_cpus]
#         else:
#             all_valid_cpus = session.query(CPU).all()
#             return [cpu for cpu in all_valid_cpus]
        
def valid_cpu(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        if not c_computer:
            raise ValueError(f"No computer found with id {c_id}")
        valid_cpu_list = session.query(CPU)
        if c_computer.motherboard:
            valid_cpu_list = valid_cpu.filter_by(socket=c_computer.motherboard.socket)
        return valid_cpu_list.all()

def valid_motherboard(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        if not c_computer:
            raise ValueError(f"No computer found with id {c_id}")
        valid_motherboards_list = session.query(Motherboard)
        if c_computer.cpu:
            valid_motherboards_list = valid_motherboards_list.filter_by(socket=c_computer.cpu.socket)
        if c_computer.ram:
            valid_motherboards_list = valid_motherboards_list.filter_by(ddr=c_computer.ram.ddr)
        if c_computer.case:
            # # Retrieve the largest supported form factor for the case
            largest_ff = c_computer.case.l_motherboard_ff
            # # Filter motherboards that are equal to or smaller than the case's largest form factor
            # # This requires a hierarchy of form factors to be predefined, which should be known to your system
            form_factor_hierarchy = ['ATX', 'Micro ATX', 'Mini ITX']  # Example hierarchy from largest to smallest
            # # Find all form factors that are compatible (equal or smaller)
            compatible_ffs = form_factor_hierarchy[form_factor_hierarchy.index(largest_ff):]
            valid_motherboards_list = valid_motherboards_list.filter(Motherboard.form_factor.in_(compatible_ffs))
        return valid_motherboards_list.all()
    
def valid_ram(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        if not c_computer:
            raise ValueError(f"No computer found with id {c_id}")
        valid_ram_list = session.query(RAM)
        if c_computer.motherboard:
            valid_ram_list = valid_ram_list.filter_by(ddr=c_computer.motherboard.ddr)
        return valid_ram_list.all()
    
def valid_power_supply(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        if not c_computer:
            raise ValueError(f"No computer found with id {c_id}")
        valid_power_supply_list = session.query(Power_Supply)
        total_tdp = 50
        if c_computer.cpu:
            total_tdp += c_computer.cpu.tdp
        if c_computer.gpu:
            total_tdp += c_computer.gpu.tdp
        valid_power_supply_list = valid_power_supply_list.filter(Power_Supply.wattage > total_tdp * 1.25)
        return valid_power_supply_list.all()
    
def valid_case(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        if not c_computer:
            raise ValueError(f"No computer found with id {c_id}")
        valid_case_list = session.query(Case)
        if c_computer.motherboard:
            if c_computer.motherboard is "Micro ATX":
                supported_form_factors = ["Micro ATX", "Mini ITX"]
                valid_case_list = valid_case_list.filter(Case.motherboard_ff.in_(supported_form_factors))
                # valid_case_list = valid_case_list.filter_by(motherboard_ff="Micro ATX, Mini ITX")
            elif c_computer.motherboard is "ATX":
                valid_case_list = valid_case_list.filter_by(motherboard_ff="ATX, Micro ATX, Mini ITX")

# add_to_computer(6, "cpu", 25)
# print([motherboard.name for motherboard in valid_motherboard_parts(3)])

# create_computer("Computer 5")
add_to_computer(5, "cpu", 93)
# add_to_computer(11, "gpu", 23)
add_to_computer(5, "ram", 217)
add_to_computer(5, "case", 232)
# print([motherboard.name for motherboard in valid_motherboard(11)])
# print([power_supply.name for power_supply in valid_power_supply(3)])

# create_computer("The Chosen Juan")
# add_to_computer(13, "cpu", 10)
# add_to_computer(13, "gpu", 12)

print([motherboard.name for motherboard in valid_motherboard(5)])
# add_to_computer(13, "motherboard", 49)

# print([power_supply.name for power_supply in valid_power_supply(13)])
create_computer("Computer 6")
add_to_computer(6, "cpu", 93)
# add_to_computer(11, "gpu", 23)
add_to_computer(6, "ram", 217)
add_to_computer(6, "case", 232)
print([motherboard.name for motherboard in valid_motherboard(6)])
