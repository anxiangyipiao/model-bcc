import math



class Read_Data(object):
   
    #读取初始数据
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

        self.Es_vFe =  float(data_list[7])
        self.Es_vCu =  float(data_list[8])

        self.de1_CuCu= float(data_list[9])
        self.de2_CuCu= float(data_list[10])
        self.de1_CuFe= float(data_list[11])
        self.de2_CuFe= float(data_list[12])
        self.de1_CuV= float(data_list[13])
        self.de2_CuV= float(data_list[14])
        self.de1_FeV= float(data_list[15])
        self.de2_FeV= float(data_list[16])
        self.de1_FeFe= float(data_list[17])
        self.de2_FeFe= float(data_list[18])

        self.partition = float(data_list[19])

        # self.texp_es_vfe=float(math.exp(-self.Es_vFe/self.temp))
        # self.texp_es_vcu=float(math.exp(-self.Es_vCu/self.temp))

        self.texp_vcu_list,self.texp_vfe_list= self._Del_enerage()
       
        self.neighbor1,self.neighbor2 = self.neighbor()
     
    #计算能量
    def _Del_enerage(self):

        texp_vcu_list= {}
        texp_vfe_list = {}
       
        for j in range(-6,7):
            for i in range(-8,9):
                
                tde_vcu  = (i-1)*self.de1_CuCu - (i-1)*self.de1_CuFe - (i-1)*self.de1_CuV + (i-1)*self.de1_FeV+\
                    (j-1)*self.de2_CuCu - (j-1)*self.de2_CuFe - (j-1)*self.de2_CuV + (j-1)*self.de2_FeV

                tde_vfe = -i*self.de1_FeFe+i*self.de1_FeV+i*self.de1_CuFe-i*self.de1_CuV+\
                            -j*self.de2_FeFe+j*self.de2_FeV+j*self.de2_CuFe-j*self.de2_CuV

                key = str(i)+' '+str(j)

                # if tde_vcu < 0:
                    
                #     texp_vcu_list[key] = self.texp_es_vcu

                # else:

                dltleE_Cu = self.Es_vCu+(tde_vcu/2)
                texp_vcu = math.exp(-dltleE_Cu/self.temp)
                texp_vcu_list[key] = texp_vcu
                    
                # if tde_vfe < 0 :
    
                #     texp_vfe_list[key] = self.texp_es_vfe

                # else:

                dltleE_Fe = self.Es_vFe+(tde_vfe/2)
                texp_vfe = math.exp( -dltleE_Fe/self.temp)
                texp_vfe_list[key] = texp_vfe


        return texp_vcu_list,texp_vfe_list

    #定义邻居坐标
    def neighbor(self):

        coordinates_p1 = [0,[-0.5, 0.5, 0.5]]     #左上
        coordinates_p2 = [1,[ 0.5, 0.5, 0.5]]     #右下
        coordinates_p3 = [2,[-0.5, 0.5,-0.5]]     #左下
        coordinates_p4 = [3,[ 0.5, 0.5,-0.5]]     #左下
                                                            #后
        coordinates_p5 = [4,[ -0.5, -0.5, -0.5]]  #左上
        coordinates_p6 = [5,[ -0.5, -0.5,  0.5]]  #左下
        coordinates_p7 = [6,[ 0.5, -0.5,  0.5]]   #右下
        coordinates_p8 = [7,[ 0.5, -0.5, -0.5]]   #右下
        neighbor1 = [coordinates_p1,coordinates_p2,coordinates_p3,coordinates_p4,coordinates_p5,
        coordinates_p6,coordinates_p7,coordinates_p8]
        
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

   
   