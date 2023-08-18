import numpy as np
import random
import math
# from mpi4py import MPI
from .Deal import DealCluster
from .Lattice import Lattice
# comm = MPI.COMM_WORLD
# comm_size = comm.Get_size()
# comm_rank = comm.Get_rank()





class Start(object):

    def __init__(self,
                 nstep=None,
                 nn = None,
                 data =None,
                 lattice =None,
                  ) -> None:
       
       
       self.time,self.index_types = self.start(nstep,data,nn,lattice)

        

    def start(self,nstep,data,nn,lattice):
      
        time =0.0
        vac = np.array([0.0,0.0,0.0])

        for h in range(nstep):

            Rate_total_list = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

           
            # vac_neighbor1_points=[]
            # if comm_rank == 0:               
            #     data = data.neighbor1
            # else:
            #     data = None

            #根据空位找到第一邻近的点
            for i in data.neighbor1:       
                        
                        neighbor_points = vac+i[1]
                        neighbor_points = lattice.periodic(lattice.repetitions,neighbor_points)                     
                        str_neighbor_points = ' '.join(str(i) for i in neighbor_points)
                        str_vac = ' '.join(str(i) for i in vac)
                    
                    # if lattice.index_types.get(str_neighbor_points):     #判断这个点是否存在
                    
                        dn1 = nn.find_nn1(str_vac,str_neighbor_points,nn.nn1)        #计算dn1
                    
                        dn2 = nn.find_nn2(str_vac,str_neighbor_points,nn.nn2)        #计算dn2

                        
                        if lattice.index_types.get(str_neighbor_points) == 'B':
                           
                                Rate_total_list[i[0]] = nn.find_tde_vcu(dn1,dn2,data.texp_vcu_list)      #结合能                         
                            #     Rate_total_list[i[0]] = 1.0
                        
                        elif lattice.index_types.get(str_neighbor_points) == 'A':
                            
                                Rate_total_list[i[0]] = nn.find_tde_vcu(dn1,dn2,data.texp_vfe_list)
                                            
                            #     Rate_total_list[i[0]] = 1.0
                          
            

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
            # str_vac_inv = str(vac_inv[0])+' '+str(vac_inv[1])+' '+str(vac_inv[2]) 
            
            
            #更新邻居和空位
            
            if lattice.index_types.get(str_vac_inv) == 'B':        
                
                        #要移动的点周围变化
                        for i in data.neighbor1:       
                            neighbor_points1 = vac_inv+i[1]
                            neighbor_points1=lattice.periodic(lattice.repetitions,neighbor_points1)
                            str_neighbor_points1 = ' '.join(str(i) for i in neighbor_points1)
                            # str_neighbor_points1 = str(neighbor_points1[0])+' '+str(neighbor_points1[1])+' '+str(neighbor_points1[2]) 

                            # if nn.nn1.get(str_neighbor_points1):
                            nn.nn1[str_neighbor_points1] = nn.nn1.get(str_neighbor_points1) - 1
                                
                                    
                        for i in data.neighbor2:
                            neighbor_points2 = vac_inv+i[1]
                            neighbor_points2=lattice.periodic(lattice.repetitions,neighbor_points2)
                            str_neighbor_points2 = ' '.join(str(i) for i in neighbor_points2)
                           
                            # if nn.nn2.get(str_neighbor_points2):
                            nn.nn2[str_neighbor_points2] = nn.nn2.get(str_neighbor_points2) - 1


                        #空位周围点的变化
                        for i in data.neighbor1:       
                            neighbor_points3 = vac+i[1]
                            neighbor_points3=lattice.periodic(lattice.repetitions,neighbor_points3)
                            str_neighbor_points3 = ' '.join(str(i) for i in neighbor_points3)
                            
                            # if nn.nn1.get(str_neighbor_points3):
                            nn.nn1[str_neighbor_points3] = nn.nn1.get(str_neighbor_points3) + 1

                        for i in data.neighbor2:       
                            neighbor_points4 = vac+i[1]
                            neighbor_points4=lattice.periodic(lattice.repetitions,neighbor_points4)
                            str_neighbor_points4 = ' '.join(str(i) for i in neighbor_points4)
                           
                            # if nn.nn2.get(str_neighbor_points4):
                            nn.nn2[str_neighbor_points4] = nn.nn2.get(str_neighbor_points4) + 1
                        

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
            if h%100000==0:

                deal = DealCluster(index_types=lattice.index_types)      
                with open('./lb.txt',"a+") as f:
                    
                    str2 = str(deal.figure_num_x)+str(deal.figure_num_y)
                    f.write(str2+'\n')
                if h%1000000==0:
                    Lattice.figure(lattice.index_types,h)
        total_time = time/(6*math.pow(10,12))

        return total_time,lattice.index_types

    @staticmethod
    def save(self,data,lattice):
        
        with open("./data/list.txt","a+") as f:
            f.write(data.A+"\n")
            f.write('\t2.78'+"\n")
            for i in lattice.cell_vectors:
                i = str(i).replace('[', ' ')
                i = str(i).replace(']', ' ')
                f.write('\t\t'+i+"\n")
            f.write(data.A+" ")
            f.write(data.B+"\n")
            f.write(str(lattice.a)+" ")
            f.write(str(lattice.b)+"\n")
            f.write('Direct'+'\n')
            
            for key,value in self.index_types.items():
                if value == "A":
                    f.write('\t'+key+'\n')
            for key,value in self.index_types.items():
                if value == "B":
                    f.write('\t'+key+'\n')