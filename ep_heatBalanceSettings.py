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
Settings for simulations involving Phase Change Materials, specifically SurfaceConvectionAlgorithms and HeatBalanceSettings.
Don't forget to set your timestep to 6 or higher (20 or higher is recommended).
-
Provided by Honeybee 0.0.60
    
    Args:
        surfConvAlgoInside_:        (Default: TARP), other values:
                                    Simple, CeilingDiffuser, and AdaptiveConvectionAlgorithm. (see http://bigladdersoftware.com/epx/docs/8-6/input-output-reference/group-simulation-parameters.html#surfaceconvectionalgorithminside)
        surfConvAlgoOutside_:       (Default: DOE-2), other values:
                                    SimpleCombined, TARP, MoWiTT, DOE-2, and AdaptiveConvectionAlgorithm.. (see http://bigladdersoftware.com/epx/docs/8-6/input-output-reference/group-simulation-parameters.html#surfaceconvectionalgorithminside)                        
        heatBalanceAlgorithm_:      (ConductionFiniteDifference is the default for simulations involving PCMs)
        ++++++++++++++:         
        differenceScheme_:          (Default: FullyImplicitFirstOrder).
                                    CrankNicholsonSecondOrder scheme is second order in time and may be faster. 
                                    But it can be unstable over time when boundary conditions change abruptly and severely.
                                    The FullyImplicitFirstOrder scheme is first order in time and is more stable over time. But it may be slower.
        discretizationConst_:       (Default: 3). This field controls how the model determines spatial discretization, or the count of nodes across each material layer in the construction.
                                    Typical values are from 1 to 3. Lower values for this constant lead to more nodes and finer-grained space discretization.
        relaxationFactor_:          (Default: 1). (Range: from 0.01 to 1). This input field can optionally be used to modify the starting value for the relaxation factor.
                                    Larger numbers may solve faster, while smaller numbers may be more stable.
        insideFaceSurfTempConv_:    (Default: 0.002). (Range: from 0.0000001 to 0.01). Lower values may further increase stability at the expense of longer runtimes, 
                                    while higher values may decrease runtimes but lead to possible instabilities.
    Returns:
        SurfConv_HeatBal:           Surface Convection Settings, Heat Balance Algorithm and HeatBalanceSettings:ConductionFiniteDifference Settings.
"""

ghenv.Component.Name = "Honeybee_EnergyPlus HeatBalanceSettings"
ghenv.Component.NickName = 'EPHeatBalance'
ghenv.Component.Message = 'VER 0.0.60\nJAN_07_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "User"
ghenv.Component.SubCategory = "06 | Energy | Material | Construction"
#compatibleHBVersion = VER 0.0.56\nFEB_01_2015
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "0"
except: pass

import scriptcontext as sc
import Grasshopper.Kernel as gh

w = gh.GH_RuntimeMessageLevel.Warning

# set the correct names when adding input

ghenv.Component.Params.Input[0].NickName = "surfConvAlgoInside_"
ghenv.Component.Params.Input[0].Name = "SurfaceConvectionAlgorithm:Inside"
ghenv.Component.Params.Input[1].NickName = "surfConvAlgoOutside_"
ghenv.Component.Params.Input[1].Name = "SurfaceConvectionAlgorithm:Outside"
ghenv.Component.Params.Input[2].NickName = "heatBalanceAlgorithm_"
ghenv.Component.Params.Input[2].Name = "HeatBalanceAlgorithm"
ghenv.Component.Params.Input[3].NickName = "++++++++++++++"
ghenv.Component.Params.Input[3].Name = "++++++++++++++"
ghenv.Component.Params.Input[4].NickName = "differenceScheme_"
ghenv.Component.Params.Input[4].Name = "Difference Scheme"
ghenv.Component.Params.Input[5].NickName = "discretizationConst_"
ghenv.Component.Params.Input[5].Name = "Space Discretization Constant"
ghenv.Component.Params.Input[6].NickName = "relaxationFactor_"
ghenv.Component.Params.Input[6].Name = "Relaxation Factor"
ghenv.Component.Params.Input[7].NickName = "insideFaceSurfTempConv_"
ghenv.Component.Params.Input[7].Name = "Inside Face Surface Temperature Convergence Criteria" 

def setDefaults(surfConvAlgoInside_, surfConvAlgoOutside_, heatBalanceAlgorithm_, \
                differenceScheme_, discretizationConst_, relaxationFactor_, insideFaceSurfTempConv_):
                    
    checkData = True
    
    #
    surfAlgoInsideOptions = ["Simple", "TARP", "CeilingDiffuser", "AdaptiveConvectionAlgorithm"]
    if surfConvAlgoInside_ == None: 
        surfConvAlgoInside_ = "TARP"
        
    elif surfConvAlgoInside_ in surfAlgoInsideOptions: 
        surfConvAlgoInside_ = surfAlgoInsideOptions[surfAlgoInsideOptions.index(surfConvAlgoInside_)]
        
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        warning = "Invalid 'surfConvAlgoInside_' input, please select from \"Simple\", \"TARP\", \"CeilingDiffuser\", \"AdaptiveConvectionAlgorithm\""
        ghenv.Component.AddRuntimeMessage(w, warning)
        checkData = False
        return -1
        
    #
    surfAlgoOutsideOptions = ["SimpleCombined", "TARP", "MoWiTT", "DOE-2", "AdaptiveConvectionAlgorithm"]
    if surfConvAlgoOutside_ == None: 
        surfConvAlgoOutside_ = "DOE-2"
        
    elif surfConvAlgoOutside_ in surfAlgoOutsideOptions: 
        surfConvAlgoOutside_ = surfAlgoOutsideOptions[surfAlgoOutsideOptions.index(surfConvAlgoOutside_)]
        
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        warning = "Invalid 'surfConvAlgoOutside_' input, please select from \"SimpleCombined\", \"TARP\", \"MoWiTT\", \"DOE-2\", \"AdaptiveConvectionAlgorithm\""
        ghenv.Component.AddRuntimeMessage(w, warning)
        checkData = False
        return -1
        
    #
    if heatBalanceAlgorithm_ == None:
        heatBalanceAlgorithm_ = "ConductionFiniteDifference"
    
    elif heatBalanceAlgorithm_ == "ConductionFiniteDifference":
        heatBalanceAlgorithm_ = "ConductionFiniteDifference"
        
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        warning = "Invalid input for 'heatBalanceAlgorithm_', Only 'ConductionFiniteDifference' is valid for simulations involving PCMs"
        ghenv.Component.AddRuntimeMessage(w, warning)
        checkData = False
        return -1
    
    #
    differenceScheme_Options = ["CrankNicholsonSecondOrder", "FullyImplicitFirstOrder"]
    if differenceScheme_ == None:
        differenceScheme_ = "FullyImplicitFirstOrder"
        
    elif differenceScheme_ in differenceScheme_Options:
        differenceScheme_ = differenceScheme_Options[differenceScheme_Options.index(differenceScheme_)]
        
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        warning = "Invalid input for 'differenceScheme_', please select from \"CrankNicholsonSecondOrder\", \"FullyImplicitFirstOrder\""
        ghenv.Component.AddRuntimeMessage(w, warning)
        checkData = False
        return -1
        
    #
    if discretizationConst_ == None:
        discretizationConst_ = 3.0
    
    else:
        try:
            discretizationConst_ = float(discretizationConst_)
            
        except:
            w = gh.GH_RuntimeMessageLevel.Warning
            warning = "Invalid input for 'discretizationConst_', Please input a valid number"
            ghenv.Component.AddRuntimeMessage(w, warning)
            checkData = False
            return -1
        
    #
    if relaxationFactor_ == None:
        relaxationFactor_ = 1.0
        
    elif (relaxationFactor_ >= 0.01) and (relaxationFactor_ <= 1):
        pass
        
    elif (relaxationFactor_ < 0.01) or (relaxationFactor_ > 1):
        w = gh.GH_RuntimeMessageLevel.Warning
        warning = "Invalid input for 'relaxationFactor_', The number should be between 0.01 and 1"
        ghenv.Component.AddRuntimeMessage(w, warning)
        checkData = False
        return -1
        
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        warning = "Invalid input for 'relaxationFactor_', Enter a valid input"
        ghenv.Component.AddRuntimeMessage(w, warning)
        checkData = False
        return -1
    
    #
    if insideFaceSurfTempConv_ == None:
        insideFaceSurfTempConv_ = 0.002
    
    elif (insideFaceSurfTempConv_ >= 0.0000001) and (insideFaceSurfTempConv_ <= 0.01):
        pass
        
    elif (insideFaceSurfTempConv_ < 0.0000001) or (insideFaceSurfTempConv_ > 0.01):
        w = gh.GH_RuntimeMessageLevel.Warning
        warning = "Invalid input for 'insideFaceSurfTempConv_', The number should be between 0.0000001 and 0.01"
        ghenv.Component.AddRuntimeMessage(w, warning)
        checkData = False
        return -1
        
    else:
        w = gh.GH_RuntimeMessageLevel.Warning
        warning = "Invalid input for 'insideFaceSurfTempConv_', Enter a valid input"
        ghenv.Component.AddRuntimeMessage(w, warning)
        checkData = False
        return -1
        
        
    return checkData, surfConvAlgoInside_, surfConvAlgoOutside_, heatBalanceAlgorithm_, \
            differenceScheme_, discretizationConst_, relaxationFactor_, insideFaceSurfTempConv_
            
            
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


def main(surfConvAlgoInside_, surfConvAlgoOutside_, heatBalanceAlgorithm_, \
                differenceScheme_, discretizationConst_, relaxationFactor_, insideFaceSurfTempConv_):
    
    #print heatBalanceAlgorithm_
    phasechangeStr = ""
    phasechangeStr += "SurfaceConvectionAlgorithm:Inside," + str(surfConvAlgoInside_) + ";\n" + "\n"
    phasechangeStr += "SurfaceConvectionAlgorithm:Outside," + str(surfConvAlgoOutside_) + ";\n" + "\n"
    phasechangeStr += "HeatBalanceAlgorithm," + str(heatBalanceAlgorithm_) + ";\n" + "\n"
    phasechangeStr += "HeatBalanceSettings:ConductionFiniteDifference,\n"
    phasechangeStr += str(differenceScheme_) + ",                   !- Difference Scheme\n"                    
    phasechangeStr += str(discretizationConst_) + ",                   !- Space Discretization Constant\n"
    phasechangeStr += str(relaxationFactor_) + ",                   !- Relaxation Factor\n"
    phasechangeStr += str(insideFaceSurfTempConv_) + ";                   !- Inside Face Surface Temperature Convergence Criteria\n"
    
            
    return phasechangeStr
    
    
## set default values
checkData, surfConvAlgoInside_, surfConvAlgoOutside_, \
heatBalanceAlgorithm_, differenceScheme_, discretizationConst_, \
relaxationFactor_, insideFaceSurfTempConv_ = setDefaults(surfConvAlgoInside_, \
                                        surfConvAlgoOutside_, \
                                        heatBalanceAlgorithm_, differenceScheme_, \
                                        discretizationConst_, relaxationFactor_, \
                                        insideFaceSurfTempConv_)
#checkHBLB = checkHBLB()  # not yet needed

#print checkData, checkHBLB, checkTemperature, setInputNames
# check function returns before running main
if checkData == True and checkData != -1:
    SurfConv_HeatBal = main(surfConvAlgoInside_, \
                                        surfConvAlgoOutside_, \
                                        heatBalanceAlgorithm_, differenceScheme_, \
                                        discretizationConst_, relaxationFactor_, \
                                        insideFaceSurfTempConv_)
