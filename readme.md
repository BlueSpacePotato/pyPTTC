<figure>
    <img 
        src="https://vigophotonics.com/app/uploads/sites/3/2022/06/ptcc-01-1024x683-1.webp"
        href="https://vigophotonics.com/us/products/infrared-detection-modules/accessories/"
        alt="ptcc smarttec controller"
        style="float: center; margin: 10px;"
    />
    <figcaption>
        <a href="https://vigophotonics.com/us/products/infrared-detection-modules/accessories/">Vigo Photonics</a> PTCC Smarttec Controller. <a href="https://vigophotonics.com/us/">[Source]</a>   
    </figcaption>
</figure>


# Project is under development

# pyPTTC

Python toolbox for controlling the Vigo System SmartTec PTTC-01-ADV detector.


# Requirements

- python >= 3.8


# Installation

- `pip install -r requierments.txt`


# Example

```python3

import pyPTCC

```


# Infos

## BasicObject
The BasicObject only contains single information.

<table>
    <thead>
        <tr style="text-align:center">BasicObject</tr>
    </thead>
    <tbody>
        <tr>
            <td>obj_id</td>
            <td>dlen</td>
            <td>data</td>
        </tr>
        <tr>
            <td>unique obj id</td>
            <td>size of obj</td>
            <td>basic data</td>
        </tr>
    </tbody>
</table>

## ContainerObject


size of object = (`obj_id` + `dlen` + size of `Data`) = (2 Byte + 2 Byte + size of `data`)


# Known Issues
If the detector is connected to the USB port but not to the power supply, the FDTI chip is found and the serial port opens without error. But when you send data to the port, you get no response.

If you get an Port-Permission-denied-error on linux trying to open the port, you could try: 
```
chmod a+rw /dev/ttyUSBx 
```
