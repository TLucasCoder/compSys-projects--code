
#include "pico/stdlib.h"
#include <stdio.h>
#include "pico/time.h"
#include "hardware/irq.h"
#include "hardware/pwm.h"
#include "PicoType.h"

uint led [29];
uint brightness = 0;
bool flag = true;
bool start_flag = false;
bool stop_ring_flag = false;
uint timer = 1000;
uint button1ID = 20;
uint button2ID = 21;
uint button3ID = 22;


void updateBrightness(void) {
    // Clears the LED via is PWM slice.
    for (int i = 0 ; i< 29 ; i++){
        uint ledd = led[i];
        pwm_clear_irq(pwm_gpio_to_slice_num(ledd));
    
        // Changes the brightness value. It changes its direction once it gets to a certain value.
        if (flag) {
            if (brightness >= 27500) {flag = false;}
            else{brightness += 50;}
        }
        else {
            if (brightness <= 0) { flag = true;}
            else{
                brightness -= 1;
                }
        }
        // Updates the PWM of the brightness.
        pwm_set_gpio_level(ledd, brightness);
    }
}

void ring_alarm(){
    while (/*stop_ring_flag == false*/ 1  ){
       
        for (int i = 0 ; i < 19; i++){

            led[i] = i;  
            // Initialises the IO and gets the LED's slice.
            gpio_set_function(led[i], GPIO_FUNC_PWM);
            uint slice_num = pwm_gpio_to_slice_num(led[i]);
            // Clears the irq, enables it and sets up the brightness handler.
            pwm_clear_irq(slice_num);
            pwm_set_irq_enabled(slice_num, true);
            irq_set_exclusive_handler(PWM_IRQ_WRAP, updateBrightness);
            irq_set_enabled(PWM_IRQ_WRAP, true);

            // Initilises the PWM itself.
            pwm_config config = pwm_get_default_config();
            pwm_config_set_clkdiv(&config, 4.f);
            pwm_init(slice_num, &config, true);
         
        }
        sleep_ms(2000);
        if(!gpio_get(button3ID)){
            gpio_put(27,0);
            irq_set_enabled(PWM_IRQ_WRAP, false);
            for(int i = 0 ; i < 19; i++){
                gpio_put(i,0);
            }
            start_flag = !start_flag;
            return;
       }
    
    }
}

void timer_start(){
    gpio_put(27,1);
    while(timer != 0){
       sleep_ms(100);
       timer -= 100;
       if (timer % 1000 == 0){
          gpio_put(timer / 1000 + 1,0);
       }
       if(!gpio_get(button3ID)){
            gpio_put(27,0);
            start_flag = !start_flag;
            return;
       }
    }
    ring_alarm();
}


int main() {
    
    for (int i = 0; i < 16; i++){
        led[i] = i;
        gpio_init(led[i]);
        gpio_set_dir(led[i],GPIO_OUT);
    }
    gpio_init(button1ID);
    gpio_set_dir(button1ID,GPIO_IN);
    gpio_init(button2ID);
    gpio_set_dir(button2ID,GPIO_IN);
    gpio_init(button3ID);
    gpio_set_dir(button3ID,GPIO_IN);
    gpio_init(17);
    gpio_set_dir(17,GPIO_OUT);
    gpio_init(18);
    gpio_set_dir(18,GPIO_OUT);
    gpio_init(27);
    gpio_set_dir(27,GPIO_OUT);
    gpio_init(28);
    gpio_set_dir(28,GPIO_OUT);
    


    // Main loop for the program.
    while (1) { 
        gpio_put(0,1);
        gpio_put(1,1);
        gpio_pull_up(20);
        gpio_pull_up(21);
        gpio_pull_up(22);

         if (!gpio_get(button3ID)){
            start_flag = !start_flag;
            if (start_flag && timer > 1000){
                timer_start();
            }
         }
         if (start_flag == false){
            if (!gpio_get(button1ID) && timer  > 1000){
                gpio_put(timer / 1000, 0);
                timer -=1000;    
                if(!gpio_get(button1ID)){
                }
                sleep_ms(100);
            }
            if (!gpio_get(button2ID) && timer < 15 * 1000){
                timer +=1000 ;
                gpio_put(timer / 1000, 1);
                sleep_ms(100);

            }
         }
         
    }
}