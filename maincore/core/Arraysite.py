import numpy as np
from . import Lattice


class Arraysite(object):

    def __init__(self,
                lattice=None,
                neighbor1=None,
                neighbor2=None,
                nlist=None,     ) -> None:
        

        self.repetitions = lattice.repetitions
        self.nlist = nlist
        self.neighbor1 = neighbor1
        self.neighbor2 = neighbor2
        self.index_types = lattice.index_types
        self.dis = [1,2]

        self.F = self._calF()
        self.arrayA = self._calarrayA()

    # 计算F
    def _calF(self):
        
        F = {}
        for r in self.dis:
            for j, value in enumerate(self.nlist):
                key = (r, j)  # 使用元组将 r 和 j 组合成一个键
                result = np.prod(np.exp(-((r / value[0]) ** value[1])))
                F[key] = result

        return  F
          

    #r 不变的 矩阵
    def _calarrayA(self):

        num_rows = len(self.nlist)
        num_cols = 14

        # 生成全0矩阵
        arrayA_matrix = np.zeros((num_rows, num_cols))

        for i in range(num_rows):
            for j in range(num_cols):
                r = 1
                if j > 7:
                     r = 2

                arrayA_matrix[i, j] = self.F[r,i]

        return arrayA_matrix

    # 类型矩阵
    #Fe原子类型： [1, 0, 0]           1
    #Cu原子类型： [0, 1, 0]           2
    #空位原子类型：[0, 0, 1]           0
    def find_array_list(self,asite):

            num_rows = 14
            num_cols = 3

            # 生成全0矩阵
            arrayB_matrix = np.zeros((num_rows, num_cols))

            #搜索asite附近邻近的点
            for i in self.neighbor1: 
                
                #处理key
                a=asite.split(' ')   #['0.0', '0.0', '0.0']
                add_key = [float(a[0]),float(a[1]),float(a[2])]
                neighbor_points = np.array(add_key)+i[1]

                neighbor_points = Lattice.Lattice.periodic(self.repetitions,neighbor_points)
               
                str_neighbor_points = ' '.join(str(i) for i in neighbor_points)

                if self.index_types[str_neighbor_points] == 0:
                     arrayB_matrix[i[0],:] = np.array([0, 0, 1])
                if self.index_types[str_neighbor_points] == 1:
                     arrayB_matrix[i[0],:] = np.array([1, 0, 0])
                if self.index_types[str_neighbor_points] == 2: 
                     arrayB_matrix[i[0],:] = np.array([0, 1, 0])
                             
            for i in self.neighbor2: 
                 
                #处理key
                a=asite.split(' ')   #['0.0', '0.0', '0.0']
                add_key = [float(a[0]),float(a[1]),float(a[2])]
                neighbor_points = np.array(add_key)+i[1]

                neighbor_points = Lattice.Lattice.periodic(self.repetitions,neighbor_points)
               
                str_neighbor_points = ' '.join(str(i) for i in neighbor_points)
                             
                if self.index_types[str_neighbor_points] == 0:
                     arrayB_matrix[i[0]+8,:] = np.array([0, 0, 1])
                if self.index_types[str_neighbor_points] == 1:
                     arrayB_matrix[i[0]+8,:] = np.array([1, 0, 0])
                if self.index_types[str_neighbor_points] == 2: 
                     arrayB_matrix[i[0]+8,:] =  np.array([0, 1, 0])       
                
               # arrayB_matrix[i[0]+8,0] = self.index_types[str_neighbor_points]


            return  arrayB_matrix
    

    def each_array_list(self,asite):

        
        arrayB = self.find_array_list(asite)

        eacharray =  np.dot(self.arrayA, arrayB)

        return eacharray
    


    def all_array_list(self,asite):


        num_rows = len(self.nlist)
        num_cols = len(self.nlist)
        num_layers = 14
        # 生成全0矩阵
        all_matrix = np.zeros((num_layers,num_rows, num_cols))


        for i in self.neighbor1: 
                
                #处理key
                a=asite.split(' ')   #['0.0', '0.0', '0.0']
                add_key = [float(a[0]),float(a[1]),float(a[2])]
                neighbor_points = np.array(add_key)+i[1]

                neighbor_points = Lattice.Lattice.periodic(self.repetitions,neighbor_points)
               
                str_neighbor_points = ' '.join(str(i) for i in neighbor_points)
                             
                all_matrix[i[0]:i[0]+1,:,:] = self.each_array_list(str_neighbor_points)
                                
        for i in self.neighbor2: 
                 
                #处理key
                a=asite.split(' ')   #['0.0', '0.0', '0.0']
                add_key = [float(a[0]),float(a[1]),float(a[2])]
                neighbor_points = np.array(add_key)+i[1]

                neighbor_points = Lattice.Lattice.periodic(self.repetitions,neighbor_points)
               
                str_neighbor_points = ' '.join(str(i) for i in neighbor_points)
                             
                all_matrix[i[0]+8:i[0]+9,:,:] = self.each_array_list(str_neighbor_points)


        return all_matrix
