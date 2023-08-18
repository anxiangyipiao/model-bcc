
de1_CuCu = -0.414
de1_CuFe = -0.480
de1_CuV = -0.102
de1_FeV = -0.163
de2_CuCu = -0.611
de2_CuFe = -0.571
de2_CuV = -0.180
de2_FeV = -0.163
de1_FeFe = -0.611
de2_FeFe = -0.611

texp_vcu_list= {}
texp_vfe_list = {}

for j in range(-6,7):
        for i in range(-8,9):
                
                
            tde_vcu  = (i-1)*de1_CuCu - (i-1)*de1_CuFe - (i-1)*de1_CuV + (i-1)*de1_FeV+\
                    (j-1)*de2_CuCu - (j-1)*de2_CuFe - (j-1)*de2_CuV + (j-1)*de2_FeV

            tde_vfe = -i*de1_FeFe+i*de1_FeV+i*de1_CuFe-i*de1_CuV+\
                            -j*de2_FeFe+j*de2_FeV+j*de2_CuFe-j*de2_CuV
            


            key = str(i)+' '+str(j)
            texp_vcu_list[key] = tde_vcu
            texp_vfe_list[key] = tde_vfe


# for key,value in texp_vcu_list.items():
print(texp_vcu_list,texp_vfe_list)