#
# DSMR P1 uitlezer
# (c) 11-2017 2016 - GJ - gratis te kopieren en te plakken

versie = "1.0"
import sys
import serial
from influxdb import InfluxDBClient

################
#Error display #
################
def show_error():
    ft = sys.exc_info()[0]
    fv = sys.exc_info()[1]
    print("Fout type: %s" % ft )
    print("Fout waarde: %s" % fv )
    return


################################################################################################################################################
#Main program
################################################################################################################################################
print ("DSMR 2.2 P1 uitlezer",  versie)
print ("Control-C om te stoppen")

# client = InfluxDBClient(host='192.168.1.2', port=8086)
# print (client.get_list_database())
# client.switch_database('energie')

#Set COM port config
ser = serial.Serial()
ser.baudrate = 9600
ser.bytesize=serial.SEVENBITS
ser.parity=serial.PARITY_EQUAL
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"

#Open COM port
try:
    ser.open()
except:
    sys.exit ("Fout bij het openen van %s. Programma afgebroken."  % ser.name)      


#Initialize
# stack is mijn list met de 26 regeltjes.
p1_teller=0
stack=[]
# interval waarin data weggeschreven wordt -> 1 cyclus vanuit meter is ~1 sec --> 60 *1 = 1 minuut
# huidig verbruik elke 10 cycli, totaalwaardes elke 60 cycli.         
cycle = 0    
while 1:
    p1_raw = ser.readline()
    p1_str=str(p1_raw)
    # print (p1_str)
    if "ISK5" in p1_str:
        # print ("reset teller naar 0")
        p1_teller = 0
        if cycle ==10:
            # json_body_10s = [
            #     {
            #         "measurement": "P1_PB22",
            #         "tags": {
            #             "device": "P1-meterkast",
            #             },
            #         "fields": {
            #             "verbruik_nu": verbruik_in_watt,
            #             "teruglevering_nu": terug_in_watt,
            #             "laag_tarief_verbruik_totaal": laag_tarief_verbruik_totaal,
            #             "hoog_tarief_verbruik_totaal": hoog_tarief_verbruik_totaal,
            #             "laag_tarief_opbrengst_totaal": laag_tarief_opbrengst_totaal,
            #             "hoog_tarief_opbrengst_totaal": hoog_tarief_opbrengst_totaal,
            #             "gas_totaal": gas_totaal
            #         }
            #     }
            # ]
            # client.write_points(json_body_10s)
            cycle = 1
        else:        
            cycle += 1
        print ("Cyclus: ",cycle)
        # print (p1_teller)
    else: 
        p1_teller = p1_teller +1

        # if "1-0:1.7.0" in p1_str:
        #     print(p1_str[12:18])
        #     verbruik_in_watt = float(p1_str[12:18])*1000
        #     print ("Verbruik Nu:                    ", verbruik_in_watt, "W")  
        # search_for item and print result"
        if "1-0:1.8.1" in p1_str:
            laag_tarief_verbruik_totaal = float(p1_str[13:22])
            print ("Laag Tarief Verbruik Totaal:    ", laag_tarief_verbruik_totaal, " kWh")
        elif "1.8.2" in p1_str:
            hoog_tarief_verbruik_totaal = float(p1_str[13:22])
            print ("Hoog Tarief Verbruik Totaal:    ", hoog_tarief_verbruik_totaal, " kWh")
        elif "1-0:2.8.1" in p1_str:
            laag_tarief_opbrengst_totaal = float(p1_str[13:22])
            print ("Laag Tarief Opbrengst Totaal:   ", laag_tarief_opbrengst_totaal, " kWh")
        elif "1-0:2.8.2" in p1_str:
            hoog_tarief_opbrengst_totaal = float(p1_str[13:22])
            print ("Hoog Tarief Opbrengst Totaal:   ", hoog_tarief_opbrengst_totaal, " kWh")
        elif "1-0:1.7.0" in p1_str:
            verbruik_in_watt = float(p1_str[12:18])*1000
            print ("Verbruik Nu:                    ", verbruik_in_watt, "W")    

        elif "1-0:2.7.0" in p1_str:
            terug_in_watt = float(p1_str[12:18])*1000
            print ("Teruglevering Nu:               ", terug_in_watt, " W")   
        elif "0-1:24.2.1" in p1_str:
            gas_totaal = float(p1_str[28:36])
            print ("Gas Totaal:                     ", gas_totaal, " m3 \n")       
 

#Close port and show status
try:
    ser.close()
except:
    sys.exit ("Oops %s. Programma afgebroken." % ser.name )      
