import math
import csv

#THIS IS USEFUL DO NOT DELETE
def getkeys(dictionary):
    return [*dictionary]

# allows to write dictionary(data) to file(file). If clear is 1 then the previous data is not carried over, if 0 then it only overwrites what is in dictionary(data)
def write_output(data, file, clear):
    keys = getkeys(data)
    adata = {}
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',]
    for letter in alphabet:
        for i in keys:
            if i[0] == letter:
                adata[i] = data[i]
    if clear == 1:
        with open(file, 'w') as f:
            for i in keys:
                text = i+' = '+ str(adata[i])+'\n'
                f.write(text)
    else:
        # this is totally reused shitty code, will it cause unnecisary slowdowns? YES! do I care? HELL NO
        split = []
        f = open(file,'a')
        f.close
        with open(file) as f:
            for line in f:
                # copy
                split = (line.split(' = '))
                # reformat
                split[1] = split[1].strip('\n')
                # insert
                #finding if the key in dictionary is ocupied
                try:
                    temp = adata[split[0]]
                except:
                    adata.update({split[0]: split[1]})
                else:
                    continue
                adata.update({split[0]: split[1]})
        with open(file, 'w') as f:
            for i in keys:
                text = i+' = '+str(adata[i])+'\n'
                f.write(text)
    return ()


# This function converts input csv file to a matrix (list of list)
# Input should be inserted to desending order (however asending should work but I am to lazy to verify that)
def graph_to_value(value, dataset,inverse):
    # Import Data points
    p = 0
    p2 = 0
    data = []
    n = 0
    with open(dataset, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
            # convert string to float
            data[n][0] = float(data[n][0])
            data[n][1] = float(data[n][1])
            if inverse == 1:
                data[n][0], data[n][1] = data[n][1], data[n][0]
            n += 1
        # close file
        if inverse == 1 and data[0][0] < data[1][0]:
            data.reverse()

    # find closest datapoint
    for i in range(len(data)):
        if i > 1:
            if value > data[0][0]:
                print("error, X-Axis Too High")
                break
            if abs(data[i][0] - value) > abs(data[i-1][0] - value):
                p = i - 1
                break

    # find second closest datapoint
    if value > data[p][0]:
        p2 = p - 1
    else:
        p2 = p + 1
    # print(data[p][0], ' - ', value, ' - ', data[p2][0])
    # calculate the line between points y=mx+b
    # m=(y2-y1)/(x2-x1)
    m = (data[p2][1] - data[p][1]) / (data[p2][0] - data[p][0])
    # b=y-m*x
    b = data[p][1] - (m * data[p][0])
    # plug in x
    return(m * value + b)

def print_output(file):
    with open(file) as f:
        for line in f:
            try:
                print(line)
            except:
                continue
    return()