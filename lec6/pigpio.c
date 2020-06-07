#include <stdio.h>
#include <pigpiod_if2.h>
const int PORT=17;
//gcc -Wall -pthread -o prog prog.c -lpigpio -lrt
int main(){
    int pi=pigpio_start(NULL,NULL);
    set_PWM_range(pi, PORT, 256);
    gpioSetPWMfrequency(PORT, 256);
    gpioPWM(PORT,128);
    //printf("d"，gpioGetPWMdutycycle(PORT));
    pigpio_stop(pi);
}