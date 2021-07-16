
/*
 * serial_usb_simple_arduino - For communicating over USB serial. Send it a '1' (character one) 
 * and it will make the builtin LED start blinking every one second. Send it a '0' 
 * (character zero) and it will make it stop blinking.
 * 
 * Each time it receives one of the commands, it sends back an 'A' for acknowledge.
 * But send it a commmand it doesn't recognize and it sends back an 'E' for error.
 */

bool blinking = false;
bool led_on = false;
int target_time;

void setup()
{
    Serial.begin(115200);
    while (!Serial)
    {
        ; // wait for serial port to connect. Needed for native USB
    }
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
    char c;

    if (Serial.available() > 0)
    {
        c = Serial.read();
        switch (c)
        {
        case '0':
            // stop blinking
            blinking = false;
            if (led_on)
            {
                digitalWrite(LED_BUILTIN, LOW);
            }
            Serial.write("A", 1);
            break;
        case '1':
            // start blinking
            if (blinking == false)
            {
                blinking = true;
                digitalWrite(LED_BUILTIN, HIGH);
                led_on = true;
                target_time = millis() + 100; // turn off in 1 tenth of a second (100 milliseconds)
            }
            Serial.write("A", 1);
            break;
        default:
            Serial.write("E", 1);
            break;
        }
    }
    else if (blinking)
    {
        if (millis() >= target_time)
        {
            if (led_on)
            {
                digitalWrite(LED_BUILTIN, LOW);
                led_on = false;
                target_time = millis() + 100; // turn on in 1 tenth of a second (100 milliseconds)
            }
            else
            {
                digitalWrite(LED_BUILTIN, HIGH);
                led_on = true;
                target_time = millis() + 100; // turn off in 1 tenth of a second (100 milliseconds)
            }
        }
    }
}
