#encoding: utf-8
import numpy as np
import random
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


class Lattice(object):
    
    def __init__(self,
                cell_vectors=None,
                basis_points=None,
                repetitions=None,
                partition=None,
                ) -> None:
        
        #生成坐标
        self.cell_vectors=cell_vectors
        self.basis = basis_points
        self.repetitions=repetitions
        self.sites = self.__generateLatticeSites()
        
        #生成类型
        self.number_a =0
        self.number_b =0
        self.types,self.a,self.b = self._type(repetitions,partition,self.basis)

        #生成模型
        self.index_types =self._make_globle_dict(self.types,self.sites)

    #生成坐标
    def __generateLatticeSites(self):
        
        # Get the basis out of the unit cell.  得到basis点
        basis = self.basis

        # Loop through all repetitions and insert the sites.循环遍历所有的重复并插入站点
        sites = []         #列表
        for i in range(self.repetitions[0]):
            for j in range(self.repetitions[1]):
                for k in range(self.repetitions[2]):

                    # for b in range(len(basis)):

                    #     site = [i,j,k,b]
                    #     sites.append(site)
                    # For each point in the basis, add the translation
                    translation = np.array([i,j,k])
                    for b in basis:
                        site = b+translation
                        sites.append(site)
        
        # sites = sites.tolist()
        # Return the data.         返回矩阵
        return sites

    #生成类型
    def _type(self,repetitions,partiton,basis):
        
        types = []
        number_a =0
        number_b =0
        a = repetitions[0]
        b = repetitions[1]
        c = repetitions[2]
        d = len(basis)
        
        for i in range(a):
            for j in range(b):
                for k in range(c):
                    for m in range(d):
                        if random.uniform(0,1)>partiton:
                            number_a+=1
                            types += [1]
                        else:
                            number_b+=1
                            types += [2]
    #    设置一个空位
        types[0] = 0   

        return types,number_a,number_b

    # #生成模型
    def _make_globle_dict(self,types,sites):
        

        index_types = {}
        
        for n,item in enumerate(sites):
            
            # print(item)
            strkey = ' '.join(str(i) for i in item)

           
            # item = str(item[0])+' '+str(item[1])+' '+str(item[2])
            # # item = str(item)
            
            index_types[strkey] = types[n]


        return index_types


    @staticmethod
    def periodic(repetitions,neighbor):
        
        # print(neighbor)
        if neighbor[0]<0 :
            neighbor[0]=neighbor[0]+repetitions[0]
        if neighbor[1]<0:
            neighbor[1]=neighbor[1]+repetitions[1]
        if neighbor[2]<0:
            neighbor[2]=neighbor[2]+repetitions[2]
       
        if neighbor[0]>=repetitions[0]:
            neighbor[0]=neighbor[0]-repetitions[0]
        if neighbor[1]>=repetitions[1]:
            neighbor[1]=neighbor[1]-repetitions[1]
        if neighbor[2]>=repetitions[2]:
            neighbor[2]=neighbor[2]-repetitions[2]


        return np.array(neighbor)

   
    @staticmethod
    def figure(types,num):
            
          
            fig = plt.figure()           
            ax = plt.axes(projection='3d')         

            for key,value in types.items():
               
                a=key.split(' ') 
                if value == 'A':
                    # color = 'r'
                    # ax.scatter3D(float(a[0]),float(a[1]),float(a[2]), c = color)
                    continue
                elif value == 'B':
                    color = 'g'
                    ax.scatter3D(float(a[0]),float(a[1]),float(a[2]), c = color)
                   
                else:
                    color = 'b'
                    ax.scatter3D(float(a[0]),float(a[1]),float(a[2]), c = color)
                    

            
            ax.set_xlabel('X')  # 设置x坐标轴
            ax.set_ylabel('Y')  # 设置y坐标轴
            ax.set_zlabel('Z')  # 设置z坐标轴
            
            # plt.show()
            plt.savefig(str(num)+".png")