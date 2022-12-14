# modbus_sim_interface


Modbus TCP Master på port 502 på avtalt IP


### Function Code 03 request K-Sim (order)

Register 1: Lever Order Forward Azimuth Range:  0-100  (%)
Register 2: Lever Order Aft Azimuth  Range: 0-100 (%)
Register 3: Azimuth Order Forward Azimuth Range:  0-359 (deg)
Register 4: Azimuth Order Aft Azimuth  Range: 0-359 (deg)

 

### Function Code 16 request K-Sim  (feedback)

Register 101: Power Forward Azimuth Range:  0-1250 (kW)
Register 102: Lever Feedback Forward Azimuth  Range: 0-100 (%)
Register 103: Azimuth Feedback Forward Azimuth Range:  0-359 (deg)
Register 104: Power Aft Azimuth Range:  0-1250 (kW)  
Register 105: Lever Feedback Aft Azimuth Range: 0-100 (%)
Register 106: Azimuth Feedback Aft Azimuth Range:  0-359 (deg)


## Requirements

[pymodbus](https://github.com/riptideio/pymodbus)

`pip install pymodbus`
