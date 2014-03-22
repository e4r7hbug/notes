# Adafruit Gemma/Trinket On Ubuntu
Some quick tips to using the Gemma/Trinket ATtiny85 boards.

## Ubuntu 13.10
### Install
1. Install Arduino IDE
```bash
$ sudo apt-get update
$ sudo apt-get install arduino
```
1. Open Arduino, should prompt to add you to `dailout` group
1. Logout and login, or reboot machine
1. Follow instructions: http://learn.adafruit.com/introducing-gemma/setting-up-with-arduino-ide
  * Add ATtiny85 support
  * Download `trinkethardwaresupport.zip`
  * Extract and move `hardware` directory to `~/sketchbook/hardware/`
1. Update avrdude.conf
  * Download `avrdude.conf`
  * Move original configuration
  ```bash
$ sudo mv /etc/avrdude.conf /etc/avrdude.conf.orig`
  ```
  * Move new configuration
  ```bash
$ sudo mv ~/Downloads/avrdude.conf /etc/
  ```
1. Allow `dailout` group access to Gemma/Trinket over USB
  * Monitor System Log
  ```bash
$ tail -f /var/log/syslog
  ```
  * Plug in Gemma/Trinket, look for something like
  ```bash
Mar 22 03:32:28 tinytower mtp-probe: checking bus 3, device 5: "/sys/devices/pci0000:00/0000:00:14.0/usb3/3-3"
  ```
  * View attributes
  ```bash
$ udevadm info -a -p /sys/devices/pci0000:00/0000:00:14.0/usb3/3-3
  ```
  * Look for valuable attributes:
  ```bash
SUBSYSTEM=="usb"
ATTR{idVendor}=="1781"
ATTR{idProduct}=="0c9f"
ATTR{product}=="Trinket"
  ```
  * Create new `udev` rule
  ```bash
$ sudo nano /etc/udev/rules.d/60-trinket-usb.rules
"SUBSYSTEM=="usb", ATTR{product}=="Trinket", ATTR{idProduct}=="0c9f", ATTRS{idVendor}=="1781", MODE="0660", GROUP="dialout"
```
  * Restart `udev` service
  ```bash
$ sudo restart udev
  ```

### Check
#### Terminal
1. Get Gemma/Trinket into Boot Mode (push button or re-plug USB cable)
1. From regular terminal, try accessing device
```bash
$ avrdude -c usbtiny -p m8

avrdude: AVR device initialized and ready to accept instructions

Reading | ################################################## | 100% 0.00s

avrdude: Device signature = 0x1e930b
avrdude: Expected signature for ATMEGA8 is 1E 93 07
         Double check chip, or use -F to override this check.

avrdude done.  Thank you.
```

#### Arduino IDE
1. Open Arduino
1. Set `Tools > Boards > Adafruit {Gemma 8MHz|Trinket 8MHz|Trinket 16MHz}`
1. Set `Tools > Programmer > USBtinyISP`
1. Upload test sketch from Adafruit
```arduino
/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.

  To upload to your Gemma or Trinket:
  1) Select the proper board from the Tools->Board Menu
  2) Select USBtinyISP from the Tools->Programmer
  3) Plug in the Gemma/Trinket, make sure you see the green LED lit
  4) For windows, install the USBtiny drivers
  5) Press the button on the Gemma/Trinket - verify you see
     the red LED pulse. This means it is ready to receive data
  6) Click the upload button above within 10 seconds
*/
 
int led = 1; // blink 'digital' pin 1 - AKA the built in red LED

// the setup routine runs once when you press reset:
void setup() {
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);

}

// the loop routine runs over and over again forever:
void loop() {
    digitalWrite(led, HIGH); 
    delay(500);
    digitalWrite(led, LOW);
    delay(1000);
}
```
