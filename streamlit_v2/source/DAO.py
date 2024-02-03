import mysql.connector
from mysql.connector import Error

'''

    Classe para persistência de Dados do VIS - Vision Inspection System;
    
    Autor: Thiago Rodrigo Monteiro Salgado - 
    Engenharia da Computação: UFAM


'''

class DAO:
    
    '''
    
        Inicia o objeto sem parâmetros iniciais. Ele cria o banco.

    '''

    def __init__(self) -> None:

        self.mydb = self.get_banco()

    def get_banco(self):

        try:

            mydb = mysql.connector.connect(
                
                host = 'localhost', 
                database = 'vis', 
                user = 'root', 
                password = '1234')
            
            return mydb
        
        except mysql.connector.Error as e:

            print("Erro ao acessar o banco de dados:", e)
    
    def insert_gap_result(self, result_gap:bool) -> None:

        '''
        
            Insere no banco de dados.

        '''

        try:

            '''
            
                Se for verdade insere o valor 1,
                caso contrário insere 0.

            '''

            if (result_gap == True):

                comando = "INSERT INTO `vis`.`results_prod_gap` (`result`, `class`) VALUES (1, 'correto');"

            elif(result_gap == False):

                comando = "INSERT INTO `vis`.`results_prod_gap` (`result`, `class`) VALUES (0, 'incorreto');"

            else:

                print('Result GAP inválido')

            cursor = self.mydb.cursor()

            cursor.execute(comando)

            self.mydb.commit()


        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)
    
    def free_db(self):
        '''
        
            Fecha o banco de dados.

        '''

        if (self.mydb.is_connected()):

            self.mydb.close()

            print('Banco de dados encerrado.')

        else:

            print('Banco de dados anteriormente fechado.')

