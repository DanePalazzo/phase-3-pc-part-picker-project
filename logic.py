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

def current_computer(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        return c_computer

def add_to_computer(computer_id, part_attr, find_id):
    c_part = find_part(part_attr, find_id)
    c_computer = current_computer(computer_id)
    if validate_part(c_computer, c_part):
        c_computer.add_part(c_part)
    else:
        raise Exception(f"Part Not Compatable: {c_part.name}")

def remove_from_computer(c_id, part_attr):
    c_computer = current_computer(c_id)
    c_computer.remove_part(part_attr)

def validate_part(c_computer, c_part):
    part_validation_map = {
        CPU: (valid_cpu),
        Motherboard: (valid_motherboard),
        RAM: (valid_ram),
        Power_Supply: (valid_power_supply),
        Case: (valid_case),
        GPU: (valid_gpu),
        CPU_Cooler: (valid_cpu_cooler)
    }

    validate_function = part_validation_map.get(type(c_part), None)

    if validate_function is None:
        print(f"{c_part.name.capitalize()} validation not implemented or unknown part type.")
        return False

    valid_parts = validate_function(c_computer.id)
    if c_part.id in [part.id for part in valid_parts]:
        # print(f"{c_part.name.capitalize()} Exists.")
        return True
    else:
        # print(f"{c_part.name.capitalize()} Doesn't Exist.")
        return False
    
def valid_cpu(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        if not c_computer:
            raise ValueError(f"No computer found with id {c_id}")
        valid_cpu_list = session.query(CPU)
        if c_computer.motherboard:
            valid_cpu_list = valid_cpu_list.filter_by(socket=c_computer.motherboard.socket)
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
            largest_ff = c_computer.case.l_motherboard_ff
            form_factor_hierarchy = ['ATX', 'Micro ATX', 'Mini ITX']
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
        if c_computer.cpu:
            c_socket = c_computer.cpu.socket
            if c_socket == "AM5" or c_socket == "AM4":
                m_first = session.query(Motherboard).filter_by(socket=c_socket).first()
                valid_ram_list = valid_ram_list.filter_by(ddr=m_first.ddr)
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
        if c_computer.case:
            valid_power_supply_list = valid_power_supply_list.filter_by(ps_type=c_computer.case.l_ps_ff)
        return valid_power_supply_list.all()
    
def valid_case(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        if not c_computer:
            raise ValueError(f"No computer found with id {c_id}")
        valid_case_list = session.query(Case)
        if c_computer.motherboard:
            m_ff = c_computer.motherboard.form_factor
            form_factor_hierarchy = ['Mini ITX', 'Micro ATX', 'ATX']
            compatible_ffs = form_factor_hierarchy[form_factor_hierarchy.index(m_ff):]
            valid_case_list = valid_case_list.filter(Case.l_motherboard_ff.in_(compatible_ffs))
        if c_computer.power_supply:
            ps_ff = c_computer.power_supply.ps_type
            form_factor_hierarchy = ['SFX', 'ATX']
            compatible_ffs = form_factor_hierarchy[form_factor_hierarchy.index(ps_ff):]
            valid_case_list = valid_case_list.filter(Case.l_motherboard_ff.in_(compatible_ffs))
        return valid_case_list.all()

def valid_gpu(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        valid_gpu_list = session.query(GPU)
        return valid_gpu_list.all()
  
def valid_cpu_cooler(c_id):
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=c_id).first()
        valid_cpu_cooler_list = session.query(CPU_Cooler)
        return valid_cpu_cooler_list.all()

# add_to_computer(2, "motherboard", 340)
# add_to_computer(2, "power_supply", 35)
# print(len(valid_cases(2)))
# print([case.name for case in valid_cases(2)])

# remove_from_computer(3, "case")
# print(len(valid_power_supply(3)))
# add_to_computer(3, "case", 228)
# print(len(valid_power_supply(3)))

# create_computer("5")
add_to_computer(5, "cpu", 100)
# add_to_computer(5, "ram", 256)
# print([motherboard.id for motherboard in valid_motherboard(4)])
# print(len(valid_motherboard(5)))
# remove_from_computer(5, "motherboard")
# add_to_computer(5, "motherboard", 251)
add_to_computer(5, "ram", 1)
