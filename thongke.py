import os
import librosa


def get_all_info():
    folders = os.listdir("static/audios")
    files_name, files_path, durations_all = [], [], []
    for folder in folders:
        # print(file)
        files = os.listdir("static/audios/" + folder)
        for file in files:
            file_path = os.path.join(os.path.join("static/audios", folder),
                                     file)
            duration = librosa.get_duration(filename=file_path)
            files_name.append(".".join(file.split(".")[:-1]))
            files_path.append(file_path)
            durations_all.append(duration)
    # print(files_name)
    names, duration_each_user, number_files, files_path_each_user, ids_each_user = [], [], [], [], []
    for i in range(0, len(files_name)):
        name = "_".join(files_name[i].split("_")[:-1])
        id = int(files_name[i].split("_")[-1])
        if name not in names:
            names.append(name)
            duration_each_user.append(durations_all[i])
            number_files.append(1)
            files_path_each_user.append([files_path[i]])
            ids_each_user.append([id])
            # print(files_path_each_user)
        else:
            index = names.index(name)
            duration_each_user[index] = duration_each_user[index] + \
                                        durations_all[i]
            number_files[index] = number_files[index] + 1
            # print(files_path_each_user[index].append(files_path[i]))
            # print(files_path_each_user[index])
            files_path_each_user[index].append(files_path[i])
            ids_each_user[index].append(id)
    # print(names)
    # print(duration_each_user)
    # print(number_files)
    # print(files_path_each_user)
    for i in range(0, len(duration_each_user)):
        duration_each_user[i] = round(duration_each_user[i],3)
    names, duration_each_user, number_files, files_path_each_user, ids_each_user = zip(
        *sorted(
                zip(names, duration_each_user, number_files,
                    files_path_each_user, ids_each_user)))
    return names, number_files, duration_each_user, files_path_each_user, ids_each_user


if __name__ == '__main__':
    get_all_info()
