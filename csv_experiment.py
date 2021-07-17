import threading
import os
import serial
import time
import tkinter
import datetime
from tkinter import *
import serial.tools.list_ports
connected="Connected"
disconnected="Disconnected"
error="Error"
# import pandas as pd
import csv
# import tModeSettings
# dict = {'Time Stamp':ct , 'Serial Number': serialNumber, 'T mode': tMode, 'T Value [Kg /Cm^3]': tValue, 'Flow[LPS]': varFlowrate, 'Voltage [V]': varVoltage, 'Current[A]'= varCurrent}

# ct = datetime.datetime.now() 
# Global Vaiables

tkTop = tkinter.Tk()

t1=tkinter.IntVar()
txt_T1=Entry(tkTop, bd=5, textvariable=t1, font=("Helvetica", 16), width=5)
txt_T1.place(x=70, y=500)
t2=tkinter.StringVar()
lbl_T2 = Label(tkTop, fg='black', relief="sunken",  borderwidth=4, font=("Helvetica", 16), bg='white', textvariable= t2, width=5)
lbl_T2.place(x=220, y=500)
t3=tkinter.StringVar()
lbl_T3 = Label(tkTop, fg='black', relief="sunken",  borderwidth=4, font=("Helvetica", 16), bg='white', textvariable= t3, width=5)
lbl_T3.place(x=370, y=500)
t4=tkinter.IntVar()
txt_T4=Entry(tkTop, bd=5, textvariable=t4, font=("Helvetica", 16), width=5)
txt_T4.place(x=520, y=500)

val=""
hey="hey"
filter_data = ""
serial_data=""
serial_buffer=""
tMode=""
tValue=""
b=""
ser=None    
sr=""
hey=52456
t1Csv=0.0
t2Csv=0.0
t3Csv=0.0
t4Csv=0.0
tFloatValue=0.0
voltageFloat=0.0
currentFloat=0.0
flowrateFloat=0.0
# def com_scanner():

with open('settings.csv') as csv_setting:
            data = csv.reader(csv_setting, delimiter=',')
            i=0
            for row in data:
                # print(row['T2'])
                if(i==1):
                    print(row[0])
                    t1.set(row[0])
                    t1Csv=float(row[0])
                    # print(row[1])
                    t2.set(row[1])
                    print(t2Csv)
                    t2Csv=float(row[1])
                    # print(row[2])
                    t3.set(row[2])
                    t3Csv=float(row[2])
                    # print(row[3])
                    t4.set(row[3])
                    t4Csv=float(row[3])
                    print(t4Csv)
                    i=0
                i=i+1
                

            csv_setting.close()

with open('rawdata.csv', mode='a') as csv_file:
    fieldnames = ['Time Stamp', 'Serial Number', 'T mode', 'T Value [Kg /Cm^3]','Flow[LPS]', 'Voltage [V]', 'Current[A]', 'P (kPa)','Actual Current (A)','PumpPower (W)', 'Electrical Power (W)', 'Total Efficiency']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    # writer.writeheader()
    csv_file.close()

def openPort():
    global ser
    check_presence
    port=textbox_portNumber.get()
    # if int(port)<0 or int(port)>20:
    #     status.set(error)
    #     lbl_connectColour.config(fg='red')
    ser = serial.Serial('COM' + str(port), 9600, timeout=0, writeTimeout=0)
    if ser==None:
        status.set(error)
        lbl_connectColour.config(fg='red')
    elif ser!=None:
        status.set(connected)
        lbl_connectColour.config(fg='green')

    # while True:
    #     myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    #     if port not in myports:
    #         status.set(disconnected)
    #         lbl_connectColour.config(fg='red')
    #         break
    #     else:
    #         status.set(connected)
    #         lbl_connectColour.config(fg='green')

    time.sleep(1)
    # ser.write(bytes(hey, 'UTF-8'))
    # val=textbox_file.get()
    # ser.write(bytes(val, 'UTF-8'))
    # print(val)
    # time.sleep(1)
    # t1 = threading.Thread(target = get_data)
    # t1.daemon = True
    # t1.start()
    
def quit():
    global ser
    global tkTop
    # ser.write(bytes('LMNO', 'UTF-8'))
    tkTop.destroy()

def checkPort():
    # global ser
    if ser.isOpen() == False:
        # ser.close()
        status.set(error)
        lbl_connectColour.config(fg='red')
    elif ser.isOpen() == True:
        status.set(connected)
        lbl_connectColour.config(fg='green')

def check_presence():
    port=textbox_portNumber.get()
    while True:
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        if port not in myports:
            status.set(disconnected)
            lbl_connectColour.config(fg='red')
            break
        else:
            status.set(connected)
            lbl_connectColour.config(fg='green')


def closePort():
    global ser
    ser.close()
    time.sleep(3)
    


def set_button1_state():
    global ser
    global val
    if not val:
        print("Sent Nothing")
    
    ser.write(bytes(val,'UTF-8'))
    print(portNum)
    print(val)
    # ser.write(test)
    ser.write(bytes(val,'UTF-8'))
    time.sleep(1)
    
    checkPort()
    print(val)
    

def update_gui():
    global filter_data
    while(1):
        if filter_data:
            try:
                varVoltage.set(filter_data[0])
                varCurrent.set(filter_data[1])
                varFlowrate.set(filter_data[2])
            except TypeError:
                pass

def get_data():
    global filter_data
    global serial_data
    global serial_buffer
    global ser
    global voltageFloat
    global currentFloat
    global flowrateFloat
    global b
    # serial_data = ser.readline().strip('\n').strip('\r')
    # filter_data = serial_data.split(',')
    # print(filter_data)
    ser.flushInput()
    while True:  
        # flushInput()
        c = ser.read().decode('ascii')
        # print(c)
        if c=='\n' or c=='\r' or c==" " or c=="''":
            serial_buffer=b
            serial_data=b
            b=""
            break
            # serial_buffer+=c
        b=b+c  
    # print(serial_data)    
    # print(b)  
    filter_data = serial_data.split(',')
    varVoltage.set(filter_data[0])
    varCurrent.set(filter_data[1])
    varFlowrate.set(filter_data[2])
    voltageFloat=float(filter_data[0])
    currentFloat=float(filter_data[1])
    flowrateFloat=float(filter_data[2])
    print(filter_data[0])
    # dict = {'Time Stamp':ct , 'Serial Number': serialNumber, 'T mode': tMode, 'T Value [Kg /Cm^3]': tValue, 'Flow[LPS]': varFlowrate, 'Voltage [V]': varVoltage, 'Current[A]'= varCurrent}
    
    # time.sleep(1)
def store_data():
    
    global filter_data
    global writer
    # global 
    global sr
    global tMode
    global t1Csv
    global t2Csv
    global t3Csv
    global t4Csv
    global voltageFloat
    global currentFloat
    global flowrateFloat
    ct = datetime.datetime.now()
    checkPort
    sr=txt_SerialNo_Part1.get()+txt_SerialNo_Part2.get()+txt_SerialNo_Part3.get()
    # dict = {'Time Stamp':[ct] , 'Serial Number': [serialNumber], 'T mode': [tMode], 'T Value [Kg /Cm^3]': [tValue], 'Flow[LPS]': [varFlowrate], 'Voltage [V]': [varVoltage], 'Current[A]': [varCurrent]}        
        # df = pd.DataFrame(dict, columns=['Time Stamp', 'Serial Number', 'T mode', 'T Value [Kg /Cm^3','Flow[LPS]', 'Voltage [V]', 'Current[A]'])
        # df.to_csv('rawdata.csv') 
    with open('settings.csv', mode='w', newline='') as csv_file:
            fieldnames = ['T1', 'T2', 'T3', 'T4']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'T1':txt_T1.get() , 'T2': t2.get(), 'T3': t3.get(), 'T4': txt_T4.get()})
    
    setRadio()
        
    tNumber = v.get()
    if tNumber==1:
        tMode="T1"
        tValue=txt_T1.get()
        tFloatValue=t1Csv
        tvalueError=""
        tvalue_select.set(tvalueError)
    elif tNumber==2:
        tMode="T2"
        tValue=t2.get()
        tFloatValue=t2Csv
        print(t2Csv)
        tvalueError=""
        tvalue_select.set(tvalueError)
        # print(t2)
    elif tNumber==3:
        tMode="T3"
        tValue=t3.get()
        tFloatValue=t3Csv
        tvalueError=""
        tvalue_select.set(tvalueError)
    elif tNumber==4:
        tMode="T4"
        tValue=txt_T4.get()
        tFloatValue=t4Csv
        tvalueError=""
        tvalue_select.set(tvalueError)
    else:
        tvalueError="Please select a T value"
        tvalue_select.set(tvalueError)
        lbl_tvalue.config(fg='red')

    with open('rawdata.csv', mode='a+', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # writer.writerow({'Time Stamp':[ct] , 'Serial Number': [serialNumber], 'T mode': [tMode], 'T Value [Kg /Cm^3]': [tValue], 'Flow[LPS]': [varFlowrate], 'Voltage [V]': [varVoltage], 'Current[A]': [varCurrent]})
        print(tFloatValue)
        P_in_kPa= tFloatValue*0.1019716213
        CurrentFixed = 9
        PumpPower = P_in_kPa*flowrateFloat
        ElectricalPower = voltageFloat*CurrentFixed 
        TotalEfficiency=(PumpPower/ElectricalPower)*100
        writer.writerow({'Time Stamp':ct , 'Serial Number': sr, 'T mode': tMode, 'T Value [Kg /Cm^3]': tValue, 'Flow[LPS]': filter_data[2], 'Voltage [V]': filter_data[0], 'Current[A]': filter_data[1],'P (kPa)': round(P_in_kPa,5),'Actual Current (A)': CurrentFixed,'PumpPower (W)':round(PumpPower,4) , 'Electrical Power (W)': ElectricalPower, 'Total Efficiency': round(TotalEfficiency,3)})

def settingButton():
    import tModeSettings
    os.system('c:/Users/Ritvi/tkinterAttempt1/tModeSettings.py')
    # if success==0:
    #     with open('settings.csv', mode='r') as csv_setting:
    #         fieldnames = ['Time Stamp', 'Serial Number', 'T mode', 'T Value [Kg /Cm^3','Flow[LPS]', 'Voltage [V]', 'Current[A]']
    #         reader = csv.DictWriter(csv_setting, fieldnames=fieldnames)

    #         csv_file.close()
    setRadio

def setRadio():
    global t1Csv
    global t2Csv
    global t3Csv
    global t4Csv
    with open('settings.csv') as csv_setting:
            data = csv.reader(csv_setting, delimiter=',')
            i=0
            for row in data:
                # print(row['T2'])
                if(i==1):
                    print(row[0])
                    t1.set(row[0])
                    t1Csv=float(row[0])
                    print(row[1])
                    t2.set(row[1])
                    print(t2Csv)
                    t2Csv=float(row[1])
                    print(row[2])
                    t3.set(row[2])
                    t3Csv=float(row[2])
                    print(row[3])
                    t4.set(row[3])
                    t4Csv=float(row[3])
                    print(t4Csv)
                    i=0
                i=i+1
                

            csv_setting.close()

def newWindow():
    setRadio
    tkT = Toplevel(tkTop)
    
    tkT.geometry('600x300+10+20')
    tkT.title("Settings")

    def save():
        with open('settings.csv', mode='w', newline='') as csv_file:
            fieldnames = ['T1', 'T2', 'T3', 'T4']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'T1':t1.get() , 'T2': t2.get(), 'T3': t3.get(), 'T4': t4.get()})
            # csv_file.close()
        tkT.destroy()

    def quit():
        # global ser
        # global tkTop
        # ser.write(bytes('LMNO', 'UTF-8'))
        tkT.destroy()

    # setRadio
    lbl_T1 = Label(tkT, fg='black', font=("Helvetica", 16), text="T1 = ")
    lbl_T1.place(x=50, y=10)
    t1=tkinter.StringVar()
    txt_T1=Entry(tkT, bd=5, textvariable=t1)
    txt_T1.place(x=200, y=10)
    lbl_T2 = Label(tkT, fg='black', font=("Helvetica", 16), text="T2 = ")
    lbl_T2.place(x=50, y=60)
    t2=tkinter.StringVar()
    txt_T2 = Entry(tkT, bd=5, textvariable= t2)
    txt_T2.place(x=200, y=60)
    t3=tkinter.StringVar()
    lbl_T3 = Label(tkT, fg='black', font=("Helvetica", 16), text="T3 = ")
    lbl_T3.place(x=50, y=110)
    txt_T3 = Entry(tkT, bd=5, textvariable= t3)
    txt_T3.place(x=200, y=110)
    lbl_T4 = Label(tkT, fg='black', font=("Helvetica", 16), text="T4 = ")
    lbl_T4.place(x=50, y=160)
    t4=tkinter.StringVar()
    txt_T4=Entry(tkT, bd=5, textvariable=t4)
    txt_T4.place(x=200, y=160)

    with open('settings.csv') as csv_setting:
            data = csv.reader(csv_setting, delimiter=',')
            i=0
            for row in data:
                # print(row['T2'])
                if(i==1):
                    print(row[0])
                    t1.set(row[0])
                    print(row[1])
                    t2.set(row[1])
                    print(row[2])
                    t3.set(row[2])
                    print(row[3])
                    t4.set(row[3])
                    i=0
                i=i+1
                

            csv_setting.close()

    saveButton= tkinter.Button(
        tkT,
        text="Save and Exit",
        command=save,
        height = 4,
        fg = "black",
        width = 10,
        bd = 5
    )
    saveButton.place(x=50, y=210)

    saveButton= tkinter.Button(
        tkT,
        text="Reload",
        command=setRadio,
        height = 4,
        fg = "black",
        width = 10,
        bd = 5
    )
    saveButton.place(x=400, y=210)

    tkButtonQuit = tkinter.Button(
        tkT,
        text="Quit",
        command=quit,
        height = 4,
        fg = "black",
        width = 8,
        bg = 'yellow',
        bd = 5
    )
    tkButtonQuit.place(x=140, y=210)

    # return setRadio

    
    
    

        
    # if filter_data:
    #     print(filter_data)
    #     print(serial_data)
    #     print(filter_data)
    #     varVoltage.set(filter_data[0])
    #     varCurrent.set(filter_data[1])
    #     varFlowrate.set(filter_data[2])
# ser = serial.Serial('COM' + str(port) + str(port), 9600, timeout=0, writeTimeout=0)
# print("Reset Arduino")
# time.sleep(3)
# ser.write(bytes(hey, 'UTF-8'))




                
    # time.sleep(1)
                

# tkTop.geometry('300x600')
# tkTop.title("IoT24hours")

# WIDTH = 800
# HEIGHT = 400
# w = tkinter.Canvas(tkTop, width=WIDTH, height=HEIGHT)

if __name__ == "__main__":

    # serialNumber=tkinter.IntVar()
    # w = tkinter.Canvas(tkTop, width=WIDTH, height=HEIGHT)
    # w.create_line(55, 85, 155, 85, 105, 180, 55, 85)
    # w.create_oval(event.x, event.y, event.x+25, event.y+25, outline="#000000", fill="#ff0000", width=1)


    lbl_ConnectStatus= Label(tkTop, text=" Connection Status:", fg='black', font=("Helvetica", 16))
    lbl_ConnectStatus.place(x=30, y=200)
    status=tkinter.StringVar()
    status.set(disconnected)
    lbl_connectColour= Label(tkTop,borderwidth = 3, text=" Disconnected", fg='red', font=("Helvetica", 16), textvariable=status)
    lbl_connectColour.place(x=230, y=200)
    lbl_portNumber= Label(tkTop, text=" Port COM", fg='black', font=("Helvetica", 16))
    lbl_portNumber.place(x=400, y=200)
    textbox_portNumber = tkinter.Entry(tkTop, text="PORT", font=("Helvetica", 16), width=5)
    textbox_portNumber.place(x=520,y=200)
    portNum=textbox_portNumber.get()

    lbl_H1 = Label(tkTop, text="Kethworks", bg='white', borderwidth=2, relief='ridge', fg='green', font=("Helvetica", 18))
    lbl_H1.place(x=350, y=20)
    lbl_H2 = Label(tkTop, text="Functional Test for Production", bg='white', borderwidth=2, relief='ridge', fg='black', font=("Helvetica", 18))
    lbl_H2.place(x=250, y=80)

    lbl_Serial = Label(tkTop, text="Serial Number", fg='black', font=("Helvetica", 16))
    lbl_Serial.place(x=50, y=400)
    txt_SerialNo_Part1=Entry(tkTop, text="KWR3B1", bd=5, font=("Helvetica", 16), width=12)
    txt_SerialNo_Part1.place(x=200, y=400)
    txt_SerialNo_Part2=Entry(tkTop, text="xxxx", bd=5, font=("Helvetica", 16), width=12)
    txt_SerialNo_Part2.place(x=400, y=400)
    txt_SerialNo_Part3=Entry(tkTop, text="1220", bd=5,  font=("Helvetica", 16), width=12)
    txt_SerialNo_Part3.place(x=600, y=400)
    
    txt_SerialNo_Part1.insert(END, 'KWR3B1')
    txt_SerialNo_Part2.insert(END, 'xxxx')
    txt_SerialNo_Part3.insert(END, '1220')


    Voltage_tag = tkinter.Label(tkTop, text = "Voltage", font=("Helvetica", 14))
    Voltage_tag.place(x=50, y=300)
    
    varVoltage = tkinter.IntVar()
    Voltage_read = tkinter.Label(tkTop, text = "00", bg='white', borderwidth=2, relief='ridge', textvariable=varVoltage, font=("Helvetica", 14), width=5)
    Voltage_read.place(x=150, y=300)

    Current_tag = tkinter.Label(tkTop, text = "Current",  font=("Helvetica", 14))
    Current_tag.place(x=250, y=300)
    
    varCurrent = tkinter.IntVar()
    Current_read = tkinter.Label(tkTop, text = "00", textvariable=varCurrent, bg='white', borderwidth=2, relief='ridge', font=("Helvetica", 14), width=5)
    Current_read.place(x=350, y=300)
    
    Flowrate_tag = tkinter.Label(tkTop, text = "Flow",  font=("Helvetica", 14))
    Flowrate_tag.place(x=450, y=300)
    
    varFlowrate = tkinter.IntVar()
    Flowrate_read = tkinter.Label(tkTop, text = "00", textvariable=varFlowrate, bg='white', borderwidth=2, relief='ridge', font=("Helvetica", 14), width=5)
    Flowrate_read.place(x=550, y=300)

   
    
    
    v = tkinter.IntVar()
    
    tkinter.Radiobutton(tkTop, 
               text="T1",
               padx = 20, 
               font=("Helvetica", 16),
               variable=v, 
               value=1).place(x=50, y=550)

    tkinter.Radiobutton(tkTop, 
               text="T2",
               padx = 20, 
               font=("Helvetica", 16),
               variable=v, 
               value=2).place(x=200, y=550)

    tkinter.Radiobutton(tkTop, 
               text="T3",
               padx = 20, 
               font=("Helvetica", 16),
               variable=v, 
               value=3).place(x=350, y=550)

    tkinter.Radiobutton(tkTop, 
               text="T4",
               padx = 20, 
               font=("Helvetica", 16),
               variable=v, 
               value=4).place(x=500, y=550)

    
    tvalue_select=tkinter.StringVar()
    lbl_tvalue=tkinter.Label(tkTop, fg='red',  textvariable= tvalue_select, font=("Helvetica", 11))
    lbl_tvalue.place(x=600, y=550)

    button2state = tkinter.Button(tkTop,
        text="Connect",
        command=openPort,
        height = 2,
        fg = "black",
        width = 8,
        bd = 5, 
        bg='light green',
        font=("Helvetica", 12)
    )
    button2state.place(x=700, y=180)

    button5state = tkinter.Button(tkTop,
        text="Get Data",
        command=get_data,
        height = 2,
        fg = "black",
        width = 8,
        bg='orange',
        font=("Helvetica", 12),
        bd = 5
    )
    button5state.place(x=700, y=280)

    button6state = tkinter.Button(tkTop,
        text="Record",
        command=store_data,
        height = 2,
        fg = "black",
        width = 6,
        bg='light blue',
        bd = 5,
        font=("Helvetica", 12)
    )
    button6state.place(x=700, y=650)

    tkButtonQuit = tkinter.Button(
        tkTop,
        text="Quit",
        command=quit,
        height = 2,
        fg = "black",
        width = 7,
        bg = 'light pink',
        bd = 5,
        font=("Helvetica", 12)
    )
    tkButtonQuit.place(x=110, y=650)

    tkButtonSettings = tkinter.Button(
        tkTop,
        text="Settings",
        command=newWindow,
        height = 2,
        fg = "black",
        width = 8,
        bg = 'yellow',
        bd = 5,
        font=("Helvetica", 12)
    )
    tkButtonSettings.place(x=20, y=650)

    tkButtonSettings = tkinter.Button(
        tkTop,
        text="Reload",
        command=setRadio,
        height = 2,
        fg = "black",
        width = 6,
        bg = 'light green',
        bd = 5,
        font=("Helvetica", 12)
    )
    tkButtonSettings.place(x=190, y=650)



    tkTop.geometry('900x800+10+20')
    tkTop.title("Data Recorder")   

    tkTop.mainloop()


