#tdvals = [1.1]
#tbetavals = [0.05, 0.07] 
tdvals = [0.001, 0.5, 0.6, 0.7, 0.8, 0.9]
tbetavals = [0.10] 
for td in tdvals:
    for tbeta in tbetavals:
        dc_templ_file = open("./spvcnn_config_Feb14_PFtarget_weighted_WITHPU_TEMPLATE.yaml")
        dc_file = open("./yaml_files_Feb14_PFtarget_weighted_WITHPU/spvcnn_config_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0)))+"_ttbar.yaml","w")
        for line in dc_templ_file:
            line=line.replace('TDVAL', str(td))
            line=line.replace('TBETAVAL', str(tbeta))
            dc_file.write(line)
        dc_file.close()
        dc_templ_file.close()
