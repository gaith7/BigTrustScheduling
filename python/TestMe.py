import csv
import pprint
import threading
import time
from multiprocessing import Process


DEBUG = False


class TasksScheduler:
    def __init__(self):
        self.trustFile = 'vms.csv'
        self.vmsFile = '1_exported.csv'
        self.t = []

    def __readTrustFileInfo(self):
        titles = []
        tasks = []
        with open(self.trustFile, 'rU') as csvFile:
            csvReader = csv.reader(csvFile)
            for task in csvReader:
                if not task[1].replace('.', '', 1).isdigit():
                    titles = task[1:]
                    if DEBUG:
                        print ('task titles: ', titles)
                else:
                    tasks.append(task[1:])
                    if DEBUG:
                        print ('tasks: ', tasks)

        #  FIXME: add a Trust title as the first one to fix the vms table first row left shift
        titles.insert(0, 'Trust')

        return titles, tasks

    def __readTasksFile(self):
        titles = []
        tasks = []
        with open(self.vmsFile, 'rU') as csvFile:
            csvReader = csv.reader(csvFile)
            for task in csvReader:
                if not task[1].replace('.', '', 1).isdigit():
                    titles = filter(None, task)
                    tmp = []
                    for title in titles:
                        tmp.append(' '.join(title.split()))
                    titles = tmp
                    if DEBUG:
                        print ('vm titles: ', titles)
                else:
                    task = list(filter(None, task))
                    tasks.append(task)
                    if DEBUG:
                        print ('vm specs: ', tasks)

        if DEBUG:
            for task in tasks:
                print (task)

        return titles, tasks

    def convertTrustFileToListOfDicts(self):
        vmsList = []
        titles, tasks = self.__readTrustFileInfo()

        for task in tasks:
            dict = {}
            for index, item in enumerate(task):
                dict[titles[index]] = item
            vmsList.append(dict)

        # Sort list of dictionaries by Trust value
        vmsList = sorted(vmsList, key=lambda k: k['Trust'], reverse=True)

        if DEBUG:
            print ('vms list before processing\n')
            for vm in vmsList:
                print ('vm: ', vm)

        return vmsList

    def convertVmsFileToListOfDicts(self):
        tasks = []
        titles, tasksItem = self.__readTasksFile()

        for taskItem in tasksItem:
            dict = {}
            for index, item in enumerate(taskItem):
                if len(item) > 0:
                    dict[titles[index]] = item
            tasks.append(dict)

        tmpTask = {}
        tmpTasks = []

        for task in tasks:
            tmpTask['CPU cores'] = int(task.get('CPU cores'))
            # TODO: Convert me to GHZ
            tmpTask['CPU capacity provisioned [MHZ]'] = float(task.get('CPU capacity provisioned [MHZ]'))
            tmpTask['CPU usage [GHZ]'] = float(task.get('CPU usage [MHZ]')) / 1000
            tmpTask['CPU usage [%]'] = float(task.get('CPU usage [%]'))
            tmpTask['Memory capacity provisioned [KB]'] = float(task.get('Memory capacity provisioned [KB]'))
            tmpTask['Memory usage [GB]'] = float(task.get('Memory usage [KB]')) / 1000000
            tmpTask['Disk read throughput [KB/s]'] = float(task.get('Disk read throughput [KB/s]'))
            tmpTask['Disk write throughput [GB/s]'] = float(task.get('Disk write throughput [KB/s]')) / 1000000
            tmpTask['Network received throughput [KB/s]'] = float(task.get('Network received throughput [KB/s]'))
            tmpTask['Network transmitted throughput [MB/s]'] = float(task.get('Network transmitted throughput [KB/s]')) / 1000
            tmpTask['Timestamp [ms]'] = task.get('Timestamp [ms]')
            tmpTasks.append(tmpTask)
            tmpTask = {}

        tasks = tmpTasks

        if DEBUG:
            for task in tasks:
                print ('task: ', task)

        return tasks

    def computeExecutionTimeForGivenTasks(self, tasks):
        tmp = []
        for task in tasks:
            task['Processing Time/s'] = {}
            # we are going to ignore the tasks that their CPU usage [GHZ] value is equal to '0'
            if float(task['CPU usage [GHZ]']) > 0:
                estimatedProcessingTime = (1 / (float(task['CPU usage [GHZ]']) * 1000000000)) * 0.5 * 10000000
                task['Processing Time/s'] = estimatedProcessingTime
                tmp.append(task)

        tasks = tmp

        if DEBUG:
            for task in tasks:
                print (task)

        return tasks

    def __checkCpuUsage(self, task, vm):
        if vm['CPU-Ghz'] > task['CPU usage [GHZ]']:
            if DEBUG & True:
                print ('CPU ( vm:', vm['CPU-Ghz'], '> task:', task['CPU usage [GHZ]'], ')')
            return vm

        return False

    def __checkMemoryUsage(self, task, vm):
        if vm['RAM-Gb'] > task['Memory usage [GB]']:
            if DEBUG & True:
                print ('RAM ( vm:', vm['RAM-Gb'], '> task:', task['Memory usage [GB]'], ')')
            return vm

        return False

    def __checkNetworkTransmittedThroughput(self, task, vm):
        if vm['BW-Ms'] > task['Network transmitted throughput [MB/s]']:
            if DEBUG & True:
                print ('BW-Ms ( vm:', vm['BW-Ms'], '> task:', task['Network transmitted throughput [MB/s]'], ')')
            return vm

        return False

    def __checkDiskWriteThroughput(self, task, vm):
        if vm['DS-Gb'] > task['Disk write throughput [GB/s]']:
            if DEBUG & True:
                print ('DS-Gb ( vm:', vm['DS-Gb'], '> task:', task['Disk write throughput [GB/s]'], ')')
            return vm

        return False

    def __isMatch(self, task, vm):
        vmSelected1 = self.__checkCpuUsage(task, vm)
        vmSelected2 = self.__checkMemoryUsage(task, vm)
        vmSelected3 = self.__checkNetworkTransmittedThroughput(task, vm)
        vmSelected4 = self.__checkDiskWriteThroughput(task, vm)

        if vmSelected1 == vmSelected2 == vmSelected3 == vmSelected4:
            return vm

        return False

    def __updateSelectedVmResources(self, vmMatch, task):
        vmMatch['Trust'] = vmMatch['Trust']
        vmMatch['CPU-Ghz'] = float(vmMatch['CPU-Ghz']) - float(task['CPU usage [GHZ]'])
        vmMatch['RAM-Gb'] = float(vmMatch['RAM-Gb']) - float(task['Memory usage [GB]'])
        vmMatch['BW-Ms'] = vmMatch['BW-Ms']
        vmMatch['DS-Gb'] = vmMatch['DS-Gb']

        if 'tasksAssigned' not in vmMatch:
            vmMatch['tasksAssigned'] = []
            vmMatch['tasksAssigned'].append(task)
        else:
            vmMatch['tasksAssigned'].append(task)

        if DEBUG & True:
            print ('Updated Vm Match: ', vmMatch)
            print ('\n')

        return vmMatch

    def __updateVmsListWithSelectedVm(self, vms, vm, updatedMatchingVm):
        vms[vms.index(vm)] = updatedMatchingVm

        return vms

    def groupTasksInPairsAccordingToGreedyAlgorithmStrategy(self, tasks):
        tasks = sorted(tasks, key=lambda k: k['Processing Time/s'], reverse=False)
        if DEBUG:
            for task in tasks:
                print ('task: ', task['Processing Time/s'])

        obj = {
            '1st task': None,
            '2nd task': None,
            'total time': None
        }
        tasksPairs = []
        # TODO: handle lists with odd numbers.
        # TODO: processing a list of 9 items would result in ignoring one of the them. Mostly the one in the middle
        for i in range(len(tasks)//2):
            if DEBUG:
                print ('tasks in pairs:', tasks[i]['Processing Time/s'], '+', tasks[~i]['Processing Time/s'], \
                    '=', float(tasks[i]['Processing Time/s']) + float(tasks[~i]['Processing Time/s']))

            obj['1st task'] = tasks[i]
            obj['2nd task'] = tasks[~i]
            obj['total time'] = float(tasks[i]['Processing Time/s']) + float(tasks[~i]['Processing Time/s'])
            tasksPairs.append(obj)

            obj = {
                '1st task': None,
                '2nd task': None,
                'total time': None
            }

        tasksPairs = sorted(tasksPairs, key=lambda k: k['total time'], reverse=True)
        if DEBUG:
            for pair in tasksPairs:
                print ('pair item: ', pair)

        return tasksPairs

    def __checkPairCpuUsage(self, pair, vm):
        if vm['CPU-Ghz'] > pair['1st task']['CPU usage [GHZ]'] and vm['CPU-Ghz'] > pair['2nd task']['CPU usage [GHZ]']:
            if DEBUG & True:
                print ('CPU ( vm:', vm['CPU-Ghz'], '> task:', pair['1st task']['CPU usage [GHZ]'], ')')
                print ('CPU ( vm:', vm['CPU-Ghz'], '> task:', pair['2nd task']['CPU usage [GHZ]'], ')')
            return vm

        return False

    def __checkPairMemoryUsage(self, pair, vm):
        if vm['RAM-Gb'] > pair['1st task']['Memory usage [GB]'] and vm['RAM-Gb'] > pair['2nd task']['Memory usage [GB]']:
            if DEBUG & True:
                print ('RAM ( vm:', vm['RAM-Gb'], '> task:', pair['1st task']['Memory usage [GB]'], ')')
                print ('RAM ( vm:', vm['RAM-Gb'], '> task:', pair['2nd task']['Memory usage [GB]'], ')')
            return vm

        return False

    def __checkPairNetworkTransmittedThroughput(self, pair, vm):
        if vm['BW-Ms'] > pair['1st task']['Network transmitted throughput [MB/s]'] and \
                vm['BW-Ms'] > pair['2nd task']['Network transmitted throughput [MB/s]']:
            if DEBUG & True:
                print ('BW-Ms ( vm:', vm['BW-Ms'], '> task:', pair['1st task'][
                    'Network transmitted throughput [MB/s]'], ')')
                print ('BW-Ms ( vm:', vm['BW-Ms'], '> task:', pair['2nd task'][
                    'Network transmitted throughput [MB/s]'], ')')
            return vm

        return False

    def __checkPairDiskWriteThroughput(self, pair, vm):
        if vm['DS-Gb'] > pair['1st task']['Disk write throughput [GB/s]'] and \
                vm['DS-Gb'] > pair['2nd task']['Disk write throughput [GB/s]']:
            if DEBUG & True:
                print ('DS-Gb ( vm:', vm['DS-Gb'], '> task:', pair['1st task']['Disk write throughput [GB/s]'], ')')
                print ('DS-Gb ( vm:', vm['DS-Gb'], '> task:', pair['2nd task']['Disk write throughput [GB/s]'], ')')
            return vm

        return False

    def __isPairAMatch(self, pair, vm):
        vmSelected1 = self.__checkPairCpuUsage(pair, vm)
        vmSelected2 = self.__checkPairMemoryUsage(pair, vm)
        vmSelected3 = self.__checkPairNetworkTransmittedThroughput(pair, vm)
        vmSelected4 = self.__checkPairDiskWriteThroughput(pair, vm)

        if vmSelected1 == vmSelected2 == vmSelected3 == vmSelected4:
            return vm

        return False

    def __updateSelectedVmResourcesWithPairs(self, vmMatch, pair):
        vmMatch['Trust'] = vmMatch['Trust']
        vmMatch['CPU-Ghz'] = float(vmMatch['CPU-Ghz']) - float(pair['1st task']['CPU usage [GHZ]'])
        vmMatch['RAM-Gb'] = float(vmMatch['RAM-Gb']) - float(pair['1st task']['Memory usage [GB]'])
        vmMatch['BW-Ms'] = vmMatch['BW-Ms']
        vmMatch['DS-Gb'] = vmMatch['DS-Gb']

        # if 'tasksAssigned' not in vmMatch:
        #     vmMatch['tasksAssigned'] = []
        #     vmMatch['tasksAssigned'].append(pair['1st task'])
        # else:
        #     vmMatch['tasksAssigned'].append(pair['1st task'])

        vmMatch['Trust'] = vmMatch['Trust']
        vmMatch['CPU-Ghz'] = float(vmMatch['CPU-Ghz']) - float(pair['2nd task']['CPU usage [GHZ]'])
        vmMatch['RAM-Gb'] = float(vmMatch['RAM-Gb']) - float(pair['2nd task']['Memory usage [GB]'])
        vmMatch['BW-Ms'] = vmMatch['BW-Ms']
        vmMatch['DS-Gb'] = vmMatch['DS-Gb']

        # if 'tasksAssigned' not in vmMatch:
        #     vmMatch['tasksAssigned'] = []
        #     vmMatch['tasksAssigned'].append(pair['2nd task'])
        # else:
        #     vmMatch['tasksAssigned'].append(pair['2nd task'])

        if 'tasksCounter' not in vmMatch:
            vmMatch['tasksCounter'] = 2
        else:
            vmMatch['tasksCounter'] += 2

        if DEBUG & True:
            print ('Updated Vm Match: ', vmMatch)
            print ('\n')

        return vmMatch

    # Method 1
    def searchForMatch(self):
        vms = self.convertTrustFileToListOfDicts()
        tasks = self.convertVmsFileToListOfDicts()
        tasks = self.computeExecutionTimeForGivenTasks(tasks)

        for task in tasks:
            if DEBUG & True:
                print ('task:', task)
            for vm in vms:
                vmMatch = self.__isMatch(task, vm)
                if vmMatch:
                    if DEBUG & True:
                        print ('Vm Match:', vmMatch)

                    updatedMatchingVm = self.__updateSelectedVmResources(vmMatch, task)
                    vms = self.__updateVmsListWithSelectedVm(vms, vm, updatedMatchingVm)
                    break

                else:
                    print ('No match found or all vms are busy. Wait for at least one vm to be available')

                # TODO: remove me. break here to check on the first item only
                # break
            # TODO: remove me. break here to check on the first item only
            # break

        if DEBUG:
            print ('\n\nvms list after processing\n')
            for vm in vms:
                print ('vm:')
                pprint.pprint(vm)

    def countDown(self, vmMatch, pair):
        print ('---vmMatch-->', vmMatch)
        print ('---pair--->', pair['total time'])

        t = int(pair['total time'] * 10)
        print ('----t---->', t)
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print ('---timeformat--->', timeformat)
            time.sleep(1)
            t -= 1

        self.__removePairsFromVmAndUpdateVmResources(vmMatch, pair)
        print ('----vmMatch updated-->', vmMatch)

    def testme(self, vmMatch, pair):
        t = Process(target=self.countDown, args=(vmMatch, pair))
        t.start()
        t.join()

    def __removePairsFromVmAndUpdateVmResources(self, vmMatch, pair):
        vmMatch['Trust'] = vmMatch['Trust']
        vmMatch['CPU-Ghz'] = float(vmMatch['CPU-Ghz']) + float(pair['1st task']['CPU usage [GHZ]'])
        vmMatch['RAM-Gb'] = float(vmMatch['RAM-Gb']) + float(pair['1st task']['Memory usage [GB]'])
        vmMatch['BW-Ms'] = vmMatch['BW-Ms']
        vmMatch['DS-Gb'] = vmMatch['DS-Gb']

        # if 'tasksAssigned' not in vmMatch:
        #     vmMatch['tasksAssigned'] = []
        #     vmMatch['tasksAssigned'].append(pair['1st task'])
        # else:
        #     vmMatch['tasksAssigned'].append(pair['1st task'])

        vmMatch['Trust'] = vmMatch['Trust']
        vmMatch['CPU-Ghz'] = float(vmMatch['CPU-Ghz']) + float(pair['2nd task']['CPU usage [GHZ]'])
        vmMatch['RAM-Gb'] = float(vmMatch['RAM-Gb']) + float(pair['2nd task']['Memory usage [GB]'])
        vmMatch['BW-Ms'] = vmMatch['BW-Ms']
        vmMatch['DS-Gb'] = vmMatch['DS-Gb']

        # if 'tasksAssigned' not in vmMatch:
        #     vmMatch['tasksAssigned'] = []
        #     vmMatch['tasksAssigned'].append(pair['2nd task'])
        # else:
        #     vmMatch['tasksAssigned'].append(pair['2nd task'])

        vmMatch['tasksCounter'] -= 2

        if DEBUG & True:
            print ('Updated Vm Match: ', vmMatch)
            print ('\n')

        return vmMatch

    # Method 2
    def searchForMatchWithGreedyAlgorithm(self):
        vms = self.convertTrustFileToListOfDicts()
        tasks = self.convertVmsFileToListOfDicts()
        tasks = self.computeExecutionTimeForGivenTasks(tasks)
        pairs = self.groupTasksInPairsAccordingToGreedyAlgorithmStrategy(tasks)

        # t = []
        for i, pair in enumerate(pairs):
            if DEBUG & True:
                print ('pair:', pair)
            for vm in vms:
                vmMatch = self.__isPairAMatch(pair, vm)
                if vmMatch:
                    if DEBUG & True:
                        print ('Vm Match:', vmMatch)

                    updatedMatchingVm = self.__updateSelectedVmResourcesWithPairs(vmMatch, pair)
                    # self.testme(vmMatch, pair)
                    t = threading.Thread(target=self.countDown, args=(vmMatch, pair))
                    t.start()
                    # t[i].start()
                    break
                    # assign the first pair processing time because it is the highest which covers the other assinged
                    # tasks that are in the same vm
                    # updatedMatchingVm['Total Processing Time'] = pairs[0]['total time']
                    # vms = self.__updateVmsListWithSelectedVm(vms, vm, updatedMatchingVm)
                    # break

                else:
                    print ('No match found or all vms are busy. Waiting for the next available vm')

                # TODO: remove me. break here to check on the first item only
                # break
            # TODO: remove me. break here to check on the first item only
            # break

        if DEBUG:
            print ('\n\nvms list after processing\n')
            for vm in vms:
                print ('vm:')
                pprint.pprint(vm)


if __name__ == "__main__":
    ts = TasksScheduler()

    # # Method 1
    # ts.searchForMatch()

    # # Method 2
    ts.searchForMatchWithGreedyAlgorithm()
