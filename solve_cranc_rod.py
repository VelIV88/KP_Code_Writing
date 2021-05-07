import numpy as np
from scipy.optimize import fsolve

class CrankSlideMech:
    """Класс описывающий поведение плоского кривошипно-ползунного механизма.
    Вводится плоская система координат. 
    Начало координат совмещается с точкой крепления кривошипа к стойке. 
    Вертикальная ось обозначается "у", горизонтальная - "х". 
    Точки механизма: 
        "О" - начало кривршипа, 
        "A" - конец кривошипа, начало шатуна
        "B" - конец шатуна, ползун"""
    
    
    def __init__(self, angleGuid, eccentrGuid, lengthCrank, lengthRod,
                 rotateSpeedCrank, angleCrank):
        self.angleGuid = (angleGuid) * np.pi / 180
        self.eccentrGuid = eccentrGuid
        self.lengthCrank = np.abs(lengthCrank)
        self.lengthRod = np.abs(lengthRod)
        self.rotateSpeedCrank = rotateSpeedCrank
        self.angleCrank = (angleCrank) * np.pi / 180
        
    
    def findCoord_A(self):
        """Метод нахождения координат точки А"""
        x_A = self.lengthCrank * np.cos(self.angleCrank)
        y_A = self.lengthCrank * np.sin(self.angleCrank)
        return x_A, y_A
        
        
    def findCoord_B(self):
        """Метод нахождения координат точки А"""
        z = ([(self.lengthRod) * np.cos(self.angleGuid),
                      (self.lengthRod) * np.sin(self.angleGuid)])
        def geomEqu(z):
            """Система уравнений, описывающих условия совместности перемещения
            кривошипа, шатуна и ползуна"""
            x, y = z
            X, Y = CrankSlideMech.findCoord_A(self)
            f1 = (x * np.tan(self.angleGuid) + 
                  self.eccentrGuid / np.cos(self.angleGuid) - y)
            f2 = ((x - X)**2 + (y - Y)**2 - self.lengthRod**2)
            return (f1, f2)
        
        x_B, y_B = fsolve(geomEqu, z, xtol=0.0001)
        return x_B, y_B
    
    def findVelocity(self):
        """Метод нахождения линейных скоростей точек механизма"""
        velocity_A = self.rotateSpeedCrank * self.lengthCrank
        angleVel_A = self.angleCrank - np.pi / 2
        x_B, y_B = CrankSlideMech.findCoord_B(self)
        x_A, y_A = CrankSlideMech.findCoord_A(self)
        angleVelRod = np.arctan((y_B - y_A) / (x_B - x_A)) - np.pi / 2
        
        def velocityEqu(v):
            """Система уравнений, описывающая кинематику механизма"""
            v_B, v_BA = v
            f1 = (v_B * np.sin(self.angleGuid) - 
                  velocity_A * np.sin(angleVel_A) - 
                  v_BA * np.sin(angleVelRod))
            f2 = (v_B * np.cos(self.angleGuid) - 
                  velocity_A * np.cos(angleVel_A) - 
                  v_BA * np.cos(angleVelRod))
            return (f1, f2)
        
        velocity_B, velocity_BA = fsolve(velocityEqu, (0, 0))
        return velocity_A, angleVel_A, velocity_BA, velocity_B, angleVelRod
    
    def findAcceleration(self):
        """Метод нахождения линейных ускорений точек механизма"""
        accNorm_A = self.rotateSpeedCrank**2 * self.lengthCrank
        accNorm_BA = (self.findVelocity()[2]**2 / self.lengthRod)
        x_B, y_B = CrankSlideMech.findCoord_B(self)
        x_A, y_A = CrankSlideMech.findCoord_A(self)
        angleRod = np.arctan((y_B - y_A) / (x_B - x_A))
        
        def accelerationEqu(a):
            a_B, aTau_BA = a
            f1 = (a_B * np.sin(self.angleGuid) - 
                  accNorm_A * np.sin(self.angleCrank) - 
                  accNorm_BA * np.sin(angleRod) -
                  aTau_BA * np.sin(self.findVelocity()[4]))
            f2 = (a_B * np.cos(self.angleGuid) - 
                  accNorm_A * np.cos(self.angleCrank) - 
                  accNorm_BA * np.cos(angleRod) -
                  aTau_BA * np.cos(self.findVelocity()[4]))
            return (f1, f2)
        
        acc_B, accTau_BA = fsolve(accelerationEqu, (0, 0))
        return accNorm_A, accNorm_BA, accTau_BA, acc_B, angleRod
        
#first_cr_sl_mech = CrankSlideMech(angleGuid=10, eccentrGuid=0.01, 
#                                    lengthCrank=0.1, lengthRod=0.3, 
#                                    rotateSpeedCrank=10, angleCrank=20)
#print(first_cr_sl_mech.findCoord_A())
#print(first_cr_sl_mech.findCoord_B())
#print(first_cr_sl_mech.findVelocity())
#print(first_cr_sl_mech.findAcceleration())