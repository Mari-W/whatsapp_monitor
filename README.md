# WhatsApp Monitor

## Description
Python script to monitor WhatsApp online times of a contact.

## Usage
* Enter contact names in config.cfg (Actual names like you would search for them in WA)
* Run script and wait until it asks you to scan the generated QR code.
* Scan the qr_waw.png (with white background!) with your WhatsApp App.
* Wait until contact does interact with WhatsApp (goes on/off)
* A .csv file will be generated and extended over time with online time ranges of contact in it.
* You can edit the config while script is running, new contacts added will be included in monitoring process.

##Libs
* Selenium
* psutil

##Other
I programmed this to show how much data we actually provide to everyone.
WhatsApp does NOT have a setting to hide online times.
You COULD use this to track sleep behaviour or interaction with other contacts you know.
But you know what, don't do it.