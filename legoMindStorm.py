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
#variables
contador_depuracion = 1;
contador_sensor = 1;
#constantes
log_depuracion = open("log_depuracion.txt", "w");
log_sensor = open("log_sensor.txt", "w");
angle = 10;
correction_speed = 25;
normal_speed = 100;

#Espacio de funciones
def move_ticks(right_m,left_m,speed,sense): #giro a izquierda sense = 1, giro a derecha sense = -1
        mR.run_to_rel_pos(position_sp=-sense*(right_m), speed_sp=speed);
        mL.run_to_rel_pos(position_sp=sense*left_m, speed_sp=speed);

def wait_for_both():
        mR.wait_while('running', timeout=100);
        mL.wait_while('running', timeout=100);

def rotate(num,sense):
        global angle;
        global normal_speed;
        global contador_depuracion;
        for x in range(num):
                write_log_sensor();
                move_ticks(angle,angle,normal_speed,sense);
                wait_for_both();
                correction(contador_depuracion,sense);
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
        time.sleep(0.1);
        distance = us.value();
        return distance/10;

def correction(iter,sense):
        global correction_speed;
        global angle;
        right_pos = abs(mR.position);
        left_pos = abs(mL.position);
        error_right = iter*angle - right_pos;
        error_left = iter*angle - left_pos;

        while(abs(error_right) > 1 or abs(error_left) > 1):
                print("correcting");
                move_ticks(error_right,error_left,correction_speed,sense);
                wait_for_both();
                right_pos = abs(mR.position);
                left_pos = abs(mL.position);
                error_right = iter*angle - right_pos;
                error_left = iter*angle - left_pos;

def rotate_half(sense):
        global normal_speed;
        global angle;
        for x in range(1,35):
                move_ticks(angle,angle,normal_speed-50,sense);
                wait_for_both();
                correction(x,sense);
        move_ticks(angle/2,angle/2,normal_speed-70,sense);
        wait_for_both();

def reset_motors():
        global contador_depuracion;
        global contador_sensor;
        mR.reset();
        mL.reset();
        contador_depuracion = 1;
        contador_sensor = 1;
        time.sleep(0.3);



reset_motors();
rotate(69,-1);
reset_motors();
rotate(69,1);
reset_motors();
rotate_half(1);
reset_motors();
rotate_half(-1);

log_depuracion.close();
log_sensor.close();