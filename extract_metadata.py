# Libraries imports:
import shutil as pysh
import pandas as pypd
import simplekml
import math
import PIL
import os

from exif import Image
from PIL.ExifTags import TAGS

print('- All libraries were imported.')


def create_dataset_folder():
    # Directory measurement variable:
    dataset_existente = os.path.exists(r'upload\dataset')

    # Creation of the 'dataset' directory, if it does not exist:
    if not dataset_existente:
        os.makedirs(r'upload\dataset')
        print('- Dataset folder created. Populate it with images!')
    else:
        # Dataset directory benchmarking:
        dataset_diretorio = os.listdir(r'upload\dataset')

        if len(dataset_diretorio) == 0:
            print(
                '- Dataset folder already exists, necessary to populate the dataset directory with images.')
        else:
            print('- Dataset folder already exists.')


def unzip():
    # Parameters: .zip path, where to send it and format:
    pysh.unpack_archive(r'upload\metadata\raw-images.zip',
                        r'upload\dataset', 'zip')

    print('- Sucessfully unziped.')


def read_images():
    # Reading each image [in array format] manually:
    dataset_directory = r'upload\dataset'
    dataset_array = []

    dataset = os.listdir(dataset_directory)

    for aux in range(len(dataset)):
        # Captures only files with .jpg or .png extensions and increments them in the dataset_array list:
        if (dataset[aux].split('.')[1] == 'JPG' or dataset[aux].split('.')[1] == 'jpg' or dataset[aux].split('.')[1] == 'PNG' or dataset[aux].split('.')[1] == 'png'):
            dataset_array.append(dataset[aux])

    print('- Dataset list created.')

    # Checking the amount of images obtained:
    print(f'- {len(dataset_array)} images were read.')

    return dataset_array


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1]/60 + coords[2]/3600

    if ref == 'S' or ref == 'W':
        decimal_degrees = -decimal_degrees

    return decimal_degrees


def coordinates():
    # Aux variables:
    image_time = []
    image_date = []
    image_latitude = []
    image_longitude = []
    image_altitude = []
    image_latitude_reference = []
    image_longitude_reference = []
    image_pixel_dimensions = []
    image_real_dimensions = []
    image_area = []
    path_to_image = []

    def image_coordinates(image_path):
        # Reading image file:
        with open(image_path, 'rb') as source:
            image = Image(source)

        if image.has_exif:
            try:
                image.gps_longitude
                coords = (decimal_coords(image.gps_latitude, image.gps_latitude_ref), decimal_coords(
                    image.gps_longitude, image.gps_longitude_ref))

                altitude = image.gps_altitude - 1172
                horizontal_field_of_view = 87
                vertical_field_of_view = 50

                # Convert degrees to radians:
                horizontal_field_of_view = math.radians(
                    horizontal_field_of_view)
                vertical_field_of_view = math.radians(vertical_field_of_view)

                # Calculate footprint width and height:
                footprint_width = round(
                    2 * altitude * math.tan(horizontal_field_of_view / 2), 2)
                footprint_height = round(
                    2 * altitude * math.tan(vertical_field_of_view / 2), 2)

                # Appending info:
                image_time.append(image.datetime_original[11:19])
                image_date.append(image.datetime_original[:10])
                image_latitude.append(coords[0])
                image_longitude.append(coords[1])
                image_altitude.append(
                    f'{round(image.gps_altitude - 1172, 2)} m')
                image_latitude_reference.append(image.gps_latitude_ref)
                image_longitude_reference.append(image.gps_longitude_ref)
                image_pixel_dimensions.append(
                    f'{image.pixel_x_dimension} x {image.pixel_y_dimension} pixels')
                image_real_dimensions.append(
                    f'{footprint_width} x {footprint_height} m')
                image_area.append(
                    f'{round(footprint_width*footprint_height, 2)} m²')
                path_to_image.append(image_path.split('\\')[-1])

            except AttributeError:
                print('- No coordinates')
        else:
            print(f'- {image_path} has no EXIF information.')

        print(
            f"- {image_path} was taken at {image.datetime_original[11:19]} on {image.datetime_original[:10]}, and has latitude: {coords[0]} and longitude {coords[1]}")

    dataset_array = read_images()

    for aux in range(len(dataset_array)):
        path = f'upload\\dataset\\{dataset_array[aux]}'

        if aux < 9:
            print(f'00{aux + 1} ', end='')
        elif aux < 99:
            print(f'0{aux + 1} ', end='')
        else:
            print(f'{aux + 1} ', end='')

        image_coordinates(path)

    # Calling dataframe constructor after zipping:
    images_info_dataframe = pypd.DataFrame(list(zip(path_to_image, image_time, image_date, image_latitude, image_longitude, image_altitude, image_latitude_reference, image_longitude_reference, image_pixel_dimensions, image_real_dimensions, image_area)), columns=[
                                           'Image', 'Time', 'Date', 'Latitude', 'Longitude', 'Altitude', 'Latitude Reference', 'Longitude Reference', 'Image Pixel Dimensions', 'Image Real Dimensions', 'Image Area'])
    images_info_dataframe.to_excel(r'upload\metadata\images-metadata.xlsx')

    # Create a KML object
    kml = simplekml.Kml()

    # Iterate through the DataFrame and create KML placemarks
    for index, row in images_info_dataframe.iterrows():
        if 'Latitude' in row and 'Longitude' in row:
            lat = row['Latitude']
            lon = row['Longitude']
            placemark = kml.newpoint(name=row['Image'], coords=[(lon, lat)])
            placemark.description = row.get('description', '')

    # Save the KML file
    kml.save(r'upload\metadata\images-metadata.kml')

    data = []

    for row in range(0, len(images_info_dataframe)):
        data.append((path_to_image[row], image_time[row], image_date[row], image_latitude[row], image_longitude[row], image_altitude[row],
                    image_latitude_reference[row], image_longitude_reference[row], image_pixel_dimensions[row], image_real_dimensions[row], image_area[row]))

    return data
