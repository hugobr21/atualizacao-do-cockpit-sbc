import time

class ControlRobot:
    
    def __init__(self):
        self.typerror = 1

    def interruptRobot(self, func):
        while True:
            try:
                option = int(input('\nRobô pausado.\n1 - Reiniciar robô\n2 - Desligar robô\nDigite uma opção válida e pressione ENTER.\n'))
                break
            except KeyboardInterrupt:
                print('Opção inválida. Tente novamente uma opção válida abaixo.')
                ins1_CR.interruptRobot(func)
            except:
                print('Opção inválida. Tente novamente uma opção válida abaixo.')
        if option == 1:
            func()
        elif option == 2:
            print('Desligando Robô...')
            exit()
        elif option!= 1 or option!=2:
            print('Opção inválida. Tente novamente uma opção válida abaixo.')
            ins1_CR.interruptRobot(func)

# def funcao_1():
#     print('executando funcao 1')
#     time.sleep(1)
# def funcao_2():
#     print('executando funcao 2')
#     time.sleep(1)
# def funcao_principal():
#     try:
#         while True:
#             funcao_1()
#             funcao_2()
#     except Exception as e:
#         pass
#     except KeyboardInterrupt:
#         ins1_CR.interruptRobot(funcao_principal)

# ins1_CR = ControlRobot()
# funcao_principal()
