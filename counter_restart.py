import time

class Counter:

    def __init__(self):
        self.counted_times = 0
        self.contagemlimite = 1
        self.delay = 15
        
    def contador_func(self, func):
        self.counted_times +=1
        time.sleep(1)
        maiorque5 = (self.contagemlimite>5)
        # print(self.counted_times,self.contagemlimite)
        if self.counted_times > self.contagemlimite:
            if self.delay<120:
                self.delay += 5
                print('Delay incrementado para: ', self.delay)
            self.counted_times=0
            func()
            
    def zerar_contagem(self):
        maiorque15 = (self.delay > 15)
        contagemaiguala1 = (self.counted_times == 1)
        if maiorque15 and contagemaiguala1:
            self.delay -= 5
        self.counted_times=0