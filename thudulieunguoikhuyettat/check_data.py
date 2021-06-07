import json
import argparse
import os
import time

import xlwt
from xlwt import Workbook

def write_exel(file_name, content, folder):
    wb = Workbook()
    font = xlwt.Font()  # Create the Font
    font.name = 'Times New Roman'
    font.height = 320
    style = xlwt.XFStyle()  # Create the Style
    style.font = font
    style.alignment.wrap = 0
    sheet1 = wb.add_sheet('Sheet 1', style)
    sheet1.write(0, 0, "STT", style)
    sheet1.write(0, 1, "ID", style)
    sheet1.write(0, 2, "Nội dung", style)
    sheet1.write(0, 3, " Tên file: <ID>.wav hoặc <ID>.mp3 ( ví dụ: 1609.wav) - số kênh: 1/mono - bitrate: 256 kbps - sample rate: 16000Hz", style)
    for i in range(0,len(content)):
        sheet1.write(i+1, 0, str(i+1), style)
        sheet1.write(i+1, 1, content[i][0], style)
        sheet1.write(i+1, 2, content[i][1], style)
    wb.save('thudulieunguoikhuyettat/transcript_congty/'+str(folder)+"/"+file_name+'.xls')
def get_all_sentences(transcript_path):
    # dict_sentences = {}
    f_write = open("thudulieunguoikhuyettat/text.txt", "w+", encoding='UTF-8')
    i = 1
    id = 1
    count_files = 1
    folder = 0
    content = []
    start = time.time()
    with open(transcript_path, "r") as f:
        # lines = f.readlines()
        for line in f:
            # row = json.loads(line)
            temp = "".join(line.rstrip().split(" "))
            # temp = line.rstrip()
            if temp.isalpha() and 60<len(line)<80:
                # dict_sentences[id] = row['transcript']
                f_write.write("B_"+str(id)+"\t"+line.rstrip()+"\n")
                content.append(
                        ["B_"+str(id), str(line.rstrip())])
                id = id + 1
                if i%100==0:
                    if count_files % 10 == 1:
                        folder = folder + 1
                        os.makedirs(
                            "thudulieunguoikhuyettat/transcript_congty/" + str(folder), exist_ok=True)
                    write_exel("A"+str(count_files), content, folder)
                    count_files = count_files + 1
                    content = []
                i = i + 1
            else:
                continue
            if id%1000000==0:
                end = time.time()
                print("processed from {} to {} take {:.2f}".format(id-1000000, id, end-start))
                start = time.time()
                # dict_sentences[row['id']] = row['script']
                # id.append(int(row['id']))
    # print(result)

    f_write.close()
    # return dict_sentences


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--transcript', '-f', action='store', type=str, required=True)
    args = my_parser.parse_args()
    transcript = args.transcript
    get_all_sentences(transcript)
    # print(len(dict_sentences))
