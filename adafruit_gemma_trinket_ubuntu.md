# Adafruit Gemma/Trinket On Ubuntu
Some quick tips to using the Gemma/Trinket ATtiny85 boards.

## Ubuntu 13.10
1. Install Arduino IDE
```bash
$ sudo apt-get update
$ sudo apt-get install arduino
```
1. Open Arduino, should prompt to add you to `dailout` group
1. Logout and login, or reboot machine
1. Follow instructions: http://learn.adafruit.com/introducing-gemma/setting-up-with-arduino-ide
   1. Add ATtiny85 support
      1. Download `trinkethardwaresupport.zip`
      1. Extract and move `hardware` directory to `~/sketchbook/hardware/`
   1. Update avrdude.conf
      1. Download `avrdude.conf`
      1. Move original configuration, `$ sudo mv /etc/avrdude.conf /etc/avrdude.conf.orig`
      1. Move new configuration, `$ sudo mv ~/Downloads/avrdude.conf /etc/`
1. Allow `dailout` group access to Gemma/Trinket over USB
   1. Monitor System Log, `$ tail -f /var/log/syslog`
   1. Plug in Gemma/Trinket, look for something like `Mar 22 03:32:28 tinytower mtp-probe: checking bus 3, device 5: "/sys/devices/pci0000:00/0000:00:14.0/usb3/3-3"`
   1. View attributes, `$ udevadm info -a -p /sys/devices/pci0000:00/0000:00:14.0/usb3/3-3`
   1. Look for valuable attributes:
```
  looking at device '/devices/pci0000:00/0000:00:14.0/usb3/3-3':
    KERNEL=="3-3"
    SUBSYSTEM=="usb"
...
    ATTR{idVendor}=="1781"
...
    ATTR{idProduct}=="0c9f"
    ATTR{bDeviceClass}=="ff"
    ATTR{product}=="Trinket"
```
   1. Create new `udev` rule, `$ sudo nano /etc/udev/rules.d/60-trinket-usb.rules`
```
"SUBSYSTEM=="usb", ATTR{product}=="Trinket", ATTR{idProduct}=="0c9f", ATTRS{idVendor}=="1781", MODE="0660", GROUP="dialout"
```
   1. Restart `udev` service, `$ sudo restart udev`
