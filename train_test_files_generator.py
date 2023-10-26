import os
import zipfile
import shutil as pysh


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
    pysh.unpack_archive(r'upload\to-serialize\raw-images.zip',
                        r'upload\dataset', 'zip')

    print('- Sucessfully unziped.')


def train_test_file_split(dataset_path=r'upload\dataset'):
    dataset = os.listdir(dataset_path)

    if len(dataset) == 0:
        print('- Dataset directory is empty!')
    else:
        jpg_files = []
        files_path = []

        # Capturing the files:
        for i in range(len(dataset)):
            if (dataset[i][-3:] == 'jpg'):
                # print(arquivos_txt[i]);
                jpg_files.append(f'{dataset[i][:-3]}jpg')

        # for j in range(len(jpg_files)):
        #     print(jpg_files[j]);

        for k in range(len(jpg_files)):
            files_path.append(f'{dataset_path}' + '/' + f'{jpg_files[k]}')
            # print(arquivos_path[k]);

        # Splitting:
        limite_teste = int(len(files_path) * .2)

        print('\n- Test files:')
        for l in range(limite_teste):
            print(files_path[l])

            # Writing test.txt:
            with open('upload/to-serialize/test.txt', 'a') as arquivo:
                arquivo.write(f'{files_path[l]}\n')

        m = limite_teste

        print('\n\n- Train files:')
        while m < len(files_path):
            print(files_path[m])

            # Writing train.txt:
            with open('upload/to-serialize/train.txt', 'a') as arquivo:
                arquivo.write(f'{files_path[m]}\n')

            m += 1


def zip_final_files():
    # Specify the names of the files you want to zip
    test_file = 'upload/to-serialize/test.txt'
    train_file = 'upload/to-serialize/train.txt'

    # Create a zip file (you can change the name as desired)
    zip_filename = 'upload/to-serialize/serialized-train-test-files.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Add the files to the zip file
        zipf.write(test_file, arcname='test.txt')
        zipf.write(train_file, arcname='train.txt')

    print(f'{zip_filename} has been created.')
