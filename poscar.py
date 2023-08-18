import os
import random
import numpy as np


#coff  Cu 所占的比例
class Type(object):

    def __init__(self,
                 coff=None) -> None:
     
        #Fe原子类型： [1, 0, 0]           
        #Cu原子类型： [0, 1, 0]           
        #空位原子类型：[0, 0, 1]   
        
        coordinates_p1 = [0,[-0.5, 0.5, 0.5]]     #左上
        coordinates_p2 = [1,[ 0.5, 0.5, 0.5]]     #右下
        coordinates_p3 = [2,[-0.5, 0.5,-0.5]]     #左下
        coordinates_p4 = [3,[ 0.5, 0.5,-0.5]]     #左下
                                                                    #后
        coordinates_p5 = [4,[ -0.5, -0.5, -0.5]]  #左上
        coordinates_p6 = [5,[ -0.5, -0.5,  0.5]]  #左下
        coordinates_p7 = [6,[ 0.5, -0.5,  0.5]]   #右下
        coordinates_p8 = [7,[ 0.5, -0.5, -0.5]]   #右下
        self.neighbor1 = [coordinates_p1,coordinates_p2,coordinates_p3,coordinates_p4,coordinates_p5,
                coordinates_p6,coordinates_p7,coordinates_p8]
                
        #第二邻近
        coordinates_q1 = [0,[1.0, 0.0, 0.0]]    #右
        coordinates_q2 = [1,[-1.0, 0.0, 0.0]]   #左
        coordinates_q3 = [2,[0.0, 1.0, 0.0]]    #前
        coordinates_q4 = [3,[0.0, -1.0, 0.0]]   #后
        coordinates_q5 = [4,[0.0, 0.0, 1.0]]    #上
        coordinates_q6 = [5,[0.0, 0.0, -1.0]]   #下
        self.neighbor2 = [coordinates_q1,coordinates_q2,coordinates_q3,
                            coordinates_q4,coordinates_q5,coordinates_q6]
        
        self.coff = coff
        self.sites = self._calsite()
        self.vacs = self._calvacs()
        self.types = self._caltype()
        self.index_types = self._gensite()

    def _calsite(self):

        basis_points = np.array([[0,0,0],[0.5,0.5,0.5]],dtype=float)
        ##坐标
        sites = []
        for i in range(4):
                for j in range(4):
                        for k in range(4):

                            # for b in range(len(basis)):

                            #     site = [i,j,k,b]
                            #     sites.append(site)
                            # For each point in the basis, add the translation
                            translation = np.array([i,j,k])
                            for b in basis_points:

                                site = b+translation

                                sites.append(site)

        return sites
    

    def _calvacs(self):
         
        #vac type 类型位置
        #中心点是 2，2，2 等
        vac = np.array([2.0,2.0,2.0])  
        vacs = []
        vacs.append(vac)
        for i in self.neighbor1:
            neighbor_point = vac+i[1]
            vacs.append(neighbor_point)

        return vacs
    

    def _caltype(self):
         
    #从任一vacs选择一个构建POSCAR

        types = []             
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    for m in range(2):
                            if random.uniform(0,1)>self.coff:
                                    types += [1]
                            else: 
                                    types += [2]

        return types
    
    def _gensite(self):
         
        index_types = {}
                
        for n,item in enumerate(self.sites):
                    
            strkey = ' '.join(str(i) for i in item)     
            index_types[strkey] =self.types[n]

        randoma = random.randint(0,len(self.vacs)-1)
        vaca = self.vacs[randoma]
        vackey = ' '.join(str(i) for i in vaca)     
        index_types[vackey] = 0

        return  index_types

#第二步
#输出矩阵
class Arraysite(object):

    def __init__(self,
                lattice=None,
                neighbor1=None,
                neighbor2=None,
                nlist=None,
                ntype=None,
                coff = None,
                          ) -> None:
        

        self.nlist = nlist
        self.ntype = ntype
        self.neighbor1 = neighbor1
        self.neighbor2 = neighbor2
        self.index_types = lattice
        self.dis = [1*coff,2*coff]

        self.F = self._calF()
        self.arrayA = self._calarrayA()

        self.matrix = self.all_array_list("2 2 2")
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
                r = self.dis[0]
                if j > 7:
                     r = self.dis[1]

                arrayA_matrix[i, j] = self.F[r,i]

        return arrayA_matrix

    # 类型矩阵
    #Fe原子类型： [1, 0, 0]           1
    #Cu原子类型： [0, 1, 0]           2
    #空位原子类型：[0, 0, 1]          0
    def find_array_list(self,asite):

            num_rows = 14
            num_cols = self.ntype

            # 生成全0矩阵
            arrayB_matrix = np.zeros((num_rows, num_cols))

            #搜索asite附近邻近的点
            for i in self.neighbor1: 
                
                #处理key
                a=asite.split(' ')   #['0.0', '0.0', '0.0']
                add_key = [float(a[0]),float(a[1]),float(a[2])]
                neighbor_points = np.array(add_key)+i[1]
              
                str_neighbor_points = ' '.join(str(i) for i in neighbor_points)

                if self.index_types.get(str_neighbor_points) is None:
                     arrayB_matrix[i[0],:] = np.array([1, 0, 0])

                elif self.index_types[str_neighbor_points] == 0:
                     arrayB_matrix[i[0],:] = np.array([0, 0, 1])
                elif self.index_types[str_neighbor_points] == 1:
                     arrayB_matrix[i[0],:] = np.array([1, 0, 0])
                elif self.index_types[str_neighbor_points] == 2: 
                     arrayB_matrix[i[0],:] = np.array([0, 1, 0])
                
                                  
            for i in self.neighbor2: 
                 
                #处理key
                a=asite.split(' ')   #['0.0', '0.0', '0.0']
                add_key = [float(a[0]),float(a[1]),float(a[2])]
                neighbor_points = np.array(add_key)+i[1]
                   
                str_neighbor_points = ' '.join(str(i) for i in neighbor_points)

                if self.index_types.get(str_neighbor_points) is None:
                     arrayB_matrix[i[0],:] = np.array([1, 0, 0])

                elif self.index_types[str_neighbor_points] == 0:
                     arrayB_matrix[i[0]+8,:] = np.array([0, 0, 1])
                elif self.index_types[str_neighbor_points] == 1:
                     arrayB_matrix[i[0]+8,:] = np.array([1, 0, 0])
                elif self.index_types[str_neighbor_points] == 2: 
                     arrayB_matrix[i[0]+8,:] =  np.array([0, 1, 0])       
                
               # arrayB_matrix[i[0]+8,0] = self.index_types[str_neighbor_points]


            return  arrayB_matrix
    

    def each_array_list(self,asite):

        
        arrayB = self.find_array_list(asite)

        eacharray =  np.dot(self.arrayA, arrayB)

        return eacharray
    


    def all_array_list(self,asite):


        num_rows = len(self.nlist)
        # # 生成全0矩阵
        # all_matrix = np.zeros((num_rows, num_cols))
        num_cols = self.ntype
        num_layers = 14
        # 生成全0矩阵               14 * 3 * 3
        all_matrix = np.zeros((num_layers,num_rows, num_cols))


        for i in self.neighbor1: 
                
                #处理key
                a=asite.split(' ')   #['0.0', '0.0', '0.0']
                add_key = [float(a[0]),float(a[1]),float(a[2])]
                neighbor_points = np.array(add_key)+i[1]
               
                str_neighbor_points = ' '.join(str(i) for i in neighbor_points)
                             
                all_matrix[i[0]:i[0]+1,:,:] = self.each_array_list(str_neighbor_points)
                                
        for i in self.neighbor2: 
                 
                #处理key
                a=asite.split(' ')   #['0.0', '0.0', '0.0']
                add_key = [float(a[0]),float(a[1]),float(a[2])]
                neighbor_points = np.array(add_key)+i[1]
               
                str_neighbor_points = ' '.join(str(i) for i in neighbor_points)
                             
                all_matrix[i[0]+8:i[0]+9,:,:] = self.each_array_list(str_neighbor_points)


        return all_matrix
    

#配置Sets
class Sets(object):
    def __init__(self,
                 coff=None) -> None:
     
        # Generate the list of (p, q) sets,  like [(2.0, 0.5), (1.5, 0.3), (3.0, 0.7)]
        self.nlist_values = self._calsets()
    
    def _calsets(self):

         # Define the ranges and steps for p and q
        p_start, p_end, p_step = 4.2, 1.1, -0.1
        q_start, q_end, q_step = 1.85, 3.4, 0.05

        # Generate the list of (p, q) sets
        nlist_values = []
        p_value, q_value = p_start, q_start

        for _ in range(32):
            nlist_values.append((round(p_value, 2), round(q_value, 2)))
            q_value += q_step
            p_value += p_step

        return  nlist_values


#save
class SavePOSACR(object):
    
    def __init__(self,
                lattice=None,
                matrix = None,
                filename = None,
                filepath = None  ) -> None:

        # 示例数据
        self.filepath = filepath
        self.filename = filename
        self.matrix = matrix
        self.index_types = lattice
        self.lattice_vectors = [
            [11.4800000000000004, 0.0000000000000000, 0.0000000000000000],
            [0.0000000000000000, 11.4800000000000004, 0.0000000000000000],
            [0.0000000000000000, 0.0000000000000000, 11.4800000000000004]
        ]
        self.atom_symbols = ['Fe', 'Cu']

        self.Felist = []
        self.Culist = []
        for key,value in self.index_types.items():
                    
            #a=key.split(' ') 
            if value == 1:
                #Fe
                self.Felist.append(key)
            if value == 2:
                self.Culist.append(key)     

        self.merged_list = self.Felist + self.Culist

        self.save_poscar()


    def save_poscar(self):
        # 构建 POSCAR 文件内容
        poscar_data = "Fe\n"
        poscar_data += "1.0\n"
        for vector in  self.lattice_vectors:
            poscar_data += f"{vector[0]:.10f} {vector[1]:.10f} {vector[2]:.10f}\n"
        poscar_data += " ".join(self.atom_symbols) + "\n"
        poscar_data += str(len(self.Felist))+" "+str(len(self.Culist)) + "\n"
        poscar_data += "Cartesian\n"
        for atom_coord in self.merged_list:
            atom_coord_list = atom_coord.split(" ")

            # 将列表中的每个元素转换为浮点数，并乘以 2.87
            scaled_coords = [float(coord) * 2.87 for coord in atom_coord_list]
            scaled_coords = ' '.join(str(i) for i in  scaled_coords)  
            poscar_data += f"{scaled_coords}\n"

        # 将 POSCAR 数据写入文件
        homedir = os.getcwd()
        if not os.path.exists(homedir+"\\"+self.filepath):
            os.makedirs(homedir+"\\"+self.filepath)

        with open("./"+self.filepath+"/"+"POSCAR"+self.filename, 'w') as file:
            file.write(poscar_data)

        #将 矩阵 数据写入文件
        np.save("./"+self.filepath+"/"+"POSCAR"+self.filename + ".npy", self.matrix)



if __name__ == '__main__':
     
    #sets 配置 32组
    nlist = Sets()

    #Cu 比例
    for coffi in np.arange(0.01,0.9,0.5):
        
        coffi = round(coffi, 2)
        #lattice 类型
        types = Type(
            coff=coffi
        )

        #计算矩阵
        nn = Arraysite(
                lattice=types.index_types,
                neighbor1=types.neighbor1,
                neighbor2=types.neighbor2,
                nlist= nlist.nlist_values,
                ntype=3,
                coff=2.87
            )


        savenn = SavePOSACR(
              lattice=types.index_types,
              matrix= nn.matrix,
              filename=str(coffi),
              filepath = "test"
        )

