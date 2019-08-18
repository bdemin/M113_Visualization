import numpy as np

from vtk import vtkLookupTable, vtkUnsignedCharArray, vtkNamedColors


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
        0: colors.HTMLColorToRGB('DarkKhaki'),
        1: colors.HTMLColorToRGB('Wheat'),
        2: colors.HTMLColorToRGB('BurlyWood'),
        3: colors.HTMLColorToRGB('SandyBrown'),
        4: colors.HTMLColorToRGB('Khaki'),
        5: colors.HTMLColorToRGB('DarkOliveGreen'),
        6: colors.HTMLColorToRGB('DarkGreen')}

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
    
    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3
    
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


def perlin2D(m):
    from scipy.interpolate import interp2d
    s = np.zeros((m,m)) # Prepare output image (size: m x m)
    w = m
    i = 0
    while w > 3:
        i = i + 1
        # d = interp2(randn([m,m]), i-1, 'spline')
        x = i
        y = i
        z = np.random.randn(m,m)
        d = interp2d(x,y,z, kind='spline')
        s = s + i * d[1:m, 1:m]
        w = w - np.ceil(w/2 - 1)

    s = (s - min(min(s[:,:]))) / (max(max(s[:,:])) - min(min(s[:,:])))

    return s


def create_soil_type_arr(size):
    # Create an array of different soil types scatterd randomly using Perlin Noise

    np.random.seed(1)
    noise = generate_perlin_noise_2d((size), (10, 10)) # Get perlin noise
    soil_type_arr = np.zeros(size)

    num_soil_types = 3 # Define how many soil types (colors) should be set
    arr_min = noise.min()
    soil_type_step = (noise.max() - arr_min)/num_soil_types
    # Fill array with different soil types
    for k in range(num_soil_types):
        for i in range(size[0]):
            for j in range(size[1]):
                if (noise[i,j] <= arr_min + (k+1)*soil_type_step) and (arr_min + k*soil_type_step <= noise[i,j]):
                    soil_type_arr[i,j] = k

    return soil_type_arr
