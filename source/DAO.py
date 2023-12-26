import mysql.connector
from mysql.connector import Error

class DAO_gap:

    def __init__(self, id) -> None:

        self.mydb = self.get_banco()
        self.comando = self.get_comando(id)

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
    
    def insert_gap_result(self, result_gap, distance_gap) -> None:

        try:

            comando = "INSERT INTO `vis`.`results_prod_gap` (`result`, `gap_result`) VALUES (%s, %s);"

            cursor = self.mydb.cursor()

            cursor.execute(comando, (result_gap, distance_gap, ))

            result = cursor.fetchall()

            # print(result)

            result = result[0]

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)
        
        finally:

            if (self.mydb.is_connected()):

                cursor.close()

                self.mydb.close()

                print('Banco de dados encerrado.')
  

            else:

                print('Banco de dados anteriormente fechado.')




    def insert_pattern_result(self, result_gap, distance_gap) -> None:

        try:

            comando = "INSERT INTO `vis`.`results_prod_gap` (`result`, `gap_result`) VALUES (%s, %s);"

            cursor = self.mydb.cursor()

            cursor.execute(comando, (result_gap, distance_gap, ))

            result = cursor.fetchall()

            # print(result)

            result = result[0]

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

