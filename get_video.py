import vtk


def get_video(renWin, rate, filename):
    _filter = vtk.vtkWindowToImageFilter()
    _filter.SetInput(renWin)
    _filter.SetInputBufferTypeToRGB()
    
    writer = vtk.vtkAVIWriter()
    writer.SetRate(int(rate))
    writer.SetQuality(2)
    writer.SetCompressorFourCC('DIB')
    writer.SetInputConnection(_filter.GetOutputPort())
    writer.SetFileName(filename + '.avi')
    writer.Start()
    return _filter, writer


def get_snapshots(renWin, _dir, frame):
    _filter = vtk.vtkWindowToImageFilter()
    _filter.SetInput(renWin)
    _filter.SetInputBufferTypeToRGB()
    
    writer = vtk.vtkPNGWriter()

    writer.SetInputConnection(_filter.GetOutputPort())
    writer.SetFileName(_dir + 'snap' + str(frame) + '.png')
#    writer.Start()
    return _filter, writer

def snap(writer, _dir, frame):
    writer.SetFileName(_dir + 'snap' + str(frame) + '.png')

def image_writer(renWin, _dir):
    _filter = vtk.vtkWindowToImageFilter()
    _filter.SetInput(renWin)
    _filter.SetInputBufferTypeToRGB()