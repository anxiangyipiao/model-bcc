import numpy as np
import math


class DealCluster(object):

    def __init__(self,
                index_types = None,
            
                ) -> None:
        
        list_b=self.pass_b(index_types)

        new_list = self.dis_b(list_b)      #[[array([0.5, 1.5, 1.5]), 'B', [array([0.5, 4.5, 1.5]), 9.0], [array([1., 3., 4.]), 8.75]

        num_list = self.find_cluster(new_list)

        self.figure_num_x,self.figure_num_y=self.figures_num(num_list)


    def pass_b(self,index_types):

        list_b = []
        for key,value in index_types.items():

            if value == 'B':
                #vac 转化成矩阵
                a=key.split(' ') 
                key = np.array([float(a[0]),float(a[1]),float(a[2])])   
                item = [key,value]
                list_b.append(item)
        
        return list_b


    def dis_b(self,list_b):

        # list_r = list(reversed(list_b))
        new_list = []
        
        for i in list_b:
            dis = []

            for j in list_b:
                

                flag = (i[0] == j[0]).all()     #true

                if not flag:

                    distant = math.pow((i[0][0]-j[0][0]),2) + math.pow ((i[0][1]-j[0][1]),2) + math.pow((i[0][2]-j[0][2]),2)

                    dis.append([j[0],distant])
                # else:
                #     break
            i = i + [dis]
            new_list.append(i)

        return new_list


    def deep(self,new_list,item,cluster):
        
                distant = 0.75
            
        # for item in new_list:
        #     if all(j[0]==item[0]):
                item[1] = 'A'      #这里查询过了，下次跳过
                for k in item[2]:

                    if k[1] <= distant:       #寻找到点

                        for point in new_list:       #判断这个点是否被访问过
                            if all(k[0]==point[0]): 
                                if point[1]=="B": 
                    
                                    cluster +=1
                        
                                    cluster=self.deep(new_list,point,cluster)            
                                    
                    

                return cluster


    def find_cluster(self,new_list):
        
        # 距离
        distant = 0.75
        #簇个数列表
        num_list =[]
    
        for i in new_list: 
            # print(i)     #所有循环
            if i[1] == 'B':
                
                i[1] = "A"
                cluster = 1        #簇的大小
                for j in i[2]:     #单独一个循环

                    if j[1] <= distant:        #第一次

                        for item in new_list:       #判断这个点是否被访问过
                            if all(j[0]==item[0]): 
                                if item[1]=="B": 

                                        cluster +=1
                                        cluster = self.deep(new_list,item,cluster)
                        
                        
                
                num_list.append(cluster) 
                
        return num_list


    def figures_num(self,num_list):
        

        num_list.sort()       #sort


        num_lable = list(set(num_list))
        num_lable.sort()

        
        # print(num_lable,num_list)

        dict={}

        for j in num_lable:       #标签
            num1 = 0
            for i in num_list:      #个数

                if i == j :
                    num1 +=1
            
            dict[j] = num1

        x = []
        y = []
        for key,value in dict.items():
            x.append(key)
            y.append(value)

        # y=list(dict.values())
        # x = num_lable
        
        # print(x,y)
        return x,y

    
   