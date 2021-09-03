from genericpath import exists
import os 
import heapq as heap
import fnmatch


rootDir = os.getcwd()
dirName = os.path.join(rootDir,'lab1/input')
merge_values= []

        

def mergeSort(arr):
    arr = [int(val) for val in arr] #convert value to int
    if len(arr) <= 1: 
        return arr
    else:
        mid = len(arr)//2
        firstHalf = mergeSort(arr[:mid]) #first half of array
        secondhalf = mergeSort(arr[mid:]) #second half of array
        return merge(firstHalf,secondhalf)

def merge(firstHalf = [],secondHalf= []):
    newArr = []
    
    while len(firstHalf) != 0 and len(secondHalf) != 0:
        if firstHalf[0] < secondHalf[0]:
            newArr.append(firstHalf[0])
            firstHalf.remove(firstHalf[0])
        else:
            newArr.append(secondHalf[0])
            secondHalf.remove(secondHalf[0])
    if len(firstHalf) == 0:
        newArr += secondHalf
    else:
        newArr +=firstHalf
    return newArr

    

def main():
    for filename in os.listdir(dirName):
        if fnmatch.fnmatch(filename, '*.txt'):
            with open(os.path.join(dirName,filename)) as file:
                values = file.read().split()
                sorted =  mergeSort(values) 
                merge_values.append(sorted)
    print(len(merge_values))
    heaped = list(heap.merge(*merge_values)) #arrange in ascending
    outputDir = os.path.join(rootDir,'lab1/output')
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    outputFile = outputDir + "/sorted.txt" #export to sorted
    with open(outputFile, 'w') as f:
        for item in heaped:
            f.write("%s\n" % item)
    file.close()

main()