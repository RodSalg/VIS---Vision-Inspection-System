import mysql.connector
from mysql.connector import Error

class DAO_gap:

    def __init__(self, id) -> None:

        self.mydb = self.get_banco()
        self.comando = self.get_comando(id)

    def get_banco(self):

        try:

            mydb = mysql.connector.connect(
                
                host='mnsnt066', 
                database='gapserver', 
                user='fit_inventario', 
                password='Flex@2k20')
            
            return mydb
        
        except mysql.connector.Error as e:

            print("Erro ao acessar o banco de dados:", e)


    def get_comando(self, id):
        
        command = "SELECT * FROM tbreceita where ID_receita = {} order by id DESC".format(id)

        return command
    
    def get_limits_and_areas_gap(self):

        try:

            cursor = self.mydb.cursor()

            cursor.execute(self.comando)

            result = cursor.fetchall()

            # print(result)

            result = result[0]

            return result

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)
        
        finally:

            if (self.mydb.is_connected()):

                cursor.close()

                self.mydb.close()

                print('Banco de dados encerrado.')
  

            else:

                print('Banco de dados anteriormente fechado.')

# teste = DAO_gap(1)
# algo = teste.get_limits_and_areas_gap()

# print(algo)

