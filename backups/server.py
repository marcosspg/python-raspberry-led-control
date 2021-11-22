# 7b41d3

def getNumeroNuevoRango(num):
    OldRange = (255 - 0)  
    NewRange = (100 - 0)  
    return (((int("0x"+num, 0) - 0) * NewRange) / OldRange) + 0


print(getNumeroNuevoRango("7b"));
print(getNumeroNuevoRango("41"));
print(getNumeroNuevoRango("d3"));



def hexaToNewRange(hexa):
    if(hexa.__len__()==6):
        new = {}
        new["r"] = getNumeroNuevoRango(hexa[0:2]);
        new["g"] = getNumeroNuevoRango(hexa[2:4]);
        new["b"] = getNumeroNuevoRango(hexa[4:6]);
        return new;
    else:
        return None;   



print(hexaToNewRange("f57fc2"));
