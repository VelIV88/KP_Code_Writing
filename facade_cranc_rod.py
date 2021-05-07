import sys
import numpy as np
from datetime import datetime as dt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QVBoxLayout
from PyQt5.QtGui import QIcon
from window_cranc_rod import Ui_MainWindow
from solve_cranc_rod import CrankSlideMech
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT


class MyCanvas(FigureCanvasQTAgg):
    """Виджет графика"""
    def __init__(self, fig, parent=None):
        self.fig = fig
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)


class MainWindow(QMainWindow, Ui_MainWindow):
    """Основное окно программы"""
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.widgetAdjust()
        prepareCanvas(parent=self)


    def widgetAdjust(self):
        self.textInAngleGuid.setToolTip('Угол направляющей ползуна в градусах (целое цисло)')
        self.textInAngleCrank.setToolTip('Угол поворота кривошипа в градусах (целое число)')
        self.textInEccentrGuid.setToolTip('Смещение направляющей ползуна в метрах')
        self.textInRotateSpeed.setToolTip('Угловая скорость кривошипа в 1 / с (положительна если движение по часовой стрелке)')
        self.textInLengthCrank.setToolTip('Длина кривошипа в метрах (только положительное число)')
        self.textInLengthRod.setToolTip('Длина шатуна в метрах (только положительное число)')
        
        self.setWindowTitle('Расчет кинематических параметров механизма')
        self.setWindowIcon(QIcon('TMM.ico'))

        self.toolButtonPosition.clicked.connect(self.plotPosition)
        self.toolButtonSpeed.clicked.connect(self.plotSpeed)
        self.toolButtonAcceliration.clicked.connect(self.plotAcceleration)

    
    def readData(self):
        """Получение параметров механизма введенных пользавателем"""
        CSM = CrankSlideMech(angleGuid=float(self.textInAngleGuid.toPlainText()), 
                            eccentrGuid=float(self.textInEccentrGuid.toPlainText()), 
                            lengthCrank=float(self.textInLengthCrank.toPlainText()), 
                            lengthRod=float(self.textInLengthRod.toPlainText()), 
                            rotateSpeedCrank=float(self.textInRotateSpeed.toPlainText()), 
                            angleCrank=int(self.textInAngleCrank.toPlainText()))
        return CSM

    
    def logToFile(self, message):
        """Метод ведущий логи ошибок"""
        logFile = open('logErrors.txt', 'a', encoding='utf8')
        time_format = "%Y-%m-%d %H:%M:%S"
        logMessage = (f'{dt.now():{time_format}}\nВведенные значения параметров механизма:\n'+
                        f'Угол наклона направляющей {self.textInAngleGuid.toPlainText()} \n'+
                        f'Смещение направляющей {self.textInEccentrGuid.toPlainText()} \n'+
                        f'Длина кривошипа {self.textInLengthCrank.toPlainText()} \n'+
                        f'Длина шатуна {self.textInLengthCrank.toPlainText()} \n'+
                        f'Угловая скорость кривошипа {self.textInRotateSpeed.toPlainText()}\n'+
                        f'Угол поворота кривошипа {self.textInAngleCrank.toPlainText()} \n')
        logFile.write(logMessage+message)
        logFile.close()


    def plotPosition(self):
        """Метод обработки нажатия кнопки для построения положения механизма"""
        #Проверки
        try:
            CSM = self.readData()
        except:
            self.labelLog.setText(f'Заполнны не все поля или\n'+
                                f'поля заполнены не числами.\n'+
                                f'Проверьте корректность\n'+
                                f'введенных данных.')
            errMessage = 'Ошибка:\nЗаполнены не все поля или поля заполнены не числами\n\n'
            self.logToFile(errMessage)
            return
        
        distanceToGuid = (abs(CSM.eccentrGuid / np.cos(CSM.angleGuid) / 
                         np.sqrt(1 + np.tan(CSM.angleGuid)**2)))
        minDistanceMech = (CSM.lengthRod - CSM.lengthCrank)
        if  minDistanceMech < distanceToGuid or CSM.lengthCrank == 0 or CSM.lengthRod == 0:
            self.labelLog.setText(f'Механизм с такими параметрами\n'+
                                f'не существует.\n'+
                                f'Проверьте корректность\n'+
                                f'введенных данных.')
            errMessage = 'Ошибка:\nМеханизм с такими параметрами не существует.\n\n'
            self.logToFile(errMessage)
            return

        x_A, y_A = CSM.findCoord_A()
        x_B, y_B = CSM.findCoord_B()

        test_eq1 = (x_B * np.tan(CSM.angleGuid) + CSM.eccentrGuid / np.cos(CSM.angleGuid) - y_B)
        test_eq2 = ((x_A - x_B)**2 + (y_A - y_B)**2 - CSM.lengthRod**2)
        acceptError = CSM.lengthCrank / 1000
        if test_eq1 > acceptError or test_eq2 > acceptError:
            self.labelLog.setText(f'Неизвестная ошибка!\n'+
                                f'отправьте файл logErrors.txt\n'+
                                f'разработчику по адресу\n' +
                                f'iapenkov@omgtu.tech\n')
            errMessage = 'Ошибка:\nОшибка решения уравнений при расчете координат механизма.\n\n'
            self.logToFile(errMessage)
            return

        plt.cla()
        #Отрисовка механизма
        xPointsMech = [0, x_A, x_B]
        yPointsMech = [0, y_A, y_B]
        self.axes.plot(xPointsMech, yPointsMech, 'o-', c='black')
        #Отрисовка направляющей
        xPointsGuid = [x_B - CSM.lengthRod / 2, x_B + CSM.lengthRod / 2]
        yPointsGuid = [(x_B - CSM.lengthRod / 2) * np.tan(CSM.angleGuid) + CSM.eccentrGuid / np.cos(CSM.angleGuid), 
                        (x_B + CSM.lengthRod / 2) * np.tan(CSM.angleGuid) + CSM.eccentrGuid / np.cos(CSM.angleGuid)]
        self.axes.plot(xPointsGuid, yPointsGuid, '--', c='orange')
        #Отрисовка стойки
        xPointsBody = [0, 0.3 * CSM.lengthCrank * np.sin(np.pi / 6), -0.3 * CSM.lengthCrank * np.sin(np.pi / 6), 0]
        yPointsBody = [0, -0.3 * CSM.lengthCrank , -0.3 * CSM.lengthCrank, 0]
        self.axes.plot(xPointsBody, yPointsBody, c='black')
        #Отрисовка ползуна
        x1 = x_B + 0.25 * CSM.lengthCrank
        x2 = x_B + 0.25 * CSM.lengthCrank
        x3 = x_B - 0.25 * CSM.lengthCrank
        x4 = x_B - 0.25 * CSM.lengthCrank
        y1 = y_B + 0.15 * CSM.lengthCrank
        y2 = y_B - 0.15 * CSM.lengthCrank
        y3 = y_B - 0.15 * CSM.lengthCrank
        y4 = y_B + 0.15 * CSM.lengthCrank
        rotX1 = x_B + (x1 - x_B) * np.cos(CSM.angleGuid) - (y1 - y_B) * np.sin(CSM.angleGuid)
        rotX2 = x_B + (x2 - x_B) * np.cos(CSM.angleGuid) - (y2 - y_B) * np.sin(CSM.angleGuid)
        rotX3 = x_B + (x3 - x_B) * np.cos(CSM.angleGuid) - (y3 - y_B) * np.sin(CSM.angleGuid)
        rotX4 = x_B + (x4 - x_B) * np.cos(CSM.angleGuid) - (y4 - y_B) * np.sin(CSM.angleGuid)
        rotY1 = y_B + (x1 - x_B) * np.sin(CSM.angleGuid) + (y1 - y_B) * np.cos(CSM.angleGuid)
        rotY2 = y_B + (x2 - x_B) * np.sin(CSM.angleGuid) + (y2 - y_B) * np.cos(CSM.angleGuid)
        rotY3 = y_B + (x3 - x_B) * np.sin(CSM.angleGuid) + (y3 - y_B) * np.cos(CSM.angleGuid)
        rotY4 = y_B + (x4 - x_B) * np.sin(CSM.angleGuid) + (y4 - y_B) * np.cos(CSM.angleGuid)
        xPointsRod = [rotX1, rotX2, rotX3, rotX4, rotX1]
        yPointsRod = [rotY1, rotY2, rotY3, rotY4, rotY1]
        self.axes.plot(xPointsRod, yPointsRod, c='black')
        #Параметры графика
        self.axes.set_aspect('equal')
        self.axes.set_title('Положение механизма')
        self.axes.set_xlabel('X, м')
        self.axes.set_ylabel('Y, м')
        minCoord = min(x_A, x_B, y_A, y_B)
        maxCoord = max(x_A, x_B, y_A, y_B)
        plt.xlim(minCoord - 0.2 * max(abs(maxCoord), abs(minCoord)), maxCoord + 0.2 * max(abs(maxCoord), abs(minCoord)))
        plt.ylim(minCoord - 0.2 * max(abs(maxCoord), abs(minCoord)), maxCoord + 0.2 * max(abs(maxCoord), abs(minCoord)))
        self.axes.annotate('O', (0.1 * CSM.lengthCrank, 0.1 * CSM.lengthCrank))
        self.axes.annotate('A', (x_A + 0.1 * CSM.lengthCrank, y_A + 0.1 * CSM.lengthCrank))
        self.axes.annotate('B', (x_B + 0.1 * CSM.lengthCrank, y_B + 0.25 * CSM.lengthCrank))
        self.axes.grid(True, c='lightgrey', alpha=0.5)
        self.fig.canvas.draw()

        self.labelLog.setText(f'Координаты точeк механизма:\n' +
                              f'А[{x_A*1000:.0f}, {y_A*1000:.0f}] мм.\n' +
                              f'B[{x_B*1000:.0f}, {y_B*1000:.0f}] мм.')
    
    
    def plotSpeed(self):
        """Метод обработки нажатия кнопки для построения плана скоростей"""
        #Проверки
        try:
            CSM = self.readData()
        except:
            self.labelLog.setText(f'Заполнны не все поля или\n'+
                                f'поля заполнены не числами.\n'+
                                f'Проверьте корректность\n'+
                                f'введенных данных.')
            errMessage = 'Ошибка:\nЗаполнены не все поля или поля заполнены не числами\n\n'
            self.logToFile(errMessage)
            return
        
        distanceToGuid = (abs(CSM.eccentrGuid / np.cos(CSM.angleGuid) / 
                         np.sqrt(1 + np.tan(CSM.angleGuid)**2)))
        minDistanceMech = (CSM.lengthRod - CSM.lengthCrank)
        if  minDistanceMech < distanceToGuid or CSM.lengthCrank == 0 or CSM.lengthRod == 0:
            self.labelLog.setText(f'Механизм с такими параметрами\n'+
                                f'не существует.\n'+
                                f'Проверьте корректность\n'+
                                f'введенных данных.')
            errMessage = 'Ошибка:\nМеханизм с такими параметрами не существует.\n\n'
            self.logToFile(errMessage)
            return

        v_A, angleV_A, v_BA, v_B, angleV_BA = CSM.findVelocity()
        
        plt.cla()
        #Отрисовка плана скоростей
        xPointV_A = v_A * np.cos(angleV_A)
        yPointV_A = v_A * np.sin(angleV_A)
        xPointV_B = v_B * np.cos(CSM.angleGuid)
        yPointV_B = v_B * np.sin(CSM.angleGuid)
        xLenVe_A = v_A * np.cos(angleV_A)
        yLenVe_A = v_A * np.sin(angleV_A)
        xLenVe_B = v_B * np.cos(CSM.angleGuid)
        yLenVe_B = v_B * np.sin(CSM.angleGuid)
        xLenVe_BA = v_BA * np.cos(angleV_BA)
        yLenVe_BA = v_BA * np.sin(angleV_BA)
        self.axes.quiver(0, 0, xLenVe_A, yLenVe_A, units='xy', scale=1, color='r')
        self.axes.quiver(xPointV_A, yPointV_A, xLenVe_BA, yLenVe_BA, units='xy', scale=1, color='g')
        self.axes.quiver(0, 0, xLenVe_B, yLenVe_B, units='xy', scale=1, color='b')
        self.axes.plot([0, xPointV_A], [0, yPointV_A], c='r', label='v_A')
        self.axes.plot([xPointV_A, xPointV_B], [yPointV_A, yPointV_B], c='g', label='v_BA')
        self.axes.plot([0, xPointV_B], [0, yPointV_B], c='b', label='v_B')
        #Параметры графика
        self.axes.grid(True, c='lightgrey', alpha=0.5)
        self.axes.set_aspect('equal')
        self.axes.set_title('План скоростей механизма')
        self.axes.legend()
        self.axes.set_xlabel('м/с')
        self.axes.set_ylabel('м/с')
        minVeh = min(xPointV_A, xPointV_B, yPointV_A, yPointV_B)
        maxVeh = max(xPointV_A, xPointV_B, yPointV_A, yPointV_B)
        plt.xlim(minVeh - 0.2 * max(abs(maxVeh), abs(minVeh)), maxVeh + 0.2 * max(abs(maxVeh), abs(minVeh)))
        plt.ylim(minVeh - 0.2 * max(abs(maxVeh), abs(minVeh)), maxVeh + 0.2 * max(abs(maxVeh), abs(minVeh)))
        self.fig.canvas.draw()

        self.labelLog.setText(f'Скорости точек механизма:\n' +
                              f'Cкорость точки А:\nv_А={abs(v_A):.2f} м/c.\n' +
                              f'Cкорость точки В:\nv_В={abs(v_B):.2f} м/c.\n' +
                              f'Oтносительная скорость:\nv_ВА={abs(v_BA):.2f} м/c.\n')
        

    def plotAcceleration(self):
        """Метод обработки нажатия кнопки для построения плана ускорений"""
        #Проверки
        try:
            CSM = self.readData()
        except:
            self.labelLog.setText(f'Заполнны не все поля или\n'+
                                f'поля заполнены не числами.\n'+
                                f'Проверьте корректность\n'+
                                f'введенных данных.')
            errMessage = 'Ошибка:\nЗаполнены не все поля или поля заполнены не числами\n\n'
            self.logToFile(errMessage)
            return
        distanceToGuid = (abs(CSM.eccentrGuid / np.cos(CSM.angleGuid) / 
                         np.sqrt(1 + np.tan(CSM.angleGuid)**2)))
        minDistanceMech = (CSM.lengthRod - CSM.lengthCrank)
        if  minDistanceMech < distanceToGuid or CSM.lengthCrank == 0 or CSM.lengthRod == 0:
            self.labelLog.setText(f'Механизм с такими параметрами\n'+
                                f'не существует.\n'+
                                f'Проверьте корректность\n'+
                                f'введенных данных.')
            errMessage = 'Ошибка:\nМеханизм с такими параметрами не существует.\n\n'
            self.logToFile(errMessage)
            return
        
        a_A, aNorm_BA, aTau_BA, a_B, angleRod = CSM.findAcceleration()
        a_BA = np.sqrt(aNorm_BA**2 + aTau_BA**2)

        plt.cla()
        #Отрисовка плана ускорений
        xPointA_A = -a_A * np.cos(CSM.angleCrank)
        yPointA_A = -a_A * np.sin(CSM.angleCrank)
        xPointA_N = xPointA_A - aNorm_BA * np.cos(angleRod)
        yPointA_N = yPointA_A - aNorm_BA * np.sin(angleRod)
        xPointA_B = xPointA_N - aTau_BA * np.cos(CSM.findVelocity()[4])
        yPointA_B = yPointA_N - aTau_BA * np.sin(CSM.findVelocity()[4])
        angleAccRod = np.arctan((yPointA_B - yPointA_A) / (xPointA_B - xPointA_A))
        xLenA_A = -a_A * np.cos(CSM.angleCrank)
        yLenA_A = -a_A * np.sin(CSM.angleCrank)
        xLenA_BA = -a_BA * np.cos(angleAccRod)
        yLenA_BA = -a_BA * np.sin(angleAccRod)
        xLenA_B = -a_B * np.cos(CSM.angleGuid)
        yLenA_B = -a_B * np.sin(CSM.angleGuid)
        
        #Костыль
        #Угол не всегда рассчитывается правильно.
        #Вектор поворачивается на 180 градусов.
        #В чем проблема не совсем понятно.
        isAngleAccRodTrue = (xPointA_B - (xPointA_A + xLenA_BA * np.cos(CSM.angleGuid)) < 0.001)
        if not isAngleAccRodTrue:
            xLenA_BA = a_BA * np.cos(angleAccRod)
            yLenA_BA = a_BA * np.sin(angleAccRod)
        
        self.axes.plot([0, xPointA_A], [0, yPointA_A], c='r', label='a_A')
        self.axes.plot([xPointA_A, xPointA_N], [yPointA_A, yPointA_N], '--', c='g')
        self.axes.plot([xPointA_N, xPointA_B], [yPointA_N, yPointA_B], '--', c='g')
        self.axes.plot([xPointA_A, xPointA_B], [yPointA_A, yPointA_B], c='g', label='a_BA')
        self.axes.plot([0, xPointA_B], [0, yPointA_B], c='b', label='a_B')
        self.axes.quiver(0, 0, xLenA_A, yLenA_A, units='xy', scale=1, color='r')
        self.axes.quiver(xPointA_A, yPointA_A, xLenA_BA, yLenA_BA, units='xy', scale=1, color='g')
        self.axes.quiver(0, 0, xLenA_B, yLenA_B, units='xy', scale=1, color='b')
        #Параметры графика
        minAcc = min(xPointA_A, xPointA_B, xPointA_N, yPointA_A, yPointA_B, yPointA_N)
        maxAcc = max(xPointA_A, xPointA_B, xPointA_N, yPointA_A, yPointA_B, yPointA_N)
        plt.xlim(minAcc - 0.2 * max(abs(maxAcc), abs(minAcc)), maxAcc + 0.2 * max(abs(maxAcc), abs(minAcc)))
        plt.ylim(minAcc - 0.2 * max(abs(maxAcc), abs(minAcc)), maxAcc + 0.2 * max(abs(maxAcc), abs(minAcc)))
        self.axes.grid(True, c='lightgrey', alpha=0.5)
        self.axes.set_aspect('equal')
        self.axes.set_title('План ускорений механизма')
        self.axes.legend()
        self.axes.set_xlabel('м/с^2')
        self.axes.set_ylabel('м/с^2')

        self.fig.canvas.draw()
        self.labelLog.setText(f'Ускорения точек механизма:\n' +
                              f'Ускорение точки А:\na_А={abs(a_A):.2f} м/c^2.\n' +
                              f'Ускорение точки В:\na_В={abs(a_B):.2f} м/c^2.\n' +
                              f'Oтносительное ускорение:\na_ВА={abs(a_BA):.2f} м/c^2.\n')
        

def plotSingleEmptyGraph():
    """Построение заготовки графика"""
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4.98, 5.19), dpi=85, facecolor='white', frameon=True,
                            edgecolor='black', linewidth=1)
    fig.subplots_adjust(wspace=0.4, hspace=0.4, left=0.15, right=0.85, top=0.9, bottom=0.1)
    axes.grid(True, c='lightgrey', alpha=0.5)
    return fig, axes


def prepareCanvas(parent=None):
    """Подготовка холста"""
    parent.fig, parent.axes = plotSingleEmptyGraph()
    parent.layoutForGraph = QVBoxLayout(parent.widgetResult)
    parent.canvas = MyCanvas(parent.fig)
    parent.layoutForGraph.addWidget(parent.canvas)
    parent.toolbar = NavigationToolbar2QT(parent.canvas, parent)
    parent.layoutForGraph.addWidget(parent.toolbar)


def main_application():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main_application()
