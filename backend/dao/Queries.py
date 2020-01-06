
# Queries belong to Supplier starts
def getAllSuppliersQuery():
    return f"SELECT `supplier_id`,`supplier_name`, `address`, `model`, `material_code`, `material_description`, `stock_volume`, `date_time`, `status` FROM `supplier_master`"

def searchSuppliersQuery(filter):
    return f"select `supplier_id`,`supplier_name`, `address`, `model`, `material_code`, `material_description`, `stock_volume`, `date_time`, `status`  from supplier_master where supplier_name like '%{filter}%' or address like '%{filter}%' or model like '%{filter}%' or material_code like '%{filter}%'"

def selectOneSupplierQuery():
    return f'select * from supplier_master where supplier_id = %s'

def insertSupplierQuery():
    return """insert into supplier_master \
            (supplier_name, address, model, material_code, material_description, stock_volume, date_time,status) \
           values(%s, %s, %s, %s, %s, %s,now(), 'ACTIVE')"""

def updateSupplierQuery():
    return """ update supplier_master 
            set supplier_name=%s, address=%s, model=%s, material_code=%s, material_description=%s,
            stock_volume = %s
            where supplier_id=%s """

# Queries belong to Supplier Ends
# Queries belong to Goods Received starts

def getAllGoodsQuery():
    return f'select gr.id,sm.supplier_id,sm.supplier_name,gr.part_no,gr.description,gr.gin_no,gr.goodsdate,gr.quantity,gr.status from goods_received_master gr,supplier_master sm where sm.supplier_id = gr.supplier_id'

def searchGoodsQuery(filter):
    return f"select gr.id,gr.supplier_id,sm.supplier_name,gr.part_no,gr.description,gr.gin_no,gr.goodsdate,gr.quantity,gr.status from goods_received_master gr , supplier_master sm where gr.supplier_id = sm.supplier_id and sm.supplier_name like '%{filter}%' or gr.part_no like '%{filter}%' or gr.description like '%{filter}%' or gr.gin_no like '%{filter}%' or gr.goodsdate like '%{filter}%' or gr.quantity like '%{filter}%'"

def selectOneGoodsQuery():
    return f'select * from goods_received_master where id = %s'

def insertGoodsQuery():
    return """insert into goods_received_master \
            (supplier_id,part_no,description,gin_no,quantity,goodsdate,status,reason,notification_no) \
           values(%s, %s, %s, %s, %s,now(),'ACTIVE','-','-')"""

def updateGoodsQuery():
    return """ update goods_received_master 
            set part_no=%s, description=%s, gin_no=%s, quantity=%s,
            status = 'ACTIVE', reason='--', notification_no='--'
            where id=%s AND  supplier_id=%s"""


# Queries belong to Goods Received Ends