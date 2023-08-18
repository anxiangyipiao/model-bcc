
from maincore.core import Read_Data,Lattice,Calcualte,Fcc_Start,Deal,Read_fcc_data
import numpy as np


def run():

    #读取文件
    path = "./data/fcc.txt"
    data = Read_fcc_data.Read_Data(path=path)

    ns_x,ns_y,ns_z,nstep,partition= \
    data.ns_X,data.ns_Y,data.ns_Z,data.nstep,data.partition
    
    # texp_es_vfe,texp_es_vcu = data.texp_es_vfe,data.texp_es_vcu
    # texp_vcu_list,texp_vfe_list=data.Fcc_Del_enerage()

    neighbor1,neighbor2 = data.fcc_neighbor1,data.fcc_neighbor2

    #构建模型
    cell_vectors = 2.78*np.eye(3,dtype=float)
    basis_points = np.array([[   0.000000e+00,   0.000000e+00,   0.000000e+00],
                            [   5.000000e-01,   5.000000e-01,   0.000000e+00],
                            [   5.000000e-01,   0.000000e+00,   5.000000e-01],
                            [   0.000000e+00,   5.000000e-01,   5.000000e-01]],dtype=float)
    
    lattice = Lattice.Lattice(
        cell_vectors=cell_vectors,
        basis_points=basis_points,
        repetitions=(ns_x,ns_y,ns_z),
        partition = partition
    )
    
    deal0 = Deal.Deal(
           index_types=lattice.index_types,
           )
    print(deal0.figure_num_x,deal0.figure_num_y)
    # print(lattice.index_types)    #dict类型      '0.0 0.0 0.0': 'V'
    # lattice.figure(lattice.index_types)

    nn = Calcualte.Calculate(
        lattice=lattice,
        neighbor1=neighbor1,
        neighbor2=neighbor2,
    )

    # nn1,nn2 = nn.nn1,nn.nn2

    
    start = Fcc_Start.Start(
        nstep=nstep,
        nn = nn,
        data = data,
        lattice = lattice,
    )

    # print(start.time,start.index_types)
    # start.save(start,data,lattice)
    # deal = Deal.Deal(
    #        index_types=start.index_types)

    # print(deal.figure_num_x,deal.figure_num_y)



if __name__=='__main__':
    run()
