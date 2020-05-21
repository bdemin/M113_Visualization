# profile = vtk.vtkPolyData()
# profile.SetPoints(points)

# Delaunay3D is used to triangulate the points. The Tolerance is the
# distance that nearly coincident points are merged
# together. (Delaunay does better if points are well spaced.) The
# alpha value is the radius of circumcircles, circumspheres. Any mesh
# entity whose circumcircle is smaller than this value is output.
# from vtk import vtkDelaunay3D
# delny = vtkDelaunay3D()
# delny.SetInputData(profile)
# delny.SetTolerance(0.01)
# delny.SetAlpha(0.2)
# delny.BoundingTriangulationOff()

# Shrink the result to help see it better.
# shrink = vtk.vtkShrinkFilter()
# shrink.SetInputConnection(delny.GetOutputPort())
# shrink.SetShrinkFactor(0.9)

# map = vtk.vtkDataSetMapper()
# map.SetInputConnection(shrink.GetOutputPort())

# triangulation = vtk.vtkActor()
# triangulation.SetMapper(map)
# triangulation.GetProperty().SetColor(1, 0, 0)

# ren.AddActor(triangulation)
