import numpy as np
import random
import math
from .Lattice import Lattice
from .Arraysite import Arraysite


class AnnStart(object):

    def __init__(self,
                 nstep=None,
                 nn = None,
                 data = None,
                 lattice =None,
                  ) -> None:
       
       
      self.index_types = self.start(nstep,data,nn,lattice)


    def start(self,nstep,data,nn,lattice):
      
        time =0.0
        vac = np.array([0.0,0.0,0.0])

        for h in range(nstep):

            Rate_total_list = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]


            # 空位周围的能量
            str_vac = ' '.join(str(i) for i in vac)

            array1  = nn.all_array_list(str_vac)

            #插入神经网络得到能量
            energyA = 1

            for i in data.neighbor1:       
                        
                        neighbor_points = vac+i[1]
                        neighbor_points = lattice.periodic(lattice.repetitions,neighbor_points)                     
                        str_neighbor_points = ' '.join(str(i) for i in neighbor_points)
                       

                        array2  = nn.all_array_list(str_neighbor_points)

                         #插入神经网络得到能量
                        energyB = 2
                        Rate_total_list[i[0]] = math.exp((energyA-energyB)/data.temp)
   
        
            Rate_list = []

            i = 0.0
            for c in Rate_total_list:         #速率界限
                
                i = i+c
                Rate_list.append(i)
            
            Rate_total_sum = sum(i for i in Rate_total_list)
        
            dtime = 1.0/Rate_total_sum
          
        
            number = random.uniform(0,1)
            
            select_number = number*Rate_total_sum
                     
            for i in range(8):
                if select_number <= Rate_list[i]:
                    select_path = i                 #选择路径
                    break
            

            vac_inv = vac + data.neighbor1[select_path][1]       #要跳跃的点
            
            vac_inv=lattice.periodic(lattice.repetitions,vac_inv)

            # print(vac_inv)      #[9.5 0.5 0.5]
            str_vac_inv =' '.join(str(i) for i in vac_inv)

            #更新空位
            temp = lattice.index_types.get(str_vac_inv)
            lattice.index_types[str_vac_inv] = lattice.index_types.get(str_vac)
            lattice.index_types[str_vac] = temp
                    
            vac =  str_vac_inv    

            #vac 转化成矩阵
            vac=vac.split(' ') 
            vac = np.array([float(vac[0]),float(vac[1]),float(vac[2])])   
            
            time = time+dtime

            #每10w输出
        #     if h%100000==0:

        #         deal = DealCluster(index_types=lattice.index_types)      
        #         with open('./lb.txt',"a+") as f:
                    
        #             str2 = str(deal.figure_num_x)+str(deal.figure_num_y)
        #             f.write(str2+'\n')
        #         if h%1000000==0:
        #             Lattice.figure(lattice.index_types,h)
        # total_time = time/(6*math.pow(10,12))

        return lattice.index_types