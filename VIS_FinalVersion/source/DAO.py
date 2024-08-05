import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
from time import sleep


'''

    Classe para persistência de Dados do VIS - Vision Inspection System;
    
    Autor: Thiago Rodrigo Monteiro Salgado - 
    Engenharia da Computação: UFAM


'''

class VIS_DAO:
    
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
    
    def inser_IA_result(self, filename:str, ia_result:bool) -> None:

        '''
        
            Insere no banco de dados.

        '''

        try:

            '''
            
                Se for verdade insere o valor 1,
                caso contrário insere 0.

            '''

            if (ia_result == True):

                comando = f"INSERT INTO `vis`.`results_prod_gap` (`filename`, `ia_result`) VALUES ({filename}, 'CORRETO');"

            elif(ia_result == False):

                comando = f"INSERT INTO `vis`.`results_prod_gap` (`filename`, `ia_result`) VALUES ({filename}, 'INCORRETO');"

            else:

                print('Resultado Inválido')

            cursor = self.mydb.cursor()

            cursor.execute(comando)

            self.mydb.commit()


        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)

    def get_tempo_atual(self, var_controle:int) -> int:


        '''     0 - POINTER_IMAGE
                1 - FAIL
                2 - PASS
                3 - POINTER_MODEL
        '''

        
        try:

            cursor = self.mydb.cursor()

            comando = f'select TEMPO_VAR from vis.vis_control where id = {var_controle}'

            cursor.execute(comando)

            result = cursor.fetchone()

            return result[0]

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)

    def get_control_element(self, var_controle:int) -> int:


        '''     0 - POINTER_IMAGE
                1 - FAIL
                2 - PASS
                3 - POINTER_MODEL
                5 - model_tampa
                6 - model_gap
        '''

        
        try:

            cursor = self.mydb.cursor()

            comando = f'select state from vis.vis_control where id = {var_controle}'

            cursor.execute(comando)

            result = cursor.fetchone()

            return result[0]

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)



    def get_models(self) -> list:
        
        try:

            cursor = self.mydb.cursor()

            comando = 'SELECT nome_modelo FROM vis.modelos;'
                
            cursor.execute(comando)

            result = cursor.fetchall()

            modelos = []

            for resultado in result:

                modelos.append(resultado[0])

            return modelos

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)


    def get_value_PLC(self, node:str) -> int:
        
        try:

            cursor = self.mydb.cursor()

            comando = f'SELECT STATE FROM vis.vis_opcua_data where OPCUA_NAME = "{node}";'

            cursor.execute(comando)

            result = cursor.fetchone()

            return result[0]

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)


    def get_not_evaluated(self, choice:int, model:str) -> list:
        
        try:

            cursor = self.mydb.cursor()


            if model == 'todos':

                comando = 'select filename from vis.results_prod_gap;'
            
            else:
            
                # if choice == 1 and model != 'todos':

                if choice == 1:
                
                    comando = f'select filename from vis.results_prod_gap where human_evaluation IS NULL and model = "{model}";'
                
                else:
                    comando = f'select filename from vis.results_prod_gap where model = "{model}";'

                # else: 
                    
                #     comando = 'select filename from vis.results_prod_gap;'
                
            cursor.execute(comando)

            result = cursor.fetchall()

            resultado_list = []

            for resultado in result:

                resultado_list.append(resultado[0])

            return resultado_list

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)



            
    def update_tempo_passagem(self, id:int, tempo_atual:float) -> None:

        try:

            cursor = self.mydb.cursor()

            comando = f'UPDATE vis.vis_control SET TEMPO_VAR = {tempo_atual} WHERE ID = {id};'

            cursor.execute(comando)

            self.mydb.commit()

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)



    def delet_model(self, filename_model:str) -> None:

        try:

            cursor = self.mydb.cursor()

            comando = f'DELETE FROM modelos WHERE nome_modelo = "{filename_model}";'

            cursor.execute(comando)

            self.mydb.commit()

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)



    def update_indice_image(self, indice_image:int) -> None:

        try:

            cursor = self.mydb.cursor()

            comando = f'UPDATE vis.vis_control SET STATE = {indice_image} WHERE ID = 1;'

            cursor.execute(comando)

            self.mydb.commit()

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)


    def resultado_tampinha(self, result) -> None:

        try:

            cursor = self.mydb.cursor()

            if result == 1:
                
                comando = f'UPDATE vis.vis_control SET STATE = 1 WHERE ID = 2;'

            elif result == 2:

                comando = f'UPDATE vis.vis_control SET STATE = 1 WHERE ID = 3;'


            cursor.execute(comando)

            self.mydb.commit()

            sleep(1)


            cursor = self.mydb.cursor()

            comando = f'UPDATE vis.vis_control SET STATE = 0 WHERE ID = 3;'

            cursor.execute(comando)

            self.mydb.commit()



            cursor = self.mydb.cursor()

            comando = f'UPDATE vis.vis_control SET STATE = 0 WHERE ID = 2;'

            cursor.execute(comando)

            self.mydb.commit()


        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)
    



    


    def resultado_final_esteira(self, result) -> None:

        try:

            cursor = self.mydb.cursor()

            if result == 1:
                
                comando = f'UPDATE vis.vis_control SET STATE = 1 WHERE ID = 5;'

            elif result == 2:

                comando = f'UPDATE vis.vis_control SET STATE = 1 WHERE ID = 6;'


            cursor.execute(comando)

            self.mydb.commit()

            sleep(1)


            cursor = self.mydb.cursor()

            comando = f'UPDATE vis.vis_control SET STATE = 0 WHERE ID = 8;'

            cursor.execute(comando)

            self.mydb.commit()



            cursor = self.mydb.cursor()

            comando = f'UPDATE vis.vis_control SET STATE = 0 WHERE ID = 7;'

            cursor.execute(comando)

            self.mydb.commit()


        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)









    def update_avaliacao_humana(self, filename:str, opcao:int) -> None:

        try:

            cursor = self.mydb.cursor()

            comando = f'UPDATE vis.results_prod_gap SET human_evaluation = {opcao} WHERE filename = "{filename}";'

            cursor.execute(comando)

            self.mydb.commit()

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)


    def insert_data_db(self, filename:str, result:str, model:str) -> None:

        try:

            cursor = self.mydb.cursor()

            comando = f'INSERT INTO vis.results_prod_gap (filename, ia_result, model) VALUES ("{filename}", "{result}", "{model}");'

            cursor.execute(comando)

            self.mydb.commit()

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)

#INSERT INTO `vis`.`modelos` (`nome_modelo`) VALUES ('adasd');

    def insert_new_model(self, filename_model:str) -> None:

        try:

            cursor = self.mydb.cursor()

            comando = f"INSERT INTO `vis`.`modelos` (`nome_modelo`) VALUES ('{filename_model}');"

            cursor.execute(comando)

            self.mydb.commit()

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)





    def get_all_not_availables(self, choice:int, model:str):

        try:

            cursor = self.mydb.cursor()

            # if model == 'todos':

            #     comando = 'select * from vis.results_prod_gap ORDER BY ID;'
            
            # else:
            
            #     if choice == 1:
                
            #         comando = f'select * from vis.results_prod_gap where human_evaluation IS NULL AND model = "{model}"  ORDER BY ID;'
                
            #     else: 
                    
            #         comando = 'select * from vis.results_prod_gap ORDER BY ID;'







            if model == 'todos':

                comando = 'select * from vis.results_prod_gap ORDER BY ID;'
            
            else:
            
                # if choice == 1 and model != 'todos':

                if choice == 1:
                
                    comando = f'select * from vis.results_prod_gap where human_evaluation IS NULL AND model = "{model}"  ORDER BY ID;'
                
                else:
                    comando = f'select * from vis.results_prod_gap where model = "{model}";'






            cursor.execute(comando)

            result = cursor.fetchall()

            # df = pd.DataFrame(cursor.fetchall(), columns = ['filename', 'start_date'])
            
            # print(result)

            result_dataFrame = pd.read_sql(comando, self.mydb)

            return result_dataFrame

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)
        
    def get_quant_por_hora(self, model:str):

        try:

            cursor = self.mydb.cursor()

            comando = f"""SELECT
    DATE_FORMAT(time_stamp, '%H') as hora,
    SUM(CASE WHEN ia_result = 'INCORRETO' THEN 1 ELSE 0 END) as incorreto,
    SUM(CASE WHEN ia_result = 'CORRETO' THEN 1 ELSE 0 END) as correto
FROM
    results_prod_gap
WHERE
    model = '{model}' AND
    DATE(time_stamp) = '2024-03-15'  -- Filtrando pelo dia de hoje
GROUP BY
    hora;"""

            cursor.execute(comando)

            result = cursor.fetchall()

            # df = pd.DataFrame(cursor.fetchall(), columns = ['filename', 'start_date'])
            
            print(result)

            result_dataFrame = pd.read_sql(comando, self.mydb)

            return result_dataFrame

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)


    def get_reprovacoes_dia(self, model:str):

        try:

            cursor = self.mydb.cursor()

            comando = f"""SELECT
    SUM(CASE WHEN ia_result = 'INCORRETO' THEN 1 ELSE 0 END) as reprovações,
    SUM(CASE WHEN ia_result = 'CORRETO' THEN 1 ELSE 0 END) as aprovações
FROM
    results_prod_gap
WHERE
    model = '{model}' AND
    DATE(time_stamp) = '2024-03-15';"""

            cursor.execute(comando)

            result = cursor.fetchall()
            
            print(result)

            result_dataFrame = pd.read_sql(comando, self.mydb)

            return result_dataFrame

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)



    def get_status_image(self, filename:str) -> list:
        
        try:

            cursor = self.mydb.cursor()

            comando = f'SELECT ia_result, human_evaluation FROM vis.results_prod_gap where filename = "{filename}";'

            cursor.execute(comando)

            result = cursor.fetchall()
            
            vetor = []
            print('meu result: ', result)

            valor_1 = (result[0])[0]

            vetor.append(valor_1)

            if valor_1 == 'CORRETO':

                valor_3 = 0

            elif valor_1 == 'INCORRETO':

                valor_3 = 1
            
            else:

                valor_3 = None
            
            valor_2 = (result[0])[1]
            
            if valor_2 != None:

                valor_2 = int(valor_2)
                

            if (valor_2 is None):
                
                vetor.append('NÃO AVALIADO')
                

            elif (valor_2 == 1):
                
                vetor.append('CORRETO')

            elif (valor_2 == 2):
                
                vetor.append('INCORRETO')

            elif (valor_2 == 3):
                
                vetor.append('NÃO DETECT')

            elif (valor_2 == 4):
                
                vetor.append('SEM APARELHO')



            return vetor[0], vetor[1], valor_3

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




    def get_all_data(self):

        try:
            cursor = self.mydb.cursor()

            comando = 'SELECT * FROM vis.results_prod_gap;'
                
            cursor.execute(comando)

            result = cursor.fetchall()

            # Convertendo os dados em uma lista de dicionários
            return result

        except mysql.connector.Error as e:

            print("Erro ao acessar a tabela: \n", e)

    def process_data(self, model:str):

        try:

            cursor = self.mydb.cursor()

            comando = f'SELECT * FROM vis.results_prod_gap where model = "{model}";'
                
            cursor.execute(comando)

            result = cursor.fetchall()

            VP = VN = FP = FN = 0

            for row in result:

                print(f'ia: {row[2]} e manual: {row[4]}')
            
                # Verificar se a avaliação humana é nula e pular a análise
                # if row[3] is None:  
            
                #     continue

                # Verificar cada registro e atualizar as contagens de acordo com o padrão

                if  row[4] == "1":

                    VP += 1

                    print('VP')

                elif row[4] == "2":

                    VN += 1

                    print('FP')

                elif row[4] == "3":

                    FP += 1
                    print('VN')

                elif row[4] == "4":

                    FN += 1
                    print('FN')

                
                # if row[2] == "CORRETO" and row[4] == "1":

                #     VP += 1

                #     print('VP')

                # elif row[2] == "INCORRETO" and row[4] == "2":

                #     VN += 1

                #     print('VN')

                # elif row[2] == "INCORRETO" and row[4] == "1":

                #     FP += 1
                #     print('FP')

                # elif row[2] == "CORRETO" and row[4] == "2":

                #     FN += 1
                #     print('FN')

                # elif row[4] == '3':

                #     FP += 1
                #     print('FP')

                # elif row[4] == '4':

                #     FN += 1
                #     print('FN')


            return VP, VN, FP, FN

        except mysql.connector.Error as e:
            print("Erro ao acessar a tabela: \n", e)

    def calculate_metrics(self, model:str):

        VP, VN, FP, FN = self.process_data(model)


        if (VP + FP == 0):
            
            precision = 0
        
        else:

            precision = (VP / (VP + FP))

        if (VP + VN + FP + FN == 0):
            
            recall = 0
        
        else:

            recall = ( (VP + VN) / (VP + VN + FP + FN) )


        # Accuracy
            
        if ((VP + VN + FP + FN == 0)):

            accuracy = 0
        
        else:

            accuracy = round( (VP + VN) / (VP + VN + FP + FN) )

        print('TODOS: ', VP, VN, FP, FN)
        # Imprimir os valores
        print('TODOS: ', VP, VN, FP, FN)
        print("Precision: {:.2f}%".format(precision * 100))
        print("Recall: {:.2f}%".format(recall * 100))
        print("Accuracy: {:.2f}%".format(accuracy * 100 ))

        return precision, recall, accuracy




    
teste = VIS_DAO()

teste.calculate_metrics('fim_esteira_gap.pt')

# # # result = teste.process_data()
# teste.calculate_metrics('com_ou_sem_tampa.pt')

# # print(result)