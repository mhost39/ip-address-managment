from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship
from database import Base


class VLAN(Base):
    __tablename__ = 'vlan'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    descrition = Column(String(255))

    __table_args__ = (UniqueConstraint('name'),)

    @validates('name')
    def validate_name(self, key, name):
        if len(name) == 0:
            raise ValueError('vlan name must not be empty')
        return name

    def __init__(self, name=None, descrition=None):
        self.name = name
        self.descrition = descrition

    def __repr__(self):
        return 'VLAN %r>' % (self.name)

class Subnets(Base):
    __tablename__ = 'subnet'
    id = Column(Integer, primary_key=True, nullable=False)
    vlan_id = Column(Integer, ForeignKey("vlan.id"))
    ip = Column(Integer, nullable=False)
    mask = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    reserved_ips_count = Column(Integer, default=0, nullable=False)
    descrition = Column(String(255))


    vlan = relationship("VLAN", foreign_keys=[vlan_id])
    __table_args__ = (UniqueConstraint('vlan_id', 'ip', 'mask'),)

    @validates('mask')
    def validate_mask(self, key, mask):
        if (mask < 0) or (mask > 32):
            raise ValueError('Mask must be between 0 and 32')
        return mask

    @validates('name')
    def validate_name(self, key, name):
        if len(name) == 0:
            raise ValueError('vlan name must not be empty')
        return name

    def __init__(self, vlan_id=None, name=None, ip=None, mask=None, descrition=None, reserved_ips_count=None):
        self.vlan_id = vlan_id
        self.name = name
        self.ip = ip
        self.mask = mask
        self.descrition = descrition
        self.reserved_ips_count = reserved_ips_count

    def __repr__(self):
        return '<VLAN %r>' % (self.name)
