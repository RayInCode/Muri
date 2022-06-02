from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


'''
JOB status:
ADDED: add job into JOBS
EVENT: init job events into event list
PENDING:
RUNNING: running job
END: completed
ERROR
'''
# import numpy
import math
import util
import models
import csv
import time
import sys
import random
import copy
# import cluster
# from switch import _Switch
# from node import _Node
# from cluster import _Cluster

# #get host info
# CLUSTER = cluster.CLUSTER
import flags
FLAGS = flags.FLAGS

job_time_dict = dict()
job_time_dict[1] = {"vgg16-16": {"model": "vgg16", "bs": 16, "iter_time": 107, "resource_time": [117, 68, 0]},
                "vgg19-16": {"model": "vgg19", "bs": 16, "iter_time": 109, "resource_time": [114, 80, 0]},
                # "resnet50-64": {"model": "resnet50", "bs": 64, "iter_time": 468, "resource_time": [370, 179, 0]},
                "resnet18-128": {"model": "resnet18", "bs": 128, "iter_time": 779, "resource_time": [711, 110, 0]},
                "shufflenet_v2_x1_0-128": {"model": "shufflenet_v2_x1_0", "bs": 128, "iter_time": 798, "resource_time": [706, 59, 0]},
                "bert-4": {"model": "bert", "bs": 4, "iter_time": 178, "resource_time": [0.5, 160, 0]},
                "gpt2-4": {"model": "gpt2", "bs": 4, "iter_time": 426, "resource_time": [0.6, 410, 0]},
                "a2c-64": {"model": "a2c", "bs": 64, "iter_time": 517, "resource_time": [514, 14, 0]},
                "dqn-128": {"model": "dqn", "bs": 128, "iter_time": 490, "resource_time": [446, 8, 0]}}
job_time_dict[2] = {"vgg16-16": {"model": "vgg16", "bs": 16, "iter_time": 191, "resource_time": [114, 72, 40]},
                "vgg19-16": {"model": "vgg19", "bs": 16, "iter_time": 205, "resource_time": [115, 83, 41]},
                # "resnet50-64": {"model": "resnet50", "bs": 64, "iter_time": 590, "resource_time": [375, 179, 75]},
                "resnet18-128": {"model": "resnet18", "bs": 128, "iter_time": 881, "resource_time": [687, 110, 95]},
                "shufflenet_v2_x1_0-128": {"model": "shufflenet_v2_x1_0", "bs": 128, "iter_time": 850, "resource_time": [747, 58, 18]},
                "bert-4": {"model": "bert", "bs": 4, "iter_time": 195, "resource_time": [0.5, 163, 18]},
                "gpt2-4": {"model": "gpt2", "bs": 4, "iter_time": 464, "resource_time": [0.7, 416, 40]},
                "a2c-64": {"model": "a2c", "bs": 64, "iter_time": 525, "resource_time": [504, 14, 0.5]},
                "dqn-128": {"model": "dqn", "bs": 128, "iter_time": 495, "resource_time": [441, 8, 0.6]}}
job_time_dict[4] = {"vgg16-16": {"model": "vgg16", "bs": 16, "iter_time": 201, "resource_time": [82, 72, 67]},
                "vgg19-16": {"model": "vgg19", "bs": 16, "iter_time": 212, "resource_time": [84, 85, 73]},
                # "resnet50-64": {"model": "resnet50", "bs": 64, "iter_time": 666, "resource_time": [378, 180, 151]},
                "resnet18-128": {"model": "resnet18", "bs": 128, "iter_time": 921, "resource_time": [723, 113, 73]},
                "shufflenet_v2_x1_0-128": {"model": "shufflenet_v2_x1_0", "bs": 128, "iter_time": 886, "resource_time": [703, 62, 17]},
                "bert-4": {"model": "bert", "bs": 4, "iter_time": 190, "resource_time": [0.5, 163, 18]},
                "gpt2-4": {"model": "gpt2", "bs": 4, "iter_time": 433, "resource_time": [0.6, 413, 20]},
                "a2c-64": {"model": "a2c", "bs": 64, "iter_time": 533, "resource_time": [502, 10, 0.3]},
                "dqn-128": {"model": "dqn", "bs": 128, "iter_time": 505, "resource_time": [440, 8, 0.4]}}
job_time_dict[8] = {"vgg16-16": {"model": "vgg16", "bs": 16, "iter_time": 214, "resource_time": [82, 75, 66]},
                "vgg19-16": {"model": "vgg19", "bs": 16, "iter_time": 226, "resource_time": [82, 88, 60]},
                # "resnet50-64": {"model": "resnet50", "bs": 64, "iter_time": 650, "resource_time": [379, 182, 156]},
                "resnet18-128": {"model": "resnet18", "bs": 128, "iter_time": 1010, "resource_time": [784, 117, 77]},
                "shufflenet_v2_x1_0-128": {"model": "shufflenet_v2_x1_0", "bs": 128, "iter_time": 957, "resource_time": [769, 57, 10]},
                "bert-4": {"model": "bert", "bs": 4, "iter_time": 192, "resource_time": [0.5, 167, 59]},
                "gpt2-4": {"model": "gpt2", "bs": 4, "iter_time": 437, "resource_time": [0.6, 419, 49]},
                "a2c-64": {"model": "a2c", "bs": 64, "iter_time": 555, "resource_time": [502, 14, 0.4]},
                "dqn-128": {"model": "dqn", "bs": 128, "iter_time": 509, "resource_time": [435, 8, 0.5]}}
job_time_dict[16] = {"vgg16-16": {"model": "vgg16", "bs": 16, "iter_time": 332, "resource_time": [83, 68, 110]},
                "vgg19-16": {"model": "vgg19", "bs": 16, "iter_time": 302, "resource_time": [102, 78, 123]},
                # "resnet50-64": {"model": "resnet50", "bs": 64, "iter_time": 681, "resource_time": [433, 177, 154]},
                "resnet18-128": {"model": "resnet18", "bs": 128, "iter_time": 1055, "resource_time": [736, 108, 93]},
                "shufflenet_v2_x1_0-128": {"model": "shufflenet_v2_x1_0", "bs": 128, "iter_time": 1006, "resource_time": [776, 57, 21]},
                "bert-4": {"model": "bert", "bs": 4, "iter_time": 244, "resource_time": [0.5, 166, 86]},
                "gpt2-4": {"model": "gpt2", "bs": 4, "iter_time": 491, "resource_time": [0.6, 415, 137]},
                "a2c-64": {"model": "a2c", "bs": 64, "iter_time": 567, "resource_time": [514, 14, 1.2]},
                "dqn-128": {"model": "dqn", "bs": 128, "iter_time": 525, "resource_time": [438, 8, 1.2]}}
job_time_dict[32] = {"vgg16-16": {"model": "vgg16", "bs": 16, "iter_time": 336, "resource_time": [87, 67, 131]},
                "vgg19-16": {"model": "vgg19", "bs": 16, "iter_time": 356, "resource_time": [89, 79, 141]},
                # "resnet50-64": {"model": "resnet50", "bs": 64, "iter_time": 753, "resource_time": [358, 177, 156]},
                "resnet18-128": {"model": "resnet18", "bs": 128, "iter_time": 1059, "resource_time": [712, 111, 93]},
                "shufflenet_v2_x1_0-128": {"model": "shufflenet_v2_x1_0", "bs": 128, "iter_time": 1019, "resource_time": [799, 56, 24]},
                "bert-4": {"model": "bert", "bs": 4, "iter_time": 260, "resource_time": [0.5, 166, 133]},
                "gpt2-4": {"model": "gpt2", "bs": 4, "iter_time": 514, "resource_time": [0.7, 414, 216]},
                "a2c-64": {"model": "a2c", "bs": 64, "iter_time": 585, "resource_time": [507, 14, 2]},
                "dqn-128": {"model": "dqn", "bs": 128, "iter_time": 546, "resource_time": [437, 8, 1.6]}}


class _TFJobs(object):

    '''
    nested-class g_job
    '''
    class g_job(object):
        def __init__(self, num_gpu, total_gpu=0):
            self.num_gpu = num_gpu       
            self.name = str(num_gpu) + '-GPU'
            self.total_job = 0
            self.end_job = 0
            self.num_queue = 2
            self.queues = [list() for i in range(self.num_queue)]
            self.queue_limit = [3600, 7200, 18000]
            self.total_gpu = total_gpu
            self.free_gpu = total_gpu
            self.running_jobs = list()
            self.pending_jobs = list()
            self.runnable_jobs = list()

        def alloc_free_gpus(self, need_num):
            if self.free_gpu >= need_num:
                self.free_gpu -= need_num
                return True
            else:
                return False

        def release_job_gpu(self, num_job=1):
            if num_job < 0:
                util.print_fn("Error: num_job < 0")
                exit()
            self.free_gpu += int(self.num_gpu * num_job)

        def empty_gpu_alloc(self):
            self.free_gpu = self.total_gpu

        def get_gpu_reservation(self, reserved_num):
            '''
            Cluster manager should decide (dynamically) the reserved gpus for each g_job object
            '''
            # diff_gpu = reserved_num - self.total_gpu
            # self.total_gpu = reserved_num
            # # how to update free_gpu
            # self.free_gpu += diff_gpu
            used = self.total_gpu - self.free_gpu
            self.total_gpu = reserved_num
            self.free_gpu = self.total_gpu - used


        def get_gpu_demands(self):
            # return int((len(self.running_jobs) + len(self.pending_jobs)) * self.num_gpu)
            return int(len(self.runnable_jobs) * self.num_gpu)

    def __init__(self):
        self.num_job = 0        
        self.job_list = list()
        ''' job events is a list of tuple
            (time, dict)
        dict:
            'start_jobs': [xxx,xxx,xxx]
            'end_jobs': [xxx,xxx,xxx]
        '''
        self.job_events = list()        
        #holding pending jobs, add job_idx
        self.pending_jobs = list() # [{job_dict}, {job_dict}]
        self.runnable_jobs = list() # pending + running
        self.running_jobs = list() # running
        self.completed_jobs = list()

        self.migratable_jobs = list()
        self.num_queue = 3
        self.queues = [list() for i in range(self.num_queue)]
        self.queue_limit = [3250, 7200, 18000]

        # mem info in GB
        self.worker_mem = 5
        self.ps_mem = 6
        self.p_w_mem = 0.1

        #sim-gpu-demands
        self.gpu_job = dict()

        #gittins static delta
        self.gittins_delta = 3250

        self.mean_duration = 800
        self.job_dist_data = None

        self.overhead_list = []
        for _ in range(0, 5):
            self.overhead_list.append([])

        self.itertime_overhead_list = [1 for _ in range(4)]

    def get_job_model(self, job_dict):
        # if job_dict.has_key('model_name') and job_dict.has_key('model_scale'):
        if ('model_name' in job_dict) and ('model_scale' in job_dict):
            job_dict['model'] = models.get_model_with_scale(job_dict['model_name'], job_dict['model_scale'])
        else:
            util.print_fn('Not enough model information to get the details')


    def get_network_load(self, job_dict):
        if 'num_gpu' not in job_dict:
            util.print_fn('No gpu information')
            return 

        if 'model' not in job_dict:
            util.print_fn('No model information')
            return
        
        num_w = job_dict['num_gpu']
        num_ps = num_w


        if num_w == 1:
            job_dict['ps_network'] = list()
            job_dict['w_network'] = list([0])

            '''
            check job ps_size 
            '''
            job_dict['ps_ave'] = 0
            return

        job_dict['w_network'] = list([job_dict['model']['total_size']] * num_w)
        job_dict['ps_network'] = list([0] * num_ps)
        for i in range(0, len(job_dict['model']['tensors'])):
            ps_idx = int(i % num_ps)
            # job_dict['ps_network'][ps_idx] += (job_dict['model']['tensors'][i] * num_w)
            job_dict['ps_network'][ps_idx] += (job_dict['model']['tensors'][i])

        for i in range(0, len(job_dict['ps_network'])):
            job_dict['ps_network'][i] = round(job_dict['ps_network'][i], 1)

        '''
        check the PS job size information  
        job_dict['ps_ave'] = round(numpy.mean(job_dict['ps_network']), 1)
        if job_dict['ps_ave'] == 0:
            print(job_dict)

        s_ps_list = sorted(job_dict['ps_network'], reverse=True) 
        job_dict['ps_max'] = s_ps_list[0] 
        max99_idx = int(math.ceil(num_ps * 0.01))
        job_dict['ps_max99th'] = s_ps_list[max99_idx]
        job_dict['ps_max_ave'] = round(job_dict['ps_max'] / job_dict['ps_ave'], 1)
        job_dict['ps_max99_ave'] = round(job_dict['ps_max99th'] / job_dict['ps_ave'], 1)
        '''


    def add_job(self, job_dict):
        ''' Add job (job_dict) into job_list'''
        job_dict['resource_time'] = list()
        for key, value in job_dict.items():
        # for key, value in job_dict.iteritems():
            if (value is None) or ('resource_time' == key):
                continue
            if 'resource_time' in key:
                job_dict['resource_time'].append(float(value))
            elif value.isdigit():
                job_dict[key] = int(value)
        job_dict['duration'] = int(float(job_dict['duration']))
        # job_dict['duration'] = int(job_dict['duration'])

        job_dict['rank'] = sys.maxsize

        # if 'iteration_time' not in job_dict:
        #     job_dict['iteration_time'] = job_dict['duration'] / job_dict['iterations']
        # else:
        job_dict['submit_time'] /= 1000
        job_dict['duration'] = job_dict['duration']/1000

        # if 'worstordering' in FLAGS.schedule:
        #     self.itertime_overhead_list = [1.015, 1.13/1.015, 1.2/1.015, 1.17/1.015]
        # else:
        self.itertime_overhead_list = [1.015, 1.33/1.015, 1.5/1.015, 1.37/1.015]
        
        if 'multi-resource-gpu-unaware' == FLAGS.schedule:
            self.itertime_overhead_list[3] = 1.3/1.015

        job_dict['iteration_time'] = job_dict['iteration_time']*self.itertime_overhead_list[0]/1000 #1.09
        # if 'batch_size' not in job_dict:
        #     job_dict['batch_size'] = 16
        job_dict['tput'] = 1/job_dict['iteration_time']

        if 'start_time' not in job_dict:
            job_dict['start_time'] = 0
        if 'end_time' not in job_dict:
            job_dict['end_time'] = 0
        if 'pending_time' not in job_dict:
            job_dict['pending_time'] = 0
        job_dict['remaining_iteration'] = float(job_dict['iterations'])
        # if no resource time is provided, we assume there are 3 resources and rand their time
        if 'multi-resource' in FLAGS.schedule or 'antman' in FLAGS.schedule:
            # job_dict['executed_iteration'] = 0.0
            if 'iteration_time' not in job_dict:
                job_dict['iteration_time'] = float(job_dict['duration'])/float(job_dict['iterations'])
            job_dict['iteration_time_cur'] = copy.deepcopy(job_dict['iteration_time'])
            if len(job_dict['resource_time']) == 0:
                tmp_resource = [random.uniform(1.0, 10.0) for i in range(FLAGS.multi_resource)]
                tmp_resource_sum = sum(tmp_resource)
                tmp_resource_time = [tmp_resource[i]/tmp_resource_sum * float(job_dict['iteration_time']) for i in range(FLAGS.multi_resource) ]
                tmp_resource_time[-1] = float(job_dict['iteration_time']) - sum(tmp_resource_time[:-1])
                job_dict['resource_time'] = copy.deepcopy(tmp_resource_time)
            else:
                for i in range(len(job_dict['resource_time'])):
                    job_dict['resource_time'][i] /= 1000

        if 'submit_time' in job_dict:
            job_dict['r_submit_time'] = int(-1 * job_dict['submit_time'])
        if 'antman' in FLAGS.schedule:
            if 'priority' not in job_dict:
                job_dict['priority'] = random.randint(0,1)
            if 'gpu_util' not in job_dict:
                if job_dict['priority']==0:
                    job_dict['gpu_util'] = 0.1 # not real
                else:
                    job_dict['gpu_util'] = 0.9
        
        job_dict['start_time'] = sys.maxsize
        job_dict['end_time'] = 0
        job_dict['pending_time'] = 0

        job_dict['packing_used'] = 0 # 0 - not used; 1 - prepare for packing; 2 - used

        # How much time this job has been executed? For preemption algorithms, this should be accumulated
        job_dict['execution_time'] = 0
        job_dict['last_start_time'] = 0
        job_dict['last_check_time'] = 0
        job_dict['executed_time'] = 0
        job_dict['remaining_iterations'] = job_dict['iterations']

        job_dict['preempt'] = 0
        job_dict['resume'] = 0
        job_dict['promote'] = 0
        job_dict['job_counter'] = 0
        job_dict['packing'] = None

        job_dict['status'] = 'ADDED'
        job_dict['job_idx'] = len(self.job_list)
        # random the priority of the job: 0 - resource-guarantee job; 1 - opportunistic job

        # job_dict['ps'] = int(job_dict['ps'])
        # job_dict['worker'] = int(job_dict['worker'])
        # job_dict['batch_size'] = int(job_dict['batch_size'])
        # job_dict['num_batch'] = int(job_dict['num_batch'])
        # job_dict['sleep'] = int(job_dict['sleep'])

        job_dict['gpus'] = list()
        job_dict['placements'] = list() #prepare an empty job_placement 
        job_dict['ps_placements'] = list()
        job_dict['w_placements'] = list()
        job_dict['remaining_gpu'] = job_dict['num_gpu']
        job_dict['last_node_id'] = None
        '''
        MS_YARN: only one switch is allowed
        template:
        [{'switch': xx, 'nodes': [{'id':xx, 'num_gpu':xxx}]},
         {'switch': xx, 'nodes': [{'id':xx, 'num_gpu':xxx}, {'id':xx, 'num_gpu':xxx}]},
         {'switch': xx, 'nodes': [{'id':xx, 'num_gpu':xxx}]},
        ]
        '''

        # if ('end_time' in job_dict) and ('duration' not in job_dict):
        #     job_dict['duration'] = job_dict['end_time'] - job_dict['start_time']
        # else:
        #     job_dict['end_time'] = job_dict['start_time'] + job_dict['duration']
        
        if 'model_scale' not in job_dict:
            job_dict['model_scale'] = 1
        #get detailed model inforamtion
        self.get_job_model(job_dict)

        #add job ps/worker information
        self.get_network_load(job_dict)

        self.job_list.append(job_dict)
        self.num_job += 1

        if FLAGS.schedule == 'multi-dlas-gpu':
            num_gpu = job_dict['num_gpu']
            if num_gpu not in self.gpu_job:
                # add that job class
                self.gpu_job[num_gpu] = self.g_job(num_gpu)

            self.gpu_job[num_gpu].total_job += 1


    def print_all_job_size_info(self):
        '''        
        print job tensor info
        '''

        ps_max_ave_fd = open('ps_max_ave.csv', 'w+')
        ps_max_ave_writer = csv.writer(ps_max_ave_fd)  
        ps_max_ave_writer.writerow(['ps_max_ave'])

        ps_max99_ave_fd = open('ps_max99_ave.csv', 'w+')
        ps_max99_ave_writer = csv.writer(ps_max99_ave_fd)  
        ps_max99_ave_writer.writerow(['ps_max99_ave'])

        w_fd = open('w.csv', 'w+')
        w_writer = csv.writer(w_fd)  
        w_writer.writerow(['w'])

        ps_fd = open('ps.csv', 'w+')
        ps_writer = csv.writer(ps_fd)  
        ps_writer.writerow(['ps'])

        ps_w_fd = open('ps_w.csv', 'w+')
        ps_w_writer = csv.writer(ps_w_fd)  
        ps_w_writer.writerow(['ps_w'])

        util.print_fn("Start to dump job information")
        for job in self.job_list:
            if job['ps_ave'] != 0:
                ps_max_ave_writer.writerow(list([job['ps_max_ave']]))
                ps_max99_ave_writer.writerow(list([job['ps_max99_ave']]))
                w_writer.writerow(list([job['w_network'][0]]))
                # ps_w_writer.writerow(job['w_network'][0])
                # for ps in job['ps_network']:
                #     ps_writer.writerow(ps)
                #     ps_w_writer.writerow(ps)
                
        ps_max_ave_fd.close()
        ps_max99_ave_fd.close()
        w_fd.close()
        ps_fd.close()
        ps_w_fd.close()
        
    def find_runnable_job(self, job_idx):
        for job in self.runnable_jobs:
            if job['job_idx'] == job_idx:
                return job
        print(f'Not found {job_idx} in runnable_jobs.')
        print([job['job_idx'] for job in self.runnable_jobs])
        assert 1==0

    def read_job_info(self, job_idx, field=None):
        ''' Read  job information, if field == NONE, show all job info'''
        ''' job_id,num_gpu,submit_time,start_time,duration,model_size,aggr_interval '''
        print('  Job[%d]: ' % job_idx)

        for job in self.job_list:
            if job['job_idx'] == job_idx:
                #find the job
                if field:
                    if isinstance(job[field], int):
                        print('%s :  %d' % (field, job[field]))
                    else:
                        print('%s :  %s' % (field, job[field]))
                else:
                    print(job)
                print('')

    def read_all_jobs(self, field=None):
        for j in self.job_list:
            print('  Job[%d]: ' % j['job_idx'])
            if field:
                if isinstance(j[field], int):
                    print('%s :  %d' % (field, j[field]))
                else:
                    print('%s :  %s' % (field, j[field]))
            else:
                print(j)
            print('')

    def sort_all_jobs(self, mode=None):
        '''
        Sort jobs based on their sumbit_time
        j1, num_gpu, start_t, end_t, duration
        '''
        # tmp_list = sorted(self.job_list, key = lambda e:e.__getitem__('start_time'))
        # tmp_dict = util.search_dict_list(self.job_list, 'start_time', 4)
        # tmp_dict['end_time'] = 15
        # print(tmp_dict)
        # self.job_list = tmp_list

        self.job_list.sort(key = lambda e:e.__getitem__('submit_time'))
        util.print_fn('   Jobs are sorted with their start time')
        # self.read_all_jobs()
        if FLAGS.schedule == 'multi-dlas-gpu' and FLAGS.scheme == 'count':
            for num_gpu, gjob in self.gpu_job.items():
                util.print_fn('%d-GPU jobs have %d ' % (num_gpu, gjob.total_job))

    def create_multi_nodes_placement(self, job, switch_id, node_list):
        tmp_dict = dict() 
        tmp_dict['switch'] = switch_id
        tmp_dict['nodes'] = node_list
        job['placements'].append(tmp_dict)

    def create_multi_nodes_placement_same_switch(self, job, switch_id, node_list):
        if len(job['placements'])==0:
            self.create_multi_nodes_placement(job, switch_id, node_list)       
        else:
            for placement in job['placements']:
                if placement['switch'] == switch_id:
                    placement['nodes'].extend(node_list)


    def create_single_node_placement(self, job, switch_id, node_id, num_gpu, num_cpu, mem=0, gpu_list=[], not_first=False):
        '''
        under this switch, there is only one need used
        {'switch': xx, 'nodes': [{'id':xx, 'num_gpu':xxx, 'num_cpu': xxx, 'network': xxxx, 'tasks': [w0, w1, ps1]}]}
        '''
        if not_first:
            node_dict = job['placements'][0]['nodes'][0]
            node_dict['num_gpu']+=num_gpu
            node_dict['num_cpu']+=num_cpu
            node_dict['mem']+=mem
            node_dict['gpu_list'].extend(gpu_list)
            # print(job['job_idx'], job['placements'][0]['nodes'][0])
        else:
            tmp_dict = dict() 
            tmp_dict['switch'] = switch_id
            node_dict = dict()
            node_dict['id'] = node_id
            node_dict['num_gpu'] = num_gpu
            node_dict['num_cpu'] = num_cpu
            node_dict['mem'] = mem
            node_dict['tasks'] = list()
            # node_dict['network'] = round(sum(job['w_network']) + sum(job['ps_network']), 1)
            node_dict['network'] = 0 #single machine, no network traffic
            node_dict['gpu_list'] = gpu_list

            tmp_dict['nodes'] = list()
            tmp_dict['nodes'].append(node_dict)
            job['placements'].append(tmp_dict)

        return node_dict['network']

    def remove_from_pending(self, job, event_time):
        job['status'] = 'RUNNING'
        job['start_time'] = event_time
        job['end_time'] = job['start_time'] + job['duration']
        job['pending_time'] = job['start_time'] - job['submit_time']

        self.pending_jobs.remove(job)

    def move_to_pending(self, job):
        job['status'] = 'PENDING'
        self.pending_jobs.append(job)


    def update_pending_time(self, event_time):
        for job in self.pending_jobs:
            if 'sumbit_time' in job:
                job['pending_time'] = int(event_time - job['submit_time'])

    def add_to_runnable(self, job):
        job['status'] = 'PENDING'
        self.runnable_jobs.append(job)

    def push_job_to_running(self, job, event_time):
        if job['status'] != 'PENDING':
            return
        job['status'] = 'RUNNING'
        if job['start_time'] == 0:
            job['start_time'] = event_time
        job['last_start_time'] = event_time


    def sort_shortest_runnable_jobs(self, event_time):
        for job in self.runnable_jobs:
            if job['status'] == 'RUNNING':
                new_execution_time = int(event_time - job['last_check_time'])
                job['execution_time'] = int(job['execution_time'] + new_execution_time)
                job['remaining_time'] = int(job['duration'] - job['execution_time'])

            elif job['status'] == 'PENDING':
                job['execution_time'] = 0
                job['remaining_time'] = int(job['duration'])

            job['last_check_time'] = int(event_time)

        JOBS.runnable_jobs.sort(key = lambda e:e.__getitem__('remaining_time'))

    def move_to_runnable(self, job):
        ''' job gets into the system: pending or running, and finally END'''
        #job not started yet
        job['status'] = 'PENDING'
        job['start_time'] = sys.maxsize
        job['last_start_time'] = 0
        job['last_check_time'] = job['submit_time']
        job['total_executed_time'] = 0 # total
        job['total_executed_gputime'] = 0
        job['calc_executed_time'] = 0
        job['executed_time'] = 0 # used for deciding priority queue, may be zeroed by last_pending_time
        job['pending_time'] = 0
        job['last_pending_time'] = 0 # how much pending_time the job has since last entering the highest priority queue

        if FLAGS.schedule == 'multi-dlas-gpu':
            num_gpu = job['num_gpu']
            self.gpu_job[num_gpu].runnable_jobs.append(job)
        elif 'multi-resource' in FLAGS.schedule or 'antman' in FLAGS.schedule:
            # job['executed_iteration'] = 0
            self.runnable_jobs.append(job)
        else:
            self.runnable_jobs.append(job)
    
    def update_priority_queues(self, gputime=False):
        for queue in self.queues:
            del queue[:]
        for job in self.runnable_jobs:
            if gputime:
                j_gt = int(job['executed_time'] * job['num_gpu'])
            else:
                j_gt = int(job['executed_time'])

            if j_gt < self.queue_limit[0]:
                self.queues[0].append(job)
                job['q_id'] = 0
            else:
                self.queues[1].append(job)
                job['q_id'] = 1

            # elif j_gt < self.queue_limit[1]:
            #     self.queues[1].append(job)
            #     job['q_id'] = 1
            # elif j_gt < self.queue_limit[2]:
            #     self.queues[2].append(job)
            #     job['q_id'] = 2
            # else:
            #     self.queues[3].append(job)
            #     job['q_id'] = 3

   
    def print_job_events(self):
        util.print_fn('    Print all job events ')
        for event in self.job_events:
            util.print_fn('      event.time[%d], with %d start_jobs, and %d end_jobs' % 
                            (event['time'], len(event['start_jobs']), len(event['end_jobs'])))

        util.print_fn(' ')

    def add_job_end_event(self, job):
        #for job end 
        tmp_dict = util.search_dict_list(self.job_events, 'time', job['end_time'])
        if tmp_dict == None:
            #not found, add the time into to job_events
            tmp_dict = dict()
            tmp_dict['time'] = job['end_time']
            tmp_dict['start_jobs'] = list()
            tmp_dict['end_jobs'] = list()
            tmp_dict['end_jobs'].append(job)
            self.job_events.append(tmp_dict)
        else:
            tmp_dict['end_jobs'].append(job)

        # ''' sort events based on their time'''
        # self.job_events.sort(key = lambda e:e.__getitem__('time'))



    def prepare_job_start_events(self):
        '''
        add job start events into job_events list
        end events should be added when they are starting
        '''
        for job in self.job_list:
            start_t = job['submit_time']
            # util.print_fn('%d, %d' % (start_t, end_t))

            #for job start
            tmp_dict = util.search_dict_list(self.job_events, 'time', start_t)
            if tmp_dict == None:
                #not found, add the time into to job_events
                tmp_dict = dict()
                tmp_dict['time'] = start_t
                tmp_dict['start_jobs'] = list()
                tmp_dict['end_jobs'] = list()
                tmp_dict['start_jobs'].append(job)
                self.job_events.append(tmp_dict)
            else:
                tmp_dict['start_jobs'].append(job)


            job['status'] = 'EVENT' #job has been in EVENT status

        ''' sort events based on their time'''
        self.job_events.sort(key = lambda e:e.__getitem__('time'))
        util.print_fn('Init, add job start events')
        self.print_job_events()


    def add_migratable(self, job):
        '''
        add job into migratable job list 
        1. distributed jobs
        2. running jobs
        3. ?
        '''
        if job['num_w'] <= 1:
            return

        #if job is distributed ?

        if job not in self.migratable_jobs:
            self.migratable_jobs.append(job)            


    def remove_migratable(self, job):
        '''
        remove from migratable job list

        '''
        if job in self.migratable_jobs:
            self.migratable_jobs.remove(job)


    def add_gpu_job(self, job):
        '''
        only used in sim-gpu-demands
        '''
        num_gpu = job['num_gpu']
        if num_gpu not in self.gpu_job:
            self.gpu_job[num_gpu] = 0
        self.gpu_job[num_gpu] = self.gpu_job[num_gpu] + 1

    def delete_gpu_job(self, job):
        num_gpu = job['num_gpu']
        if num_gpu not in self.gpu_job:
            print("Error in release_gpu_job")

        self.gpu_job[num_gpu] = self.gpu_job[num_gpu] - 1

    def end_job(self, e_job):
        if FLAGS.schedule != 'multi-dlas-gpu':
            util.print_fn("Not multi-dlas-gpu")
            exit()
        
        num_gpu = e_job['num_gpu']
        gjob = self.gpu_job[num_gpu]
        gjob.release_job_gpu(1)
        gjob.runnable_jobs.remove(e_job)
        # gjob.running_jobs.remove(e_job)
        gjob.queues[e_job['q_id']].remove(e_job)       
        gjob.end_job += 1


    def init_reserve_gpus(self, total_num):
        num_group = len(self.gpu_job)
        ave_gpu = math.floor(total_num / num_group)
        for num_gpu, gjob in self.gpu_job.items():
            gjob.get_gpu_reservation(ave_gpu)

    def reserve_gpus(self, total_num):
        '''
        GPU cluster reserve gpus for gpu_job groups
        '''
        num_group = len(self.gpu_job)
        ave_gpu = math.floor(total_num / num_group)

        job_list = list()
        for num_gpu, gjob in self.gpu_job.items():
            tmp_dict = dict()
            tmp_dict['num_gpu'] = num_gpu
            tmp_dict['used_gpu'] = gjob.total_gpu - gjob.free_gpu
            tmp_dict['demands'] = gjob.get_gpu_demands()
            tmp_dict['cur_gpu'] = gjob.total_gpu
            tmp_dict['cur_free_gpu'] = gjob.free_gpu
            tmp_dict['reserve'] = 0
            job_list.append(tmp_dict)

        total_free_gpu = total_num - sum(k['used_gpu'] for k in job_list) 
        total_demands = sum(k['demands'] for k in job_list)
        # print('total_free %d, total_demands %d' % (total_free_gpu, total_demands))
        if total_demands == 0: 
            return
        
        '''demand-based, keep current used_gpu'''
        remain_free_gpu = total_free_gpu
        job_list.sort(key = lambda e:e.__getitem__('demands'))
        for job_dict in job_list:
            if job_dict['demands'] == 0:
                continue

            ratio = round((job_dict['demands'] * 1.0) / total_demands, 2)
            cal_gpu = int(math.floor((ratio * total_num) / job_dict['num_gpu']) * job_dict['num_gpu'])
            cal_gpu = job_dict['demands'] if job_dict['demands'] <= cal_gpu else cal_gpu
            extra_gpu = cal_gpu - job_dict['used_gpu']
            if extra_gpu <= 0:
                extra_gpu = 0
            elif extra_gpu > remain_free_gpu:
                extra_gpu = int(math.floor(remain_free_gpu / job_dict['num_gpu']) * job_dict['num_gpu'])

            # print('%d-GPU, u%d, cal_gpu %d, extra_g %d' %(job_dict['num_gpu'], job_dict['used_gpu'], cal_gpu, extra_gpu))
            job_dict['reserve'] = job_dict['used_gpu'] + extra_gpu
            remain_free_gpu -= extra_gpu
            # if remain_free_gpu <= 0:
            #     break

        ''' still remaining, give to the right job group'''
        job_list.sort(key = lambda e:e.__getitem__('num_gpu'))
        num_full = 0
        while remain_free_gpu > 0:
            # if all are satisfied
            if num_full >= len(job_list):
                break
            else:
                num_full = 0

            for job_dict in job_list:
                if job_dict['demands'] <= job_dict['reserve']:
                    num_full += 1
                    continue
                if remain_free_gpu >= job_dict['num_gpu']:                
                    remain_free_gpu -= job_dict['num_gpu']
                    job_dict['reserve'] += job_dict['num_gpu']
                else:
                    num_full += 1

                if remain_free_gpu <= 0: 
                    break

        #execute reservation
        for job_dict in job_list:
            num_gpu = job_dict['num_gpu']
            self.gpu_job[num_gpu].get_gpu_reservation(job_dict['reserve'])
            print("%d-j, T%d, F%d, U%d, N%d, R%d; " % (job_dict['num_gpu'], job_dict['cur_gpu'], job_dict['cur_free_gpu'], job_dict['used_gpu'], job_dict['demands'], job_dict['reserve']), end=' ')

        for num_gpu, gjob in self.gpu_job.items():
            if gjob.free_gpu < 0:
                print("Error free gpu, %d" % num_gpu)
                exit()


        util.print_fn(' %s is done' % sys._getframe().f_code.co_name)

    def completion_check(self):
        for num_gpu, gjob in self.gpu_job.items():
            if gjob.end_job != gjob.total_job:
                util.print_fn('!!!! Miss-match %d completed jobs with %d total jobs in %d-GPU jobs' % (gjob.end_job, gjob.total_job, num_gpu))

    def test_reserve_gpus(self, total_num):
        for num_gpu, gjob in self.gpu_job.items():
            gjob.total_gpu = 0
            gjob.free_gpu = 0
            gjob.runnable_jobs = []

        self.gpu_job[8].total_gpu = 32
        self.gpu_job[8].free_gpu = 0 
        self.gpu_job[8].runnable_jobs.extend([4,5,6,7,8])

        self.gpu_job[16].total_gpu = 32 
        self.gpu_job[16].free_gpu = 16
        self.gpu_job[16].runnable_jobs.extend([5,6,7,8,9])

        self.reserve_gpus(total_num)

    def print_placement(self, ejob):
        print("placement of job ", ejob['job_idx'])
        print(ejob['placements'])

    def calc_packing_finished_info(self, rjob, tmp_time, last_check_time):
        iter_list = list()
        # print('in calc_packing_info: ', rjob['job_idx'], [tjob.job_idx for tjob in rjob['packing'].packing_jobs])
        if rjob['packing']==None:
            iter_list.append(rjob['remaining_iterations'])
        else:
            for pjob_mini in rjob['packing'].packing_jobs:
                pjob=self.find_runnable_job(pjob_mini.job_idx)
                iter_list.append(pjob['remaining_iterations'])
            sim_itertime = rjob['packing'].calc_iteration_time()
            real_itertime = rjob['real_itertime'][0]
            overhead_error = (real_itertime-sim_itertime)/sim_itertime
            self.overhead_list[len(rjob['packing'].packing_jobs)].append(overhead_error)
                # print(pjob['job_idx'], pjob['real_itertime'], pjob['remaining_iterations'])
        iter_list = list(set(iter_list))
        iter_list.sort()
        if iter_list[0]==0:
            del iter_list[0]
        # print('calc_packing_finished_info, real_itertime vs iter_list: ', iter_list)
        assert len(rjob['real_itertime']) == len(iter_list)
        finished_iteration = 0
        if rjob['last_finish_time']>last_check_time:
            overhead_time = copy.deepcopy(rjob['last_finish_time'])
            # print('calc jobs: ', rjob['job_idx'], rjob['last_iters'])
            last_iter = 0
            assert len(rjob['last_iters']) == len(rjob['real_itertime'])
            for idx, itertime in enumerate(rjob['real_itertime']):
                overhead_time -= (rjob['last_iters'][idx]-last_iter) * itertime
                last_iter = rjob['last_iters'][idx]
        else:
            overhead_time = last_check_time
        remaining_time = tmp_time - overhead_time
        finished_time = overhead_time
        done_idx = 0
        last_iter = 0
        # print('calc jobs: ', rjob['job_idx'], overhead_time-last_check_time)
        for idx, iters in enumerate(iter_list):
            if iters > rjob['remaining_iterations']:
                break
            time0 = (iters-last_iter)*rjob['real_itertime'][idx]
            if remaining_time - time0>=0:
                remaining_time -= time0
                finished_time += time0
                finished_iteration += (iters-last_iter)
                done_idx += 1
                last_iter = iters
            else:
                finished_time = tmp_time
                finished_iteration += int(remaining_time / rjob['real_itertime'][idx])
                break
        
        assert finished_iteration<=rjob['remaining_iterations']
        return finished_time, finished_iteration, done_idx


JOBS = _TFJobs()

_allowed_symbols = [
    'JOBS'
]
