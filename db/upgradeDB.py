#!/usr/bin/python
# -*- coding:utf-8 -*-
from sqlalchemy import *
from migrate import *
engine = create_engine('mysql://root:123456@localhost/flask', convert_unicode=True)

meta = MetaData(bind=engine)
    #meta.bind = db.Model
exsi_hypervisors = Table('sales', meta, autoload=True)
print dir(exsi_hypervisors)
productid = ['productid1', 'productid2', 'productid3', 'productid4', 'productid5', 'productid6', 'productid7', 'productid8', 'productid9']
warehouse = ['warehouse1', 'warehouse2', 'warehouse3', 'warehouse4', 'warehouse5', 'warehouse6', 'warehouse7', 'warehouse8', 'warehouse9']
code = ['code1', 'code2', 'code3', 'code4', 'code5', 'code6', 'code7', 'code8', 'code9']
number = ['number1', 'number2', 'number3', 'number4', 'number5', 'number6', 'number7', 'number8', 'number9']

def upgrade():
    for i in range(0,9):
        print productid[i]
        initiator_protocol = Column(productid[i], String(length=120))
        if not hasattr(exsi_hypervisors.c, productid[i]): exsi_hypervisors.create_column(initiator_protocol)
        initiator_protocol = Column(warehouse[i], String(length=120))
        if not hasattr(exsi_hypervisors.c, warehouse[i]): exsi_hypervisors.create_column(initiator_protocol)
        initiator_protocol = Column(code[i], String(length=120))
        if not hasattr(exsi_hypervisors.c, code[i]): exsi_hypervisors.create_column(initiator_protocol)
        initiator_protocol = Column(number[i], Integer)
        if not hasattr(exsi_hypervisors.c, number[i]): exsi_hypervisors.create_column(initiator_protocol)

def downgrade():
    for i in range(0,9):
        initiator_protocol = Column(productid[i], String(length=120))
        if hasattr(exsi_hypervisors.c, productid[i]): exsi_hypervisors.drop_column(initiator_protocol)
        initiator_protocol = Column(warehouse[i], String(length=120))
        if hasattr(exsi_hypervisors.c, warehouse[i]): exsi_hypervisors.drop_column(initiator_protocol)
        initiator_protocol = Column(code[i], String(length=120))
        if hasattr(exsi_hypervisors.c, code[i]): exsi_hypervisors.drop_column(initiator_protocol)
        initiator_protocol = Column(number[i], Integer)
        if hasattr(exsi_hypervisors.c, number[i]): exsi_hypervisors.drop_column(initiator_protocol)

if __name__ == '__main__':
    upgrade()