class QuadrEq:
    """Класс для работы с квадратными уравнениями вида y=a*x^2+b*x+c"""    
    
    def __init__(self, a, b, c):
        """Конструктор"""
        self.a=a
        self.b=b
        self.c=c
    
    def PrinEq(self):
        print('Уравнение y=({})*x^2+({})*x+({})'.format(self.a,self.b,self.c))        
        
    def EqRoots(self):
        """Поиск корней уравнения a*x^2+b*x+c=0"""
        D=(self.b**2-4*self.c*self.a)
        if D>0:
            EqRoot1=(-self.b+D**(1/2))/(2*self.a)
            EqRoot2=(-self.b-D**(1/2))/(2*self.a)
            print('Первый корень х1='+str("%.3f"%EqRoot1),'Второй корень x2='
                  +str("%.3f"%EqRoot2))
            return[EqRoot1, EqRoot2]
        elif D==0:
            EqRoot1=(-self.b)/(2*self.a)
            print('Единственный корень х='+str("%.3f"%EqRoot1))
            return[EqRoot1]
        else:
            print('Уравнение не имеет решений')
   
    def Extremum(self):
        """Поиск экстремума уравнения y=a*x^2+b*x+c"""
        y0=self.a*(-self.b/(2*self.a))**2+self.b*(-self.b/(2*self.a))+self.c
        print('Максимум y_max=' if self.a<0 else 
              'Минимум y_min='+str("%.3f"%y0))
      
    def Mono(self):
        """Исследование на возрастание/убывание функции y=a*x^2+b*x+c"""
        x0=-self.b/(2*self.a)
        print('Функция возрастает на участке','(-∞; '
              +str("%.3f"%x0)+')' if self.a<0 else '('+str("%.3f"%x0)+'; ∞)')
        print('Функция убывает на участке','(-∞; '
              +str("%.3f"%x0)+')' if self.a>0 else '('+str("%.3f"%x0)+'; ∞)')


Equ1=QuadrEq(2,4,-6)
Equ2=QuadrEq(1,4,0)
Equ3=QuadrEq(3,8,2)

ARR=[]

Equ1.PrinEq()
X=Equ1.EqRoots()
ARR=ARR+X
Equ1.Extremum()
Equ1.Mono()

print()
Equ2.PrinEq()
X=Equ2.EqRoots()
ARR=ARR+X
Equ2.Extremum()
Equ2.Mono()


print()
Equ3.PrinEq()        
X=Equ3.EqRoots()
ARR=ARR+X
Equ3.Extremum()
Equ3.Mono()


print('\n'+'Максимальный корень x='+str("%.3f"%max(ARR)),
      'Минимальный корень x='+str("%.3f"%min(ARR)))     
print(str(ARR))
    

