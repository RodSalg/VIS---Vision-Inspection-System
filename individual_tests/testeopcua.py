from opcua import Client
from opcua import ua

import datetime

server_ip = "192.168.0.10" #241

client = Client("opc.tcp://{}:4840".format(server_ip))


try:
    client.connect()
    
    node = client.get_node('ns=3;s="STOP_NODE_RED"')
    
# Obtém os atributos do nó
    print('nivel de acesso: ', node.get_access_level())

    attributes = node.get_attribute(1)

    print('\n', attributes)

    # node.set_value(True)
    # node.set_writable()

    print(node.get_value())

    print('\n\n')
    # node.set_data_value(True)

    # client.set_values([node], ['True'])
    

    # node.set_value(True)


    # print("Writable:", node.get_attribute())

    # node.set_value(1)

    # print(f"Valor lido do nó 'PASS_PC_CAM': {value}")

    # var = ua.DataValue(ua.Varian(True), ua.VariantType.Boolean)
    var = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
    var.ServerTimestamp = None
    var.SourceTimestamp = None

    print(var)

    node.set_value(var)
    # node.get_value()
    print('tudo certo', node.get_value())


finally:

    client.disconnect()

