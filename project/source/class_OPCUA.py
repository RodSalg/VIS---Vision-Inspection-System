from opcua import Client
from opcua import ua
import time

class Opcua:

    '''
    
        Para inicar a classe, basta criar o objeto e como parâmetro passar o IP do CLP
    o qual você deseja acessar.

    '''
    def __init__(self, ip_plc:str) -> None:

        self.client = Client("opc.tcp://{}:4840".format(ip_plc))
        self.client.connect()


    def get_value(self, node_name: str) -> str:

        '''
        
            A função get_value():
                
                - Parâmetros: o nome do nó o qual você deseja puxar as informações como String.
                - Retorno: Retorna o valor armazenado dentro desta variável no CLP em string.

        '''
    
        try:

            node = self.client.get_node('ns=3;s="{}"'.format(node_name))

            value = node.get_value()

            return value
            
        except Exception as e:

            print('Erro ao obter valor do nó: {}\n'.format(node_name))
            print('erro: ', e)

    def set_value(self, node_name:str, estado:bool) -> None: 

            
        '''
        
            A função set_value():
                
                - Parâmetros: o nome do nó o qual você deseja puxar as informações como String.
                - Retorno: Não possui.

        '''
    
        try:
            

            node = self.client.get_node('ns=3;s="{}"'.format(node_name))

            var = ua.DataValue(ua.Variant(estado, ua.VariantType.Boolean))

            var.ServerTimestamp = None
            var.SourceTimestamp = None

            node.set_value(var)

            print('')

            time.sleep(0.2)

            '''
            
                Alternando os valores -> se for positivo o comando depois ele volta para o falso e vice-versa.

            '''

            if estado == True:

                var = ua.DataValue(ua.Variant(False, ua.VariantType.Boolean))
                
                var.ServerTimestamp = None
                var.SourceTimestamp = None

                node.set_value(var)

            else:

                var = ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))

                var.ServerTimestamp = None
                var.SourceTimestamp = None

                node.set_value(var)

        except Exception as e:

            print('Erro ao escrever valor no nó: {}\n'.format(node_name))
            print('erro: ', e)

# dados = Opcua("192.168.0.10")

# print(dados.get_value('BT_START'))