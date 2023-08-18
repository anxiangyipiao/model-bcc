import math



class Read_Data(object):
   
    def __init__(self,
                path=None ):

        with open("./"+path,"r+") as f:
                o_data = f.readlines()
        
        data_list = []

        for i in o_data:
            data = i.split(' ')[0]
            data_list.append(data)

        self.A = data_list[0]
        self.B = data_list[1]
        self.ns_X = int(data_list[2])
        self.ns_Y = int(data_list[3])
        self.ns_Z = int(data_list[4])
        self.nstep = int(data_list[5])
        self.tempk = float(data_list[6])
        self.temp = self.tempk/11604.9

        self.Es_vM =  float(data_list[7])
        self.Es_vG =  float(data_list[8])

        self.de1_GaGa= float(data_list[9])
        self.de2_GaGa= float(data_list[10])

        self.de1_MnGa= float(data_list[11])
        self.de2_MnGa= float(data_list[12])

        self.de1_GaV= float(data_list[13])
        self.de2_GaV= float(data_list[14])

        self.de1_MnMn= float(data_list[15])
        self.de2_MnMn= float(data_list[16])

        self.de1_MnV= float(data_list[17])
        self.de2_MnV= float(data_list[18])

        self.partition = float(data_list[19])

        # self.texp_es_vGa=float(math.exp(-self.Es_vG/self.temp))
        # self.texp_es_vMn=float(math.exp(-self.Es_vM/self.temp))

        
        self.fcc_texp_vMn_list,self.fcc_texp_vGa_list = self._Fcc_Del_enerage()
        
     
        self.fcc_neighbor1, self.fcc_neighbor2 = self._fcc_neighbor()


    def _Fcc_Del_enerage(self):

        texp_vMn_list= {}
        texp_vGa_list = {}
        # tde_vMn_list = {}
        # tde_vGa_list = {}

        for j in range(-6,7):
            for i in range(-12,13):
                tde_vMn  =  (i-1)*self.de1_MnMn - (i-1)*self.de1_MnGa + (i-1)*self.de1_GaV-(i-1)*self.de1_MnV+\
                              (j-1)*self.de2_MnMn - (j-1)*self.de2_MnGa + (j-1)*self.de2_GaV - (j-1)*self.de2_MnV
                tde_vGa = i*self.de1_MnGa - i*self.de1_GaGa + i*self.de1_GaV - i*self.de1_MnV +\
                              j*self.de2_MnGa - j*self.de2_GaGa + j*self.de2_GaV - j*self.de2_MnV
                
                key = str(i)+' '+str(j)
                
                dltleE_Cu = self.Es_vM+tde_vMn/2
                texp_vMn = math.exp(-dltleE_Cu/self.temp)
                texp_vMn_list[key] = texp_vMn


                dltleE_Fe = self.Es_vG+tde_vGa/2
                texp_vGa = math.exp( -dltleE_Fe/self.temp)
                texp_vGa_list[key] = texp_vGa

        return texp_vMn_list,texp_vGa_list
   

    def _fcc_neighbor(self):
        
        coordinates_p1 = [0,[ 0.0, 0.5, 0.5]]     
        coordinates_p2 = [1,[ 0.0, 0.5, -0.5]]     
        coordinates_p3 = [2,[ 0.0, -0.5, 0.5]]     
        coordinates_p4 = [3,[ 0.0, -0.5,-0.5]]     
                                                        
        coordinates_p5 = [4,[ -0.5, 0.5, 0.0]]  
        coordinates_p6 = [5,[ -0.5, -0.5,  0.0]]  
        coordinates_p7 = [6,[ 0.5, 0.5,  0.0]]   
        coordinates_p8 = [7,[ 0.5, -0.5, 0.0]]   

        coordinates_p9 = [8,[ 0.5, 0.0, 0.5]]   
        coordinates_p10 = [9,[ 0.5,0.0, -0.5]]   
        coordinates_p11 = [10,[ -0.5,0.0, 0.5]]   
        coordinates_p12 = [11,[ -0.5,0.0, -0.5]]   
        neighbor1 = [coordinates_p1,coordinates_p2,coordinates_p3,coordinates_p4,coordinates_p5,
                    coordinates_p6,coordinates_p7,coordinates_p8,coordinates_p9
                    ,coordinates_p10,coordinates_p11,coordinates_p12]
        
        #第二邻近
        coordinates_q1 = [0,[1.0, 0.0, 0.0]]    #右
        coordinates_q2 = [1,[-1.0, 0.0, 0.0]]   #左
        coordinates_q3 = [2,[0.0, 1.0, 0.0]]    #前
        coordinates_q4 = [3,[0.0, -1.0, 0.0]]   #后
        coordinates_q5 = [4,[0.0, 0.0, 1.0]]    #上
        coordinates_q6 = [5,[0.0, 0.0, -1.0]]   #下
        neighbor2 = [coordinates_q1,coordinates_q2,coordinates_q3,
                    coordinates_q4,coordinates_q5,coordinates_q6]

        return neighbor1,neighbor2


  