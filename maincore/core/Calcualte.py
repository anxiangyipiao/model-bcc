import numpy as np
import math
from . import Lattice

class Calculate(object):

    def __init__(self,
                lattice=None,
                neighbor1=None,
                neighbor2=None,     ) -> None:
        
        self.repetitions = lattice.repetitions
        self.nn1 = self._find_nn1_list(lattice.index_types,neighbor1)
        self.nn2 = self._find_nn2_list(lattice.index_types,neighbor2)

  
    def _find_nn1_list(self,index_types,neighbor1):
        
        nn1 = {}
        
        #找到所有点的第一邻近 

        for key in index_types.keys():
            
            number1 = 0       #B的数量
            
            #搜索附近邻近的点
            for i in neighbor1: 
                
                #处理key
                a=key.split(' ')   #['0.0', '0.0', '0.0']
                add_key = [float(a[0]),float(a[1]),float(a[2])]
                neighbor_points = np.array(add_key)+i[1]

                neighbor_points = Lattice.Lattice.periodic(self.repetitions,neighbor_points)
               
                # for j in index_types:              #耗时
                #     if all(neighbor_points == j[0]):
                        # print(j)    #[array([0., 3., 3.]), 36, 'B', 0]

                str_neighbor_points = ' '.join(str(i) for i in neighbor_points)
                            
                # if index_types.get(str_neighbor_points):
                if index_types[str_neighbor_points] == 'B':
                        number1 = number1 + 1
                        
            nn1[key] = number1
            

        return nn1

    def _find_nn2_list(self,index_types,neighbor2):
       
        nn2 = {}
         
        for key in index_types.keys():
            
            number2 = 0       #B的数量
            
            for i in neighbor2:
               
                a=key.split(' ') 
                add_key = [float(a[0]),float(a[1]),float(a[2])]    
                neighbor_points = np.array(add_key)+i[1]
                neighbor_points = Lattice.Lattice.periodic(self.repetitions,neighbor_points)
                  
                str_neighbor_points = ' '.join(str(i) for i in neighbor_points)

                # if index_types.get(str_neighbor_points):
                if index_types[str_neighbor_points] == 'B':
                        number2  = number2 + 1
                        
            nn2[key] = number2
            

        return nn2

    @staticmethod
    def find_nn1(vac,neighbor_points,nn1):
    
        # vac_nn = 0
        # inv_nn = 0
        
        vac_nn=nn1.get(vac)
                
        inv_nn=nn1.get(neighbor_points)
                    
        dn1 = vac_nn - inv_nn
        
        return dn1
    
    @staticmethod
    def find_nn2(vac,neighbor_points,nn2):
        # vac_nn = 0
        # inv_nn = 0
        
        vac_nn=nn2.get(vac)
                
        inv_nn=nn2.get(neighbor_points)

        dn2 = vac_nn - inv_nn
       
        return dn2


    def find_tde_vcu(self,dn1,dn2,tde_vcu):


        for key,value in tde_vcu.items():

            d=key.split(' ')

            if dn1 == int(d[0]) and dn2 == int(d[1]):
                 
                    return value