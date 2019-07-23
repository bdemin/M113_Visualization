from vtk import vtkSTLReader, vtkPolyDataMapper, vtkActor, vtkSphereSource


def get_stl_actor(filename):
    reader = vtkSTLReader()
    reader.SetFileName(filename)
    
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    
    actor = vtkActor()
    actor.SetMapper(mapper)
    
    return actor


def set_actor_visuals(actor, _type):
    Chassis = {'color':(0.244, 0.275, 0.075), 'ambi':0.1, 'ambic':(0.3,0.3,0.3), 'diff':0.9, 'diffc':(0.396, 0.263, 0.129), 'spec':0.6, 'specp':10}
    Road_Wheel = {'color':(0.194, 0.225, 0.025), 'ambi':0.4, 'ambic':(1,1,1), 'diff':0.3, 'diffc':(0.396, 0.263, 0.129), 'spec':0, 'specp':0}
    Sprocket = {'color':(0.194, 0.225, 0.025), 'ambi':0.3, 'ambic':(0,0,0), 'diff':0.3, 'diffc':(0.396, 0.263, 0.129), 'spec':0, 'specp':0}
    Idler = {'color':(0.194, 0.225, 0.025), 'ambi':0.3, 'ambic':(0,0,0), 'diff':0.3, 'diffc':(0.396, 0.263, 0.129), 'spec':0, 'specp':0}
    Track_Unit = {'color':(0.35,0.35,0.35), 'ambi':0.3, 'ambic':(0,0,0), 'diff':0.3, 'diffc':(0.396, 0.263, 0.129), 'spec':0, 'specp':0}
    Trailing_Arm = {'color':(0.35,0.35,0.35), 'ambi':0.3, 'ambic':(0,0,0), 'diff':0.3, 'diffc':(0.396, 0.263, 0.129), 'spec':0, 'specp':0}
    _type = vars()[_type]
    
    actor.GetProperty().SetColor(_type['color'])
    actor.GetProperty().SetAmbient(_type['ambi'])
#    actor.GetProperty().SetAmbientColor(_type['ambic'])
    actor.GetProperty().SetDiffuse(_type['diff'])
#    actor.GetProperty().ShadingOff()
#    actor.GetProperty().LightingOff()
#    actor.GetProperty().SetDiffuseColor(_type['diffc'])
    actor.GetProperty().SetSpecular(_type['spec'])
    actor.GetProperty().SetSpecularPower(_type['specp'])
    