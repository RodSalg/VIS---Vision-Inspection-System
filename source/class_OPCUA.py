from opcua import Client
from opcua import ua
import os

class Opcua:

    '''
    
        Para inicar a classe, basta criar o objeto e como parâmetro passar o IP do CLP
    o qual você deseja acessar.
    
    '''
    def __init__(self, ip_plc):

        server_ip = ip_plc

        self.client = Client("opc.tcp://{}:4840".format(server_ip))


    def get_value(self, node_name:str) -> str:

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

    '''
    
        A função get_value():
            
            - Parâmetros: o nome do nó o qual você deseja puxar as informações como String.
            - Retorno: Não possui.

    '''
    def set_value(self, node) -> None: 
    
        try:

            node = self.client.get_node('ns=3;s="{}"'.format(node))

            node.set_value()

        except Exception as e:

            print('Erro ao escrever valor no nó: {}\n'.format(node))
            print('erro: ', e)

# dados = Opcua("192.168.0.10")

# print(dados.get_value())