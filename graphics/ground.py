import numpy as np

from vtk import vtkLookupTable, vtkUnsignedCharArray, vtkNamedColors, \
    vtkCellLocator, vtkPoints, mutable, vtkParametricSpline, vtkParametricFunctionSource, \
        vtkPolyDataMapper, vtkActor


def visualize_elevation(PolyData):
    # Create colormap
    bounds = 6*[0.0]
    PolyData.GetBounds(bounds)

    # Find min and max z
    minz = bounds[4]
    maxz = bounds[5]

    colorLookupTable = vtkLookupTable()
    colorLookupTable.SetTableRange(minz, maxz)
    colorLookupTable.Build()

    # Generate the colors for each point based on elevation
    colors = vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")
    for i in range(0, PolyData.GetNumberOfPoints()):
        p= 3*[0.0]
        PolyData.GetPoint(i,p)

        dcolor = 3*[0.0]
        colorLookupTable.GetColor(p[2], dcolor)

        color=3*[0.0]
        for j in range(0,3):
            color[j] = int(255.0 * dcolor[j])

        colors.InsertNextTypedTuple(color)

    # Assign colors to the vtkPolyData
    PolyData.GetPointData().SetScalars(colors)



def get_soil_color(soil_type_key, colors_dict):
    # Function that returns the defined color for a specific soil type
    if soil_type_key in colors_dict:
        return colors_dict[soil_type_key]
    return (255,255,255) # If undefined, return white color


def visualize_soil(PolyData, soil_type_array):
    # Assign colors to the ground based on input soil type array

    # Create a color dictionary
    colors = vtkNamedColors()
    colors_dict = {
        3: colors.HTMLColorToRGB('DarkKhaki'),
        0: colors.HTMLColorToRGB('Wheat'),
        4: colors.HTMLColorToRGB('BurlyWood'),
        6: colors.HTMLColorToRGB('SandyBrown'),
        2: colors.HTMLColorToRGB('Khaki'),
        5: colors.HTMLColorToRGB('DarkOliveGreen'),
        1: colors.HTMLColorToRGB('tan')}

    m, n = soil_type_array.shape
    soil_color_map = vtkUnsignedCharArray()
    soil_color_map.SetNumberOfComponents(3)
    soil_color_map.SetName("Colors")

    for i in range(m-1):
        for j in range(n-1):
            for _ in range(6):
                soil_color_map.InsertNextTypedTuple(get_soil_color(soil_type_array[i,j], colors_dict))

    # Assign colors to the vtkPolyData
    PolyData.GetPointData().SetScalars(soil_color_map)


def generate_perlin_noise_2d(size, res):
    # Return Perlin Noise

    def factors(n):
        from functools import reduce
        return list(reduce(list.__add__,
                    ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3
    
    m_factors = sorted(factors(size[0]))
    n_factors = sorted(factors(size[1]))
    m_mid_index = (len(m_factors) - 1) // 2
    n_mid_index = (len(n_factors) - 1) // 2
    res = (m_factors[m_mid_index], n_factors[n_mid_index])

    delta = (res[0] / size[0], res[1] / size[1])
    d = (size[0] // res[0], size[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0],0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2*np.pi*np.random.rand(res[0]+1, res[1]+1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:  ,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1,1:  ].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:  ,1:  ].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(np.dstack((grid[:,:,0]  , grid[:,:,1]  )) * g00, 2)
    n10 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]  )) * g10, 2)
    n01 = np.sum(np.dstack((grid[:,:,0]  , grid[:,:,1]-1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
    n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
    return np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)


# def perlin2D(m):
#     from scipy.interpolate import interp2d
#     s = np.zeros((m,m)) # Prepare output image (size: m x m)
#     w = m
#     i = 0
#     while w > 3:
#         i = i + 1
#         # d = interp2(randn([m,m]), i-1, 'spline')
#         x = i
#         y = i
#         z = np.random.randn(m,m)
#         d = interp2d(x,y,z, kind='spline')
#         s = s + i * d[1:m, 1:m]
#         w = w - np.ceil(w/2 - 1)

#     s = (s - min(min(s[:,:]))) / (max(max(s[:,:])) - min(min(s[:,:])))

#     return s


def create_soil_type_arr(size):
    # Create an array of different soil types scatterd randomly using Perlin Noise

    np.random.seed(1)
    noise = generate_perlin_noise_2d((size), (5, 5)) # Get perlin noise
    soil_type_arr = np.zeros(size)

    num_soil_types = 2 # Define how many soil types (colors) should be set
    arr_min = noise.min()
    soil_type_step = (noise.max() - arr_min)/num_soil_types
    
    # Fill array with different soil types
    for k in range(num_soil_types):
        for i in range(size[0]):
            for j in range(size[1]):
                if (noise[i,j] <= arr_min + (k+1)*soil_type_step) and (arr_min + k*soil_type_step <= noise[i,j]):
                    soil_type_arr[i,j] = k

    return soil_type_arr

def get_spline_actor(surface_data, chassis_cg_path, surface_bounds):
    # Iterate over chassis CG points and create a spline which marks the driving path.
    # Return the spline as a vtkActor for being added later to the renderer.

    # Update the pipeline so that vtkCellLocator finds cells
    surface_data.Update()

    # Define a cellLocator to be able to compute intersections between lines
    # and the surface
    locator = vtkCellLocator()
    locator.SetDataSet(surface_data.GetOutput())
    locator.BuildLocator()

    tolerance = 0.01 # Set intersection searching tolerance

    # Make a list of points. Each point is the intersection of a vertical line
    # defined by p1 and p2 and the surface.
    points = vtkPoints()
    for chassis_cg in chassis_cg_path:
        # p1 = [chassis_cg[0], chassis_cg[1], surface_bounds[4]]
        p1 = [chassis_cg[0], chassis_cg[1], -1]
        # p2 = [chassis_cg[0], chassis_cg[1], surface_bounds[5]]
        p2 = [chassis_cg[0], chassis_cg[1], 1]

        t = mutable(0)
        pos = [0.0, 0.0, 0.0]
        pcoords = [0.0, 0.0, 0.0]
        subId = mutable(0)
        locator.IntersectWithLine(p1, p2, tolerance, t, pos, pcoords, subId)

        # Add a slight offset in z
        pos[2] += 0.05
        
        # Add the x, y, z position of the intersection
        points.InsertNextPoint(pos)

    # Create a spline and add the pointsoi
    spline = vtkParametricSpline()
    spline.SetPoints(points)
    spline_function = vtkParametricFunctionSource()
    spline_function.SetUResolution(len(chassis_cg_path))
    spline_function.SetParametricFunction(spline)

    # Map the spline
    spline_mapper = vtkPolyDataMapper()
    spline_mapper.SetInputConnection(spline_function.GetOutputPort())

    # Define the line actor
    spline_actor = vtkActor()
    spline_actor.SetMapper(spline_mapper)
    spline_actor.GetProperty().SetColor([0,0.7,0])
    spline_actor.GetProperty().SetLineWidth(10)
    
    return spline_actor
