from opcua import Client
import pymysql
import threading
import time

def get_banco():
    # Conexão com o banco de dados MySQL
    db = pymysql.connect(

        host="127.0.0.1",
        user="root",
        password="1234",
        database="festo"
        
    )

    cursor = db.cursor()

    return cursor, db


# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------


def get_values_output():

    conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', database='festo')
    cursor = conn.cursor()

    cursor.execute('SELECT opcua_name FROM festo.outputs;')

    filenames = cursor.fetchall()

    cursor.close()
    conn.close()

    return filenames


def update_outputs():

    cursor, db = get_banco()

    server_ip = "192.168.0.10"
    client = Client("opc.tcp://{}:4840".format(server_ip))

    # output_values = ['ESTEIRA NO SENTIDO HORARIO']
    output_values = get_values_output()


    while True:
        
        try:

            client.connect()

            for opcua_name in output_values:
                
                # print(f'No {opcua_name[0]}')

                node = client.get_node('ns=3;s="{}"'.format(opcua_name[0]))
                value = node.get_value()
                print(f'valor do {opcua_name[0]}: {value}')

                cursor.execute("UPDATE outputs SET status_output = %s WHERE opcua_name = %s", (value, opcua_name))
                db.commit()

        except Exception as e:
            print(" ", opcua_name[0] )
            print(f"Erro na atualização dos outputs: {e}")

        finally:

            client.disconnect()


# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------


def get_values_input():

    conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', database='festo')
    cursor = conn.cursor()

    cursor.execute('SELECT opcua_name FROM festo.inputs;')

    filenames = cursor.fetchall()

    cursor.close()
    conn.close()

    return filenames


def update_inputs():

    cursor, db = get_banco()

    server_ip = "192.168.0.10"
    client = Client("opc.tcp://{}:4840".format(server_ip))

    # output_values = ['ESTEIRA NO SENTIDO HORARIO']
    input_values = get_values_input()


    while True:
        
        try:

            client.connect()

            for opcua_name in input_values:
                
                # print(f'No {opcua_name[0]}')

                node = client.get_node('ns=3;s="{}"'.format(opcua_name[0]))
                value = node.get_value()
                print(f'valor do {opcua_name[0]}: {value}')

                cursor.execute("UPDATE outputs SET status_input = %s WHERE opcua_name = %s", (value, opcua_name))
                db.commit()

        except Exception as e:

            print(f"Erro na atualização dos outputs: {e}")

        finally:

            client.disconnect()



def main():

    p_thread_outputs = threading.Thread(target = update_outputs)
    p_thread_inputs = threading.Thread(target = update_outputs)

    p_thread_outputs.start()
    p_thread_inputs.start()

    p_thread_outputs.join()
    p_thread_inputs.join()

        

if __name__ == "__main__":
    
    main()
