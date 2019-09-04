from vtk import vtkWindowToImageFilter, vtkAVIWriter, vtkPNGWriter


def get_video(renWin, rate, filename):
    _filter = vtkWindowToImageFilter()
    _filter.SetInput(renWin)
    _filter.SetInputBufferTypeToRGB()
    
    writer = vtkAVIWriter()
    writer.SetRate(int(rate))
    writer.SetQuality(2)
    writer.SetCompressorFourCC('DIB')
    writer.SetInputConnection(_filter.GetOutputPort())
    writer.SetFileName(filename + '.avi')
    writer.Start()
    return _filter, writer


def get_snapshots(renWin, _dir, frame):
    _filter = vtkWindowToImageFilter()
    _filter.SetInput(renWin)
    _filter.SetInputBufferTypeToRGB()
    
    writer = vtkPNGWriter()

    writer.SetInputConnection(_filter.GetOutputPort())
    writer.SetFileName(_dir + 'snap' + str(frame) + '.png')
#    writer.Start()
    return _filter, writer

def snap(writer, _dir, frame):
    writer.SetFileName(_dir + 'snap' + str(frame) + '.png')

def image_writer(renWin, _dir):
    _filter = vtkWindowToImageFilter()
    _filter.SetInput(renWin)
    _filter.SetInputBufferTypeToRGB()