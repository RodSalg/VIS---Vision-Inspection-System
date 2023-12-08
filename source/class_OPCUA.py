from opcua import Client
from opcua import ua
import os

class Opcua:

    '''
    
        Para inicar a classe, basta criar o objeto e como parâmetro passar o IP do CLP
    o qual você deseja acessar.
    
    '''
    def __init__(self, ip_plc):

        server_ip = "192.168.0.10"

        self.client = Client("opc.tcp://{}:4840".format(server_ip))

    '''
    
        A função get_value():
            
            - Parâmetros: o nome do nó o qual você deseja puxar as informações como String.
            - Retorno: Retorna o valor armazenado dentro desta variável no CLP em string.

    '''

    def get_value(self, node) -> str:
    
        try:
        
            node = self.client.get_node('ns=3;s="{}"'.format(node))

            value = node.get_value()

            return value
            
        except Exception as e:

            print('Erro ao obter valor do nó: {}\n'.format(node))
            print('erro: ', e)

    '''
    
        A função get_value():
            
            - Parâmetros: o nome do nó o qual você deseja puxar as informações como String.
            - Retorno: Não possui.

    '''
    def set_value(self, node) -> None: 
    
        try:

            node = self.client.get_node('ns=3;s="{}"'.format(node))

            value = node.set_value()

        except Exception as e:

            print('Erro ao escrever valor no nó: {}\n'.format(node))
            print('erro: ', e)