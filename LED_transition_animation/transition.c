#include "pico/stdlib.h"
#include <stdio.h>
#include "pico/time.h"
#include "hardware/irq.h"
#include "hardware/pwm.h"
#include "PicoType.h"
#include "pico/cyw43_arch.h"

uint buttonLeft = 20;
uint buttonMid = 21;
uint buttonRight = 22;
uint flag = 0;
const uint num_of_led = 29;
uint led [29];
uint brightness = 20000;
//bool flag = true;

void clearall(){
     for (int i =0 ; i< num_of_led; i++){
        gpio_put(led[i], 0);
    }
}

// animation one: lighting led up one by one untill all leds are on, turning them off one by one in the same way
void flashOne(){
    clearall();
    for (int i =0 ; i< num_of_led; i++){
        if (!gpio_get(buttonLeft) ||!gpio_get(buttonMid) || !gpio_get(buttonRight) ){
            clearall();
            return ;
        }
        gpio_put(led[i], 1);
        sleep_ms(50);
    }
    sleep_ms(50);
    for (int i =0 ; i< num_of_led; i++){
        if (!gpio_get(buttonLeft) ||!gpio_get(buttonMid) || !gpio_get(buttonRight) ){
            clearall();
            return ;
        }
        gpio_put(led[i], 0);
        sleep_ms(50);
    }

}
void flashTwo(){
    clearall();
    for (int i = 0; i < 3; i ++){
        uint separator = 3;
        uint count = i;
        while (count < num_of_led){
            gpio_put(led[count], 1);
            count +=separator;
        }
        if (!gpio_get(buttonLeft) ||!gpio_get(buttonMid) || !gpio_get(buttonRight) ){
            clearall();
            return ;
        }
        sleep_ms(50);
        clearall();
    }
    
    
}
void flashThree(){
    clearall();

    for (int j = 0; j < num_of_led -1 ; j++){
        for (int i = num_of_led-2; i >= j ; i--){
            gpio_put(led[i], 1);
            if (i<num_of_led-1 ){
                gpio_put(led[i+1],0);
            }
            if (!gpio_get(buttonLeft) ||!gpio_get(buttonMid) || !gpio_get(buttonRight) ){
            clearall();
            return ;
            }
            sleep_ms(100);
        }
        
        sleep_ms(500);
}   

}


int main(){     
    for (int i = 0; i < num_of_led; i++){
        led[i] = i;
        gpio_init(led[i]);
        gpio_set_dir(led[i], GPIO_OUT);

    }
    gpio_init(buttonLeft);
    gpio_init(buttonMid);
    gpio_init(buttonRight);
    gpio_set_dir(buttonLeft, GPIO_IN);
    gpio_pull_up(buttonLeft);
    gpio_set_dir(buttonMid, GPIO_IN);
    gpio_pull_up(buttonMid);
    gpio_set_dir(buttonRight, GPIO_IN);
    gpio_pull_up(buttonRight);

    while (1){
        if (!gpio_get(buttonLeft)){flag = 1;}
        else if (!gpio_get(buttonMid)){flag = 2;}
        else if (!gpio_get(buttonRight)){flag = 3; }

        if (flag == 1){
           flashOne();
        }
        else if (flag == 2){
           flashTwo();
        }
        else if (flag == 3){
            flashThree();
        }
        else{
            for (int i = 0 ; i < num_of_led; i++){
                 gpio_put(led[i],1);  
            }
           
        }

    }


}