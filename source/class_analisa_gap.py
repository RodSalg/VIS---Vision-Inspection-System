import os
import cv2 as cv
import datetime
import numpy as np
import time
import class_PDI as pdi
import gap_DAO as gDAO
from colorama import Fore, Back, Style, init

class Gap:
     
    def __init__(self, modelo):
        
        pass


    def get_imagem(self, path, x, y):
        
        tam_x1 = 30
        tam_x2 = 30

        image_original = cv.imread(path, cv.IMREAD_GRAYSCALE)[int(float(y))-20: int(float(y))+20, int(float(x))-tam_x1:int(float(x))+tam_x2]


        return image_original


    def get_hora_atual(self):

        current_time = datetime.datetime.now()

        hour = current_time.strftime("%H")
        minute = current_time.strftime("%M")
        second = current_time.strftime("%S")  # Adicione esta linha para obter os segundos

        current_time = "{}h_{}min_{}s".format(hour, minute, second)

        return current_time


    def get_y_inferior(self, imagem, altura_imagem, centro_imagem_x, filename):

        imagem_analise_superior = imagem.copy()

        cont = 0

        y_superior = None

        for i in range(altura_imagem): 

            if imagem[i + altura_imagem, centro_imagem_x] > 230:

                y_superior = i + altura_imagem
                break

            imagem_analise_superior[i + altura_imagem, centro_imagem_x] = 255 

            
            cont = cont + 1

        current_time = self.get_hora_atual()
        # cv.imwrite('images_canny/regiao_inferior/{}_{}_inf.jpg'.format(current_time, filename), imagem_analise_superior)

        return y_superior


    def get_y_superior(self, imagem, altura_imagem, centro_imagem_x, filename):

        imagem_analise_superior = imagem.copy()

        y_inferior = None

        for coluna in range(altura_imagem - 1, 0, -1):

            if imagem[coluna, centro_imagem_x] > 230:

                y_inferior = coluna

                break

            imagem_analise_superior[coluna, centro_imagem_x] = 255


        current_time = self.get_hora_atual()
        # cv.imwrite('images_canny/regiao_superior/{}_{}_sup.jpg'.format(current_time, filename), imagem_analise_superior)
    
        return y_inferior





    def get_distance_gap(self, imagem, filename):


        centro_imagem_x = int(imagem.shape[1] / 2)
        altura_imagem = int(imagem.shape[0]/2)


        y_superior = None
        y_inferior = None

        y_superior = self.get_y_superior(imagem, altura_imagem, centro_imagem_x, filename)

        y_inferior = self.get_y_inferior(imagem, altura_imagem, centro_imagem_x, filename)



        return y_superior, y_inferior


    def get_inteiro_x_y(self, x, y):
        
        x = float(x)
        x = round(x)
        x = int(x)

        y = float(y)
        y = round(y)
        y = int(y)

        return x, y


    def main(self, imagem, x, y):
        



        current_time = self.get_hora_atual()
        
        edge_image = pdi.processamento_de_imagem(imagem, 20, 50)

        limite_superior, limite_inferior = self.get_distance_gap(edge_image, 'gap')

        limit_gap = 30
        
       
        if(res_gap == 'NGAP'):

            return 'NGAP'
        
        else:

            if( (limite_inferior is None) or (limite_superior is None) ):

                return 'OK' #-1 é porque nao conseguiu contar o gap (falta de informação)
        
            if( (limite_inferior is None) and (limite_superior is None) ):

                return 'OK'

            if(result_gap is None):

                result_gap = 0

            distance_gap = limite_inferior - limite_superior

            if(distance_gap is None):

                distance_gap = -1 #simboliza que voltou vazio 


            

            


            print(f'limite gap: {limit_gap}')

            print(Fore.RED  + 'y_inf - y_sup = distance gap ou \n ({} - {}) = {} '.format(limite_inferior, limite_superior, distance_gap) + Style.RESET_ALL)

            if(distance_gap > limit_gap):

                result_gap =  'NOK'

            else:

                result_gap = 'OK'
            

            return result_gap

        




            