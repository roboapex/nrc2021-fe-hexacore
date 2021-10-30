### Arduino to Raspberry Pi Communication

The Arduino is used in tandem with the Raspberry Pi as the Raspberry Pi, which is the main logic processor, is unable to directly control DC motors due to too low voltage. Hence, Serial communication between the Raspberry Pi and Arduino is used to control the magnitude and direction of steering.

Data via Serial is sent in 2 bytes, one for the velocity of each wheel—left and right when facing forward.