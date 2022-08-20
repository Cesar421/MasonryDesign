import os
import sys
import comtypes.client

# set the following flag to True to attach to an existing instance of the program
# otherwise a new instance of the program will be started
AttachToInstance = False

# set the following flag to True to manually specify the path to ETABS.exe
# this allows for a connection to a version of ETABS other than the
# latest installation
# otherwise the latest installed version of ETABS will be launched
SpecifyPath = False

# if the above flag is set to True, specify the path to ETABS below
ProgramPath = "C:\Program Files\Computers and Structures\ETABS 17\ETABS.exe"

# full path to the model
# set it to the desired path of your model
APIPath = 'C:\CSi_ETABS_API_Example'
if not os.path.exists(APIPath):
    try:
        os.makedirs(APIPath)
    except OSError:
        pass
ModelPath = APIPath + os.sep + 'API_1-001.edb'

if AttachToInstance:
    # attach to a running instance of ETABS
    try:
        # get the active ETABS object
        myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        sys.exit(-1)

else:
    # create API helper object
    helper = comtypes.client.CreateObject('ETABSv17.Helper')
    helper = helper.QueryInterface(comtypes.gen.ETABSv17.cHelper)
    if SpecifyPath:
        try:
            # 'create an instance of the ETABS object from the specified path
            myETABSObject = helper.CreateObject(ProgramPath)
        except (OSError, comtypes.COMError):
            print("Cannot start a new instance of the program from " + ProgramPath)
            sys.exit(-1)
    else:

        try:
            # create an instance of the ETABS object from the latest installed ETABS
            myETABSObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
        except (OSError, comtypes.COMError):
            print("Cannot start a new instance of the program.")
            sys.exit(-1)

    # start ETABS application
    myETABSObject.ApplicationStart()

# create SapModel object
SapModel = myETABSObject.SapModel

# initialize model
SapModel.InitializeNewModel()

# create new blank model
ret = SapModel.File.NewBlank()

# switch to k-ft units
kN_m_C = 6
ret = SapModel.SetPresentUnits(kN_m_C)


# define material property
MATERIAL_CONCRETE = 2
ret = SapModel.PropMaterial.SetMaterial('CONCRETO 28 MPa', MATERIAL_CONCRETE)
ret = SapModel.PropMaterial.SetMaterial('CONCRETO 21 MPa', MATERIAL_CONCRETE)

# assign isotropic mechanical properties to material and non linear properties
ret = SapModel.PropMaterial.SetMPIsotropic('CONCRETO 28 MPa', 24855578.06, 0.2, 0.0000099)
ret = SapModel.PropMaterial.SetOConcrete('CONCRETO 28 MPa', 28000, False, 0, 1, 4, 0.002219, 0.005)

ret = SapModel.PropMaterial.SetMPIsotropic('CONCRETO 21 MPa', 21525562.37, 0.2, 0.0000099)
ret = SapModel.PropMaterial.SetOConcrete('CONCRETO 21 MPa', 21000, False, 0, 1, 4, 0.001922, 0.005)

# define rectangular frame section property
ret = SapModel.PropFrame.SetRectangle('Columna 0.3 x 0.3', 'CONCRETO 28 MPa', 0.3, 0.3)
# define frame section property modifiers
ModValue = [1, 1, 1, 1, 1, 1, 1, 1]
ret = SapModel.PropFrame.SetModifiers('Columna 0.3 x 0.3', ModValue)

# refresh view, update (initialize) zoom
ret = SapModel.View.RefreshView(0, False)

# add load patterns

ret = SapModel.LoadPatterns.Add('DeadSp', 2, 0, True)
ret = SapModel.LoadPatterns.Add('Live', 3, 0, True)
ret = SapModel.LoadPatterns.Add('Le', 3, 0, True)
ret = SapModel.LoadPatterns.Add('Granizo', 7, 0, True)
ret = SapModel.LoadPatterns.Add('Rooflive', 11, 0, True)
ret = SapModel.LoadPatterns.Add('Notional Dead x', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional Dead y', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional DeadSp x', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional DeadSp y', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional Live x', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional Live y', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional Rooflive x', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional Rooflive y', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional Granizo x', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional Granizo y', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional Le x', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Notional Le y', 12, 0, True)
ret = SapModel.LoadPatterns.Add('Fx', 5, 0, True)
ret = SapModel.LoadPatterns.Add('Fy', 5, 0, True)
ret = SapModel.LoadPatterns.Add('Fx con excel', 5, 0, True)
ret = SapModel.LoadPatterns.Add('Fy con excel', 5, 0, True)
ret = SapModel.LoadPatterns.Add('Wind +x', 6, 0, True)
ret = SapModel.LoadPatterns.Add('Wind -x', 6, 0, True)
ret = SapModel.LoadPatterns.Add('Wind +y', 6, 0, True)
ret = SapModel.LoadPatterns.Add('Wind -y', 6, 0, True)


# add Mass source
MyLoadPat = ['DeadSp', 'Rooflive', 'Dead', 'Live']
MySF = [1, 0.05, 1, 0.1]
ret = SapModel.PropMaterial.SetMassSource(2, 4, MyLoadPat, MySF)

# Define Function RS
# In diesem Moment, kann man nicht diese Method finden, bist jetzt gibt es nicht eine Lösung

# add load cases response spectrum
# In diesem Moment, kann man nicht diese Method finden, bist jetzt gibt es nicht eine Lösung


# Add load combos

# ___________________________________________________________________________________

# Crear un combo solo de Dead y solo de Live ( con granizo si se considera correcto)

# ___________________________________________________________________________________

ret = SapModel.RespCombo.Add("Ex", 0)
ret = SapModel.RespCombo.SetCaseList("Ex", 0, "Fx", 0.2)

ret = SapModel.RespCombo.Add("Ey", 0)
ret = SapModel.RespCombo.SetCaseList("Ey", 0, "Fy", 0.2)

ret = SapModel.RespCombo.Add("DeadTotal", 0)
ret = SapModel.RespCombo.SetCaseList("DeadTotal", 0, "Dead", 1.0)
ret = SapModel.RespCombo.SetCaseList("DeadTotal", 0, "DeadSp", 1.0)

# Combo 1 ----------------------------------------------------------------------------------------

ret = SapModel.RespCombo.Add("1.4*Dead", 0)
ret = SapModel.RespCombo.SetCaseList("1.4*Dead", 1, "DeadTotal", 1.4)

# Combo 2 ----------------------------------------------------------------------------------------

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Live+0.5*Rooflive", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Live+0.5*Rooflive", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Live+0.5*Rooflive", 0, "Live", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Live+0.5*Rooflive", 0, "Rooflive", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Live+0.5*Granizo", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Live+0.5*Granizo", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Live+0.5*Granizo", 0, "Live", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Live+0.5*Granizo", 0, "Granizo", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Live+0.5*Le", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Live+0.5*Le", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Live+0.5*Le", 0, "Live", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Live+0.5*Le", 0, "Le", 0.5)

# Combo 3 ----------------------------------------------------------------------------------------

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Rooflive+1.0*Live", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+1.0*Live", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+1.0*Live", 0, "Rooflive", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+1.0*Live", 0, "Live", 1.0)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Rooflive+0.8*Wind +x", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind +x", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind +x", 0, "Rooflive", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind +x", 0, "Wind +x", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Rooflive+0.8*Wind -x", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind -x", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind -x", 0, "Rooflive", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind -x", 0, "Wind -x", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Rooflive+0.8*Wind +y", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind +y", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind +y", 0, "Rooflive", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind +y", 0, "Wind +y", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Rooflive+0.8*Wind -y", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind -y", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind -y", 0, "Rooflive", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Rooflive+0.8*Wind -y", 0, "Wind -y", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Granizo+1.0*Live", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+1.0*Live", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+1.0*Live", 0, "Granizo", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+1.0*Live", 0, "Live", 1.0)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Granizo+0.8*Wind +x", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind +x", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind +x", 0, "Granizo", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind +x", 0, "Wind +x", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Granizo+0.8*Wind -x", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind -x", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind -x", 0, "Granizo", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind -x", 0, "Wind -x", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Granizo+0.8*Wind +y", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind +y", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind +y", 0, "Granizo", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind +y", 0, "Wind +y", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Granizo+0.8*Wind -y", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind -y", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind -y", 0, "Granizo", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Granizo+0.8*Wind -y", 0, "Wind -y", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Le+1.0*Live", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+1.0*Live", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+1.0*Live", 0, "Le", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+1.0*Live", 0, "Live", 1.0)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Le+0.8*Wind +x", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind +x", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind +x", 0, "Le", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind +x", 0, "Wind +x", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Le+0.8*Wind -x", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind -x", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind -x", 0, "Le", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind -x", 0, "Wind -x", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Le+0.8*Wind +y", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind +y", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind +y", 0, "Le", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind +y", 0, "Wind +y", 0.8)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Le+0.8*Wind -y", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind -y", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind -y", 0, "Le", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Le+0.8*Wind -y", 0, "Wind -y", 0.8)

# Combo 4 ----------------------------------------------------------------------------------------

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Rooflive", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Rooflive", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Rooflive", 0, "Wind +x", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Rooflive", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Rooflive", 0, "Rooflive", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Rooflive", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Rooflive", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Rooflive", 0, "Wind -x", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Rooflive", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Rooflive", 0, "Rooflive", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Rooflive", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Rooflive", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Rooflive", 0, "Wind +y", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Rooflive", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Rooflive", 0, "Rooflive", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Rooflive", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Rooflive", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Rooflive", 0, "Wind -y", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Rooflive", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Rooflive", 0, "Rooflive", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Granizo", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Granizo", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Granizo", 0, "Wind +x", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Granizo", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Granizo", 0, "Granizo", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Granizo", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Granizo", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Granizo", 0, "Wind -x", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Granizo", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Granizo", 0, "Granizo", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Granizo", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Granizo", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Granizo", 0, "Wind +y", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Granizo", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Granizo", 0, "Granizo", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Granizo", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Granizo", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Granizo", 0, "Wind -y", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Granizo", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Granizo", 0, "Granizo", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Le", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Le", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Le", 0, "Wind +x", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Le", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Le", 0, "Le", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Le", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Le", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Le", 0, "Wind -x", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Le", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Le", 0, "Le", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Le", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Le", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Le", 0, "Wind +y", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Le", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Le", 0, "Le", 0.5)

ret = SapModel.RespCombo.Add("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Le", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Le", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Le", 0, "Wind -y", 1.6)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Le", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Le", 0, "Le", 0.5)

# Combo 5 ----------------------------------------------------------------------------------------

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live + 1.0*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex", 1, "Ex", 1)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live - 1.0*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ex", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ex", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ex", 1, "Ex", -1)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live + 1.0*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey", 1, "Ey", 1)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live - 1.0*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ey", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ey", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ey", 1, "Ey", -1)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live + 1.0*Ex + 0.3*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex + 0.3*Ey", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex + 0.3*Ey", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex + 0.3*Ey", 1, "Ex", 1)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex + 0.3*Ey", 1, "Ey", 0.3)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live + 1.0*Ex -0.3*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex -0.3*Ey", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex -0.3*Ey", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex -0.3*Ey", 1, "Ex", 1)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ex -0.3*Ey", 1, "Ey", -0.3)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live -1.0*Ex -0.3*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live -1.0*Ex -0.3*Ey", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live -1.0*Ex -0.3*Ey", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live -1.0*Ex -0.3*Ey", 1, "Ex", -1)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live -1.0*Ex -0.3*Ey", 1, "Ey", -0.3)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live - 1.0*Ex + 0.3*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ex + 0.3*Ey", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ex + 0.3*Ey", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ex + 0.3*Ey", 1, "Ex", -1)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ex + 0.3*Ey", 1, "Ey", 0.3)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live + 1.0*Ey + 0.3*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey + 0.3*Ex", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey + 0.3*Ex", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey + 0.3*Ex", 1, "Ey", 1)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey + 0.3*Ex", 1, "Ex", 0.3)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live + 1.0*Ey -0.3*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey -0.3*Ex", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey -0.3*Ex", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey -0.3*Ex", 1, "Ey", 1)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live + 1.0*Ey -0.3*Ex", 1, "Ex", -0.3)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live -1.0*Ey -0.3*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live -1.0*Ey -0.3*Ex", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live -1.0*Ey -0.3*Ex", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live -1.0*Ey -0.3*Ex", 1, "Ey", -1)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live -1.0*Ey -0.3*Ex", 1, "Ex", -0.3)

ret = SapModel.RespCombo.Add("1.2*Dead + 1*Live - 1.0*Ey + 0.3*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ey + 0.3*Ex", 1, "DeadTotal", 1.2)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ey + 0.3*Ex", 0, "Live", 1.0)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ey + 0.3*Ex", 1, "Ey", -1)
ret = SapModel.RespCombo.SetCaseList("1.2*Dead + 1*Live - 1.0*Ey + 0.3*Ex", 1, "Ex", 0.3)

# Combo 6 ----------------------------------------------------------------------------------------
# Esta combinación es interesante para cubiertas o geometrías complejas, si se desea se puede usar
# la raíz cuadrada de la acción de viento en cada dirección, ejemplo
# raíz((wind +x)**2+(wind +y)**2)**1/2,
# si se requiere solo basta con crearlas, !!!!recordar el caso del edifico Citicorp Center¡¡¡¡¡.

ret = SapModel.RespCombo.Add("0.9*Dead + 1.6*Wind +x", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.6*Wind +x", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.6*Wind +x", 0, "Wind +x", 1.6)

ret = SapModel.RespCombo.Add("0.9*Dead + 1.6*Wind -x", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.6*Wind -x", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.6*Wind -x", 0, "Wind -x", 1.6)

ret = SapModel.RespCombo.Add("0.9*Dead + 1.6*Wind +y", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.6*Wind +y", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.6*Wind +y", 0, "Wind +y", 1.6)

ret = SapModel.RespCombo.Add("0.9*Dead + 1.6*Wind -y", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.6*Wind -y", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.6*Wind -y", 0, "Wind -y", 1.6)

# Combo 7 ----------------------------------------------------------------------------------------

ret = SapModel.RespCombo.Add("0.9*Dead + 1.0*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ex", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ex", 1, "Ex", 1)

ret = SapModel.RespCombo.Add("0.9*Dead - 1.0*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ex", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ex", 1, "Ex", -1)

ret = SapModel.RespCombo.Add("0.9*Dead + 1.0*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ey", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ey", 1, "Ey", 1)

ret = SapModel.RespCombo.Add("0.9*Dead - 1.0*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ey", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ey", 1, "Ey", -1)

ret = SapModel.RespCombo.Add("0.9*Dead + 1.0*Ex + 0.3*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ex + 0.3*Ey", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ex + 0.3*Ey", 1, "Ex", 1)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ex + 0.3*Ey", 1, "Ey", 0.3)

ret = SapModel.RespCombo.Add("0.9*Dead - 1.0*Ex + 0.3*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ex + 0.3*Ey", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ex + 0.3*Ey", 1, "Ex", -1)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ex + 0.3*Ey", 1, "Ey", 0.3)

ret = SapModel.RespCombo.Add("0.9*Dead - 1.0*Ex - 0.3*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ex - 0.3*Ey", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ex - 0.3*Ey", 1, "Ex", -1)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ex - 0.3*Ey", 1, "Ey", -0.3)

ret = SapModel.RespCombo.Add("0.9*Dead + 1.0*Ex - 0.3*Ey", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ex - 0.3*Ey", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ex - 0.3*Ey", 1, "Ex", 1)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ex - 0.3*Ey", 1, "Ey", -0.3)

ret = SapModel.RespCombo.Add("0.9*Dead + 1.0*Ey + 0.3*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ey + 0.3*Ex", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ey + 0.3*Ex", 1, "Ey", 1)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ey + 0.3*Ex", 1, "Ex", 0.3)

ret = SapModel.RespCombo.Add("0.9*Dead - 1.0*Ey + 0.3*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ey + 0.3*Ex", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ey + 0.3*Ex", 1, "Ey", -1)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ey + 0.3*Ex", 1, "Ex", 0.3)

ret = SapModel.RespCombo.Add("0.9*Dead - 1.0*Ey - 0.3*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ey - 0.3*Ex", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ey - 0.3*Ex", 1, "Ey", -1)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead - 1.0*Ey - 0.3*Ex", 1, "Ex", -0.3)

ret = SapModel.RespCombo.Add("0.9*Dead + 1.0*Ey - 0.3*Ex", 0)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ey - 0.3*Ex", 1, "DeadTotal", 0.9)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ey - 0.3*Ex", 1, "Ey", 1)
ret = SapModel.RespCombo.SetCaseList("0.9*Dead + 1.0*Ey - 0.3*Ex", 1, "Ex", -0.3)

# Combo 8 envolvente total -----------------------------------------------------------------------------

ret = SapModel.RespCombo.Add("EnvolventeT", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "DeadTotal", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.4*Dead", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Live+0.5*Rooflive", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Live+0.5*Granizo", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Live+0.5*Le", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Rooflive+1.0*Live", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Rooflive+0.8*Wind +x", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Rooflive+0.8*Wind -x", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Rooflive+0.8*Wind +y", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Rooflive+0.8*Wind -y", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Granizo+1.0*Live", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Granizo+0.8*Wind +x", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Granizo+0.8*Wind -x", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Granizo+0.8*Wind +y", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Granizo+0.8*Wind -y", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Le+1.0*Live", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Le+0.8*Wind +x", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Le+0.8*Wind -x", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Le+0.8*Wind +y", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Le+0.8*Wind -y", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Rooflive", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Rooflive", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Rooflive", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Rooflive", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Granizo", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Granizo", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Granizo", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Granizo", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind +x +1.0*Live +0.5*Le", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind -x +1.0*Live +0.5*Le", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind +y +1.0*Live +0.5*Le", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead+1.6*Wind -y +1.0*Live +0.5*Le", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live + 1.0*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live - 1.0*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live + 1.0*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live - 1.0*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live + 1.0*Ex + 0.3*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live + 1.0*Ex -0.3*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live -1.0*Ex -0.3*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live - 1.0*Ex + 0.3*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live + 1.0*Ey + 0.3*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live + 1.0*Ey -0.3*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live -1.0*Ey -0.3*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "1.2*Dead + 1*Live - 1.0*Ey + 0.3*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead + 1.6*Wind +x", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead + 1.6*Wind -x", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead + 1.6*Wind +y", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead + 1.6*Wind -y", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead + 1.0*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead - 1.0*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead + 1.0*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead - 1.0*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead + 1.0*Ex + 0.3*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead - 1.0*Ex + 0.3*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead - 1.0*Ex - 0.3*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead + 1.0*Ex - 0.3*Ey", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead + 1.0*Ey + 0.3*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead - 1.0*Ey + 0.3*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead - 1.0*Ey - 0.3*Ex", 1)
ret = SapModel.RespCombo.SetCaseList("EnvolventeT", 1, "0.9*Dead + 1.0*Ey - 0.3*Ex", 1)


