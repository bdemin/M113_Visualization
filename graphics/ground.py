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

    # Generate the colors for each point based on the color map
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
    PolyData.GetPointData().SetScalars(colors)



def get_soil_color(soil_type_key, colors_dict):
    # Function that returns the defined color for a specific soil type
    if soil_type_key in colors_dict:
        return colors_dict[soil_type_key]
    return (255,255,255) # If undefined, return white color


def visualize_soil(PolyData, soil_type_array):
    # Assign colors to the ground based on input soil type array
    colors = vtkNamedColors()
    colors_dict = {
        0: colors.HTMLColorToRGB('SandyBrown'),
        1: colors.HTMLColorToRGB('ForestGreen'),
        2: colors.HTMLColorToRGB('Sienna'),
        3: colors.HTMLColorToRGB('DarkOliveGreen'),
        4: colors.HTMLColorToRGB('BurlyWood'),
        5: colors.HTMLColorToRGB('RosyBrown'),
        6: colors.HTMLColorToRGB('DarkKhaki')}

    m, n = soil_type_array.shape
    soil_color_map = vtkUnsignedCharArray()
    soil_color_map.SetNumberOfComponents(3)
    soil_color_map.SetName("Colors")

    for i in range(m-1):
        for j in range(n-1):
            for _ in range(6):
                soil_type = soil_type_array[i,j]
                soil_color_map.InsertNextTypedTuple(get_soil_color(soil_type, colors_dict))

    PolyData.GetPointData().SetScalars(soil_color_map)


def create_soil_type_arr(size):
    noise = generate_perlin_noise_2d(size, (139, 3))
    for i in range(size[0]):
        for j in range(size[1]):
            if noise[i,j] < -0.2:
                noise[i,j] = 0
            elif noise[i,j] < 0.2:
                noise[i,j] = 1
            elif noise[i,j] < 0.4:
                noise[i,j] = 2
            elif noise[i,j] < 0.6:
                noise[i,j] = 3
            elif noise[i,j] < 0.7:
                noise[i,j] = 4
            elif noise[i,j] < 0.8:
                noise[i,j] = 5
            else:
                noise[i,j] = 6
    return noise
