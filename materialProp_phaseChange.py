# This component defines the Enthalpy curve for your selected material, i.e. converts your into into a PCM
#
# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# 
# This file is part of Honeybee.
# 
# Copyright (c) 2013-2016, Michael Spencer Quinto <spencer.michael.q@gmail.com>  
# Honeybee is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# Honeybee is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>


"""
Use this component to define the temperature-enthalpy curve of an existing EPMaterial, 
You'll need at least three pairs of Temperature(C) and corresponding Enthalpy(J/kg) values.
-
The temperature – enthalpy set of inputs specify a two column tabular temperature-enthalpy function for the basic material. 
Sixteen pairs can be specified. Specify only the number of pairs necessary.
The tabular function must cover the entire temperature range that will be seen by the material in the simulation. It is suggested that the function start at a low temperature, and extend to 100C. 
Note that the function has no negative slopes and the lowest slope that will occur is the base material specific heat. Temperature values should be strictly increasing.
-
Also note, when using ConductionFiniteDifference, it is more efficient to set the zone timestep shorter than those used for the ConductionTransferFunction solution algorithm. 
It should be set to 12 timesteps per hour or greater, and can range up to 60.
-
check the EnergyPlus documentation for more details: http://bigladdersoftware.com/epx/docs/8-6/input-output-reference/group-surface-construction-elements.html#materialpropertyphasechange
-
Provided by Honeybee 0.0.60
    
    Args:
        _name:          Name of the existing EPMaterial you want to define as a PCM.
        coeff_:         [W/(m-K2)] Default value of 0.
                        This field is used to enter the temperature dependent coefficient for thermal conductivity of the material. 
                        This is the thermal conductivity change per unit temperature excursion from 20 C. The conductivity value at 
                        20 C is the one specified with the basic material properties of the regular material specified in the name field.
        _temp1:         (C) The corresponding temperature for _enthalpy1
        _enthalpy1:     (J/kg) The corresponding enthalpy for _temp1
        _temp2:         (C) The corresponding temperature for _enthalpy2
        _enthalpy2:     (J/kg) The corresponding enthalpy for _temp2
        _temp3:         (C) The corresponding temperature for _enthalpy3
        _enthalpy3:     (J/kg) The corresponding enthalpy for _temp3. 
                        Zoom into the component and click the "+" symbol to add more temp-enthalpy inputs
        _temp4:         (C) The corresponding temperature for _enthalpy4
        _enthalpy4:     (J/kg) The corresponding enthalpy for _temp4
        _temp5:         (C) The corresponding temperature for _enthalpy5
        _enthalpy5:     (J/kg) The corresponding enthalpy for _temp5
    Returns:
        EPMaterialWithPCM: A Phase Change Material that can be plugged into the "Honeybee_EnergyPlus Construction"
                            component, usually used for walls, floors, ceilings.

"""

ghenv.Component.Name = "Honeybee_EnergyPlus MaterialPropertyPhaseChange"
ghenv.Component.NickName = 'EPPhaseChange'
ghenv.Component.Message = 'VER 0.0.60\nDEC_26_2016'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "User"
ghenv.Component.SubCategory = "06 | Energy | Material | Construction"
#compatibleHBVersion = VER 0.0.56\nFEB_01_2015
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "0"
except: pass

import scriptcontext as sc
import Grasshopper.Kernel as gh
from math import floor

w = gh.GH_RuntimeMessageLevel.Warning

# set the correct names when adding input
def setInputNames():
    numInputs = ghenv.Component.Params.Input.Count
    
    for input in range(numInputs):
        if input == 0: 
            inputName = '_name'
            
        elif input == 1: 
            inputName = 'coeff_'
            
        elif (input%2 == 0 and input != 0):
            inputStr = int(floor(input / 2))
            inputName = '_temp' + str(inputStr)
            ghenv.Component.Params.Input[input].NickName = inputName
            ghenv.Component.Params.Input[input].Name = inputName
            
        elif (input%2 != 0 and input != 0):
            inputStr = int(floor(input / 2))
            inputName = '_enthalpy' + str(inputStr)
            ghenv.Component.Params.Input[input].NickName = inputName
            ghenv.Component.Params.Input[input].Name = inputName
            
        else: pass
        
    if (numInputs+2) > 36:
        err = "the maximum number of temperature-enthalpy pair values in EnergyPlus" + \
              "is 16, please limit the pairs to 16."
        raise ValueError(err)
        return -1
    
    #check that there is an even number of inputs 
    #(i.e. to make sure that each temp value has a corresponding enthalpy value and V.V.
    if (numInputs%2 != 0):
        err = "Each Temperature value must have its corresponding Enthalpy value"
        ghenv.Component.AddRuntimeMessage(w, err)
        return -1

def checkTemperature():
    #check to see that the temperature does not go below absolute zero
    
    #Also check that the temperature value for the the next temperature input must not be
    #lower than the previous input
    
    for tempInput in range(ghenv.Component.Params.Input.Count):
        #print tempInput
        if tempInput <= 1: pass #skip first two inputs
        
        elif tempInput%2 != 0: pass #skip odd-numbered (i.e. enthalpy) inputs from checking
        
        elif tempInput > 1 and tempInput%2 == 0: #check only temperature inputs
            #print tempInput
            layerName = ghenv.Component.Params.Input[tempInput].NickName
            exec('tempValue = ' + layerName)
            
            #absZero
            if tempValue < -273.15:
                msg = "The values for temperature can't be lower than absolute zero (i.e. -273.15 degrees celcius)!"
                ghenv.Component.AddRuntimeMessage(w, msg)
                return -1
                
            #check that current temp input must not be lower than previous
            if tempInput == 2:
                # if the the input is _temp1, we can't compare it to the previous temperature, hence this code
                # i.e. if input is temp1, the current tempvalue will be the same as the previous
                layerName2 = ghenv.Component.Params.Input[tempInput].NickName
                exec('tempValuePrev = ' + layerName2)
            
            else:
                layerName2 = ghenv.Component.Params.Input[tempInput - 2].NickName
                exec('tempValuePrev = ' + layerName2)
            
            if tempValue >= tempValuePrev: pass
            
            elif tempValue < tempValuePrev:
                currentInput = ghenv.Component.Params.Input[tempInput].Name
                prevInput = ghenv.Component.Params.Input[tempInput - 2].Name
                print currentInput, prevInput
                msg = "The temperature for '" + str(currentInput) + "' can't be lower than then temperature input for '" + str(prevInput) + "'"
                ghenv.Component.AddRuntimeMessage(w, msg)
                return -1
        else:
            pass

def setDefaults():
    #Check if there is a _name input.
    checkData = True
    if _name == None:
        checkData = False
        print "Connect an existing EPMaterial into _name."
        msg = "Connect an existing EPMaterial into _name."
        ghenv.Component.AddRuntimeMessage(w, msg)
        materialName = None
    else: materialName = _name
    
    #Set a default coeff.
    if coeff_ == None: 
        coeff = 0.0
    else: 
        coeff = coeff_
    
    return checkData, materialName, coeff

def checkHBLB():
    # check if LB and HB are flying {1}
    if not sc.sticky.has_key('ladybug_release')and sc.sticky.has_key('honeybee_release'):
        print "You should first let both Ladybug and Honeybee to fly..."
        ghenv.Component.AddRuntimeMessage(w, "You should first let both Ladybug and Honeybee to fly...")
        return -1
    # end check {1}
    
    # check compatibility of LB and HB {2}
    try:
        if not sc.sticky['honeybee_release'].isCompatible(ghenv.Component): return -1
        if sc.sticky['honeybee_release'].isInputMissing(ghenv.Component): return -1
    except:
        warning = "You need a newer version of Honeybee to use this compoent." + \
        " Use updateHoneybee component to update userObjects.\n" + \
        "If you have already updated userObjects drag Honeybee_Honeybee component " + \
        "into canvas and try again."
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, warning)
        return -1

    try:
        if not sc.sticky['ladybug_release'].isCompatible(ghenv.Component): return -1
    except:
        warning = "You need a newer version of Ladybug to use this compoent." + \
        " Use updateLadybug component to update userObjects.\n" + \
        "If you have already updated userObjects drag Ladybug_Ladybug component " + \
        "into canvas and try again."
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, warning)
        return -1
        
    # end check {2}
    
def main(name, coeff):
    
    hb_EPMaterialAUX = sc.sticky["honeybee_EPMaterialAUX"]()
    
    materialNames = []
    phasechangeStr = "MaterialProperty:PhaseChange,\n" + name.upper() +  ",    !- Name\n"
    
    for inputCount in range(ghenv.Component.Params.Input.Count):
        
        # zeroth input = the name of the EPMaterial, check if the Material exists
        if inputCount == 0:
            layerName = ghenv.Component.Params.Input[inputCount].NickName
            exec('materialName = ' + layerName)
            
            if materialName != None and len(materialName.split("\n")) == 1:
                materialName = materialName.upper()
                
            elif materialName != None:
                added, materialName = hb_EPMaterialAUX.addEPConstructionToLib(materialName, overwrite = True)
                materialName = materialName.upper()
                
            # double check that everything is fine
            if materialName in sc.sticky ["honeybee_materialLib"].keys():
                pass
                
            ######## does E+ allow window materials to be PCMs??? (PROBABLY NOT YET)???? #########
            #elif materialName  in sc.sticky ["honeybee_windowMaterialLib"].keys():
            #    pass
            ########
            
            else:
                msg = str(materialName) + " is not a valid material name/definition.\n" + \
                    "Create the material first and try again."
                ghenv.Component.AddRuntimeMessage(w, msg)
                return
                
        #Create string for the coeff input
        elif inputCount == 1:
            phasechangeStr += str(coeff) + ",    !- Temperature Coefficient for Thermal Conductivity {W/m-K2} " + "\n"
        
        #Concatenante strings for temp values
        elif (inputCount%2 == 0 and inputCount != 0 and inputCount != ghenv.Component.Params.Input.Count - 1):
            layerName = ghenv.Component.Params.Input[inputCount].NickName
            exec('tempValue = ' + layerName)
            phasechangeStr += str(tempValue) + ",    !- Temperature " +  str(int(floor(inputCount / 2))) + " {C} " + "\n"
        
        #enthalpy, except the last enthalpy value
        elif (inputCount%2 != 0 and inputCount != 0 and inputCount != ghenv.Component.Params.Input.Count - 1):
            layerName = ghenv.Component.Params.Input[inputCount].NickName
            exec('enthalpyValue = ' + layerName)
            phasechangeStr += str(enthalpyValue) + ",    !- Enthalpy " +  str(int(floor(inputCount / 2))) + " {J/kg} " + "\n"
        
        # last enthalpy value
        elif (inputCount == ghenv.Component.Params.Input.Count - 1):
            
            layerName = ghenv.Component.Params.Input[inputCount].NickName
            exec('enthalpyLastValue = ' + layerName)
            phasechangeStr += str(enthalpyLastValue) + ";    !- Enthalpy " +  str(int(floor(inputCount / 2))) + " {J/kg} "# + "\n"
        
        # should not happen
        else:
            pass
            #print "wtf"
            
    return phasechangeStr
    
checkData, _name, coeff_ = setDefaults()
checkHBLB = checkHBLB()
checkTemperature = checkTemperature()
setInputNames = setInputNames()

#print checkData, checkHBLB, checkTemperature, setInputNames
# check function returns before running main
if checkData == True and checkHBLB != -1 and checkTemperature != -1 and setInputNames != -1:
    EPMaterialWithPCM = main(_name, coeff_)
