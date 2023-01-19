#!/usr/bin/env python3
from ev3dev.ev3 import *
import os
import time
os.system('setfont Lat15-TerminusBold14')

#Variables referentes al motor
mR = LargeMotor('outA');
mR.stop_action = 'hold';
mL = LargeMotor('outB');
mL.stop_action = 'hold';
us = UltrasonicSensor();
us.mode = 'US-DIST-CM';

log_depuracion = open("log_depuracion.txt", "w");
log_sensor = open("log_sensor.txt", "w");
contador_depuracion = 1;
contador_sensor = 1;
angle = 10;
correction_speed = 20;
normal_speed = 120;
#Espacio de funciones
def move_ticks(right_m,left_m,speed):
        mR.run_to_rel_pos(position_sp=-(right_m), speed_sp=speed);
        mL.run_to_rel_pos(position_sp=left_m, speed_sp=speed);

def wait_for_both():
        mR.wait_while('running', timeout=100);
        mL.wait_while('running', timeout=100);

def rotate(num):
        global angle;
        global normal_speed;
        for x in range(num):
                write_log_sensor();
                move_ticks(angle,angle,normal_speed);
                wait_for_both();
                correction();
                write_log_depuracion();

def write_log_depuracion():
        global contador_depuracion;
        global angle;
        log_depuracion.write(str(contador_depuracion)+" "+str(contador_depuracion*angle)+ "--> " + "mR: " + str(mR.position) + " mL: " + str(mL.position) + "\n");
        contador_depuracion = contador_depuracion + 1;

def write_log_sensor():
        global contador_sensor;
        global contador_depuracion;
        aux = contador_depuracion - 1;
        log_sensor.write(str(contador_sensor)+":"+str(measure())+":"+str(aux*5.2173)+"\n");
        contador_sensor = contador_sensor + 1;

def measure():
        global us;
        time.sleep(0.2);
        distance = us.value();
        return distance/10;

def correction():
        global correction_speed;
        global contador_depuracion;
        global angle;
        right_pos = abs(mR.position);
        left_pos = abs(mL.position);
        error_right = contador_depuracion*angle - right_pos;
        error_left = contador_depuracion*angle - left_pos;

        while(abs(error_right) > 1 or abs(error_left) > 1):
                print("correcting");
                move_ticks(error_right,error_left,correction_speed);
                wait_for_both();
                right_pos = abs(mR.position);
                left_pos = abs(mL.position);
                error_right = contador_depuracion*angle - right_pos;
                error_left = contador_depuracion*angle - left_pos;

rotate(69);
log_depuracion.close();
log_sensor.close();