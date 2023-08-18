from maincore.core import Read_Data,Lattice,Calcualte,Start,Deal,Arraysite,Ann
import numpy as np

def run():

    #读取文件
    path = "./data/data.txt"
    data = Read_Data.Read_Data(path=path)

    ns_x,ns_y,ns_z,nstep,partition= \
    data.ns_X,data.ns_Y,data.ns_Z,data.nstep,data.partition
    neighbor1,neighbor2 = data.neighbor1,data.neighbor2


    #构建模型
    cell_vectors = 2.78*np.eye(3,dtype=float)
    basis_points = np.array([[0,0,0],[0.5,0.5,0.5]],dtype=float)
    
    lattice = Lattice.Lattice(
        cell_vectors=cell_vectors,
        basis_points=basis_points,
        repetitions=(ns_x,ns_y,ns_z),
        partition = partition
    )
    
    # print(lattice.index_types)    #dict类型      '0.0 0.0 0.0': 2

    nlist_values = [(2.0, 0.5), (1.5, 0.3), (3.0, 0.7)]

    nn = Arraysite.Arraysite(
        lattice=lattice,
        neighbor1=neighbor1,
        neighbor2=neighbor2,
        nlist= nlist_values
    )

    #print(nn.arrayA) 
    print(nn.find_array_list("5 5 5"))
    # print(nn.each_array_list(site))
    # print(nn.all_array_list(site))
    # start = Ann.AnnStart(
    #     nstep=nstep,
    #     nn = nn,
    #     data = data,
    #     lattice = lattice
    # )





    # nn = Calcualte.Calculate(
    #     lattice=lattice,
    #     neighbor1=neighbor1,
    #     neighbor2=neighbor2,
    # )

    
    #开始
    # start = Start.Start(
    #     nstep=nstep,
    #     nn = nn,
    #     data = data,
    #     lattice = lattice
    # )
    


if __name__=='__main__':
    run()




