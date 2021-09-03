import os
import heapq as heap
import asyncio
import fnmatch

rootDir = os.getcwd()
dirName = os.path.join(rootDir,'lab1/input')

values= []
merge_values= []

def mergeSort(arr):
        arr = [int(val) for val in arr]
        if len(arr) <= 1:
            return arr
        else:
            mid = len(arr)//2
            firstHalf = mergeSort(arr[:mid])
            secondhalf = mergeSort(arr[mid:])
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

async def addFileValues(filename):
    with open(os.path.join(dirName,filename)) as file:
                values = file.read().split()
                file.close()
    sorted =  mergeSort(values)
        #print((sorted))
    merge_values.append(sorted)


async def main():
    tasks = []
    for filename in os.listdir(dirName):
        if fnmatch.fnmatch(filename, '*.txt'):
            task = addFileValues(filename)
            tasks.append(task)
    await asyncio.gather(*tasks)
    print(len(merge_values))
    heaped = list(heap.merge(*merge_values))
    outputDir = os.path.join(rootDir,'lab1/output')
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    outputFile = outputDir + "/async_sorted.txt"
    with open(outputFile, 'w') as f:
        for item in heaped:
            f.write("%s\n" % item)
    f.close()



if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())