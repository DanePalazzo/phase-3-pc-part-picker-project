from sqlalchemy import ForeignKey, Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.orm import Session, declarative_base, relationship, validates

Base = declarative_base()
    
class Computer(Base):
    __tablename__= "computers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpu_id = Column(Integer, ForeignKey("cpus.id"), nullable=True)
    cpu = relationship("CPU", back_populates="computers")
    gpu_id = Column(Integer, ForeignKey("gpus.id"))
    gpu = relationship("GPU", back_populates="computers")
    motherboard_id = Column(Integer, ForeignKey("motherboards.id"))
    motherboard = relationship("Motherboard", back_populates="computers")
    ram_id = Column(Integer, ForeignKey("rams.id"))
    ram = relationship("RAM", back_populates="computers")
    storage_id = Column(Integer, ForeignKey("storages.id"))
    storage = relationship("Storage", back_populates="computers")
    cpu_cooler_id = Column(Integer, ForeignKey("cpu_coolers.id"))
    cpu_cooler = relationship("CPU_Cooler", back_populates="computers")
    power_supply_id = Column(Integer, ForeignKey("power_supplys.id"))
    power_supply = relationship("Power_Supply", back_populates="computers")
    case_id = Column(Integer, ForeignKey("cases.id"))
    case = relationship("Case", back_populates="computers")

    def add_part(self, n_part):
        part_to_attr = {
            CPU: 'cpu',
            GPU: 'gpu',
            Motherboard: 'motherboard',
            RAM: 'ram',
            Storage: 'storage',
            CPU_Cooler: 'cpu_cooler',
            Power_Supply: 'power_supply',
            Case: 'case'
        }
        
        part_type = type(n_part)
        if part_type not in part_to_attr:
            raise ValueError("Not a valid part")
        
        with Session(engine) as session:
            session.add(self)
            # Set the attribute based on the part type
            setattr(self, part_to_attr[part_type], n_part)
            session.commit()

    def remove_part(self, part_attr):
        valid_attr = ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'cpu_cooler', 'power_supply', 'case']
        
        if part_attr not in valid_attr:
            raise ValueError(f"Not a valid part type: {part_attr}")
        with Session(engine) as session:
            session.add(self)
            setattr(self, part_attr, None)
            session.commit()

class CPU(Base):
    __tablename__ = "cpus"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    core_count = Column(String)
    performance_clock = Column(Float)
    performance_boost_clock = Column(Float)
    tdp = Column(Integer)
    integrated_graphics = Column(String)
    smt = Column(Boolean)
    socket = Column(String)
    price = Column(Float)
    computers = relationship("Computer", back_populates="cpu")

    def display_details(self):
        display_details = {
            "id": self.id,
            "name": self.name,
            "core_count": self.core_count,
            "performance_clock": self.performance_clock,
            "performance_boost_clock": self.performance_boost_clock,
            "tdp": self.tdp,
            "integrated_graphics": self.integrated_graphics,
            "smt": self.smt,
            "socket": self.socket,
            "price": self.price
        }
        return display_details

class GPU(Base):
    __tablename__ = "gpus"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    chipset = Column(String)
    memory = Column(Integer)
    core_clock = Column(Integer)
    boost_clock = Column(Integer, nullable=True)
    length = Column(Integer)
    tdp = Column(Integer)
    price = Column(Float)
    computers = relationship("Computer", back_populates="gpu")

    def display_details(self):
        display_details = {
            "id": self.id,
            "name": self.name,
            "chipset": self.chipset,
            "memory": self.memory,
            "core_clock": self.core_clock,
            "boost_clock": self.boost_clock,
            "length": self.length,
            "tdp": self.tdp,
            "price": self.price
        }
        return display_details

class Motherboard(Base):
    __tablename__ = "motherboards"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    socket = Column(String)
    form_factor = Column(String)
    memory_max = Column(Integer)
    memory_slots = Column(Integer)
    ddr = Column(String)
    price = Column(Float)
    computers = relationship("Computer", back_populates="motherboard")

    def display_details(self):
        display_details = {
        "id": self.id,
        "name": self.name,
        "socket": self.socket,
        "form_factor": self.form_factor,
        "memory_max": self.memory_max,
        "memory_slots": self.memory_slots,
        "ddr": self.ddr,
        "price": self.price
        }
        return display_details

class RAM(Base):
    __tablename__ = "rams"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    speed = Column(Integer)
    modules = Column(String)
    price_per_gb = Column(Float)
    ddr = Column(String)
    price = Column(Float)
    computers = relationship("Computer", back_populates="ram")

    def display_details(self):
        display_details = {
        "id": self.id,
        "name": self.name,
        "speed": self.speed,
        "modules": self.modules,
        "price_per_gb": self.price,
        "ddr": self.ddr,
        "price": self.price
        }
        return display_details
    
class Storage(Base):
    __tablename__ = "storages"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    capacity = Column(String)
    price_per_gb = Column(Float)
    type = Column(String)
    cache = Column(Integer)
    form_factor = Column(String)
    interface = Column(String)
    price = Column(Float)
    computers = relationship("Computer", back_populates="storage")

    def display_details(self):
        display_details = {
        "id": self.id,
        "name": self.name,
        "capacity": self.capacity,
        "price_per_gb": self.price_per_gb,
        "type": self.type,
        "cache": self.cache,
        "form_factor": self.form_factor,
        "interface": self.interface,
        "price": self.price,
        }
        return display_details

class CPU_Cooler(Base):
    __tablename__ = "cpu_coolers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fan_rpm = Column(String, nullable=True)
    noise_level = Column(String, nullable=True)
    radiator_size = Column(Integer)
    price = Column(Float)
    computers = relationship("Computer", back_populates="cpu_cooler")

    def display_details(self):
        display_details = {
        "id": self.id,
        "name": self.name,
        "fan_rpm": self.fan_rpm,
        "noise_level": self.noise_level,
        "radiator_size": self.radiator_size,
        "price": self.price
        }
        return display_details

class Power_Supply(Base):
    __tablename__ = "power_supplys"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ps_type = Column(String)
    efficiency_rating = Column(String)
    wattage = Column(Integer)
    modular = Column(String)
    price = Column(Float)
    computers = relationship("Computer", back_populates="power_supply")

    def display_details(self):
        display_details = {
        "id": self.id,
        "name": self.name,
        "ps_type": self.ps_type,
        "efficiency_rating": self.efficiency_rating,
        "wattage": self.wattage,
        "modular": self.modular,
        "price": self.price
        }
        return display_details

class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    color = Column(String)
    l_motherboard_ff = Column(String)
    l_ps_ff = Column(String)
    price = Column(Float)
    computers = relationship("Computer", back_populates="case")

    def display_details(self):
        display_details = {
        "id": self.id,
        "name": self.name,
        "type": self.type,
        "color": self.color,
        "l_motherboard_ff": self.l_motherboard_ff,
        "l_ps_ff": self.l_ps_ff,
        "price": self.price
        }
        return display_details

engine = create_engine('sqlite:///pc_part_picker.db')
Base.metadata.create_all(engine)