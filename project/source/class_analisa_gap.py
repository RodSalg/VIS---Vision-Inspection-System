import os
import cv2 as cv
import datetime
import numpy as np
import time
import source.class_PDI as pdi
from colorama import Fore, Back, Style, init

class Gap:
     
    def __init__(self):
        
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
        cv.imwrite('canny_testes/{}_{}_inf.jpg'.format(current_time, filename), imagem_analise_superior)

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
        cv.imwrite('canny_testes/{}_{}_sup.jpg'.format(current_time, filename), imagem_analise_superior)
    
        return y_inferior





    def get_distance_gap(self, imagem, filename):


        centro_imagem_x = int(imagem.shape[1] / 2)
        altura_imagem = int(imagem.shape[0]/2)


        y_superior = None
        y_inferior = None



        y_superior = self.get_y_superior(imagem, altura_imagem, centro_imagem_x, filename)

        y_inferior = self.get_y_inferior(imagem, altura_imagem, centro_imagem_x, filename)

                

        if( (y_superior is None) or (y_inferior is None) ):

            return None #-1 é porque nao conseguiu contar o gap (falta de informação)

        distance_gap = y_inferior - y_superior

        if(distance_gap is None):

            distance_gap = -1 #simboliza que voltou vazio 




        return distance_gap


    def get_inteiro_x_y(self, x, y):
        
        x = float(x)
        x = round(x)
        x = int(x)

        y = float(y)
        y = round(y)
        y = int(y)

        return x, y


    def main(self, imagem):
        



        current_time = self.get_hora_atual()
        
        processamento = pdi.Processamentos()

        # print(imagem.shape)

        centro_y = int(imagem.shape[1] / 2) #x
        centro_x = int(imagem.shape[0] / 2) #y

        # print(centro_x, centro_y)
        
        img = imagem[centro_x - 100:centro_x + 100, centro_y - 340:centro_y + 300] 
        
        # cv.imshow('teste', img)
        # cv.waitKey()
        
        regiao_cortada = processamento.processamento_de_imagem(img, 20, 50)

        cv.imwrite('teste2.bmp', regiao_cortada)

        distance_gap = self.get_distance_gap(regiao_cortada, 'gap')

        print(distance_gap)

        limit_gap = 200
    
        if(distance_gap > limit_gap):

            result_gap =  'NOK'

        else:

            result_gap = 'OK'

        print(result_gap)

    
# testando = Gap()

# testando.main((cv.imread('C:/GITHUB/TCC/teste.bmp', 0)), 10, 10 )
        

#         # return result_gap

        




            