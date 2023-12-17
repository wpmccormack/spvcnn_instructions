import os, shutil


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else: raise
        
if __name__ == "__main__":
    
    #tdvals = [1.1]
    #tbetavals = [0.05, 0.07]
 
    #tdvals = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
    #tdvals = [0.8, 0.9, 1.0, 1.1, 1.2]
    #tdvals = [0.8, 0.9, 1.0]

    #tdvals = [0.3]
    #tbetavals = [0.08, 0.10] 

    #tdvals = [0.9, 1.0]
    #tdvals = [0.8, 0.9, 1.0]

    #tdvals = [0.3]
    #tbetavals = [0.08, 0.10] 

    #tdvals = [0.6, 0.7, 0.8]
    tdvals = [0.7]
    #tdvals = [0.5, 0.9]
    tbetavals = [0.10] 
    for td in tdvals:
        for tbeta in tbetavals:
            try:
                os.mkdir("./spvcnn_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0))))
            except:
                print("already here")
            dc_templ_file = open("../spvcnn_TEMPLATE_Feb14_PFtarget_weighted_WITHPU/config.pbtxt")
            dc_file = open("./spvcnn_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0)))+"/config.pbtxt", "w")
            for line in dc_templ_file:
                line=line.replace('NAMEVAL', "spvcnn_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0))))
                dc_file.write(line) 
            dc_file.close()
            dc_templ_file.close()
            try:
                os.mkdir("./spvcnn_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0)))+"/1")
            except:
                print("already have 1")
            dc_templ_file = open("../spvcnn_TEMPLATE_Feb14_PFtarget_weighted_WITHPU/1/model.py")
            dc_file = open("./spvcnn_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0)))+"/1/model.py", "w")
            for line in dc_templ_file:
                line=line.replace('SPVCNNCONFIG', "spvcnn_config_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0)))+"_ttbar")
                dc_file.write(line) 
            dc_file.close()
            dc_templ_file.close()
            #copyanything("./spvcnn_TEMPLATE", "./spvcnn_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0))))
            #print("./spvcnn_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0)))+"/config.pbtxt")
            #dc_file = open("./spvcnn_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0)))+"/config.pbtxt", "w")
            #for line in dc_file:
            #    line.replace('NAMEVAL', "spvcnn_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0))))
            #dc_file = open("./yaml_files/spvcnn_config_td_"+str(int(round(td*10,0)))+"_tbeta_"+str(int(round(tbeta*100,0)))+"_ttbar.yaml","w")
            #for line in dc_templ_file:
            #    line=line.replace('TDVAL', str(td))
            #line=line.replace('TBETAVAL', str(tbeta))
            #dc_file.write(line)
            #dc_file.close()
            #dc_templ_file.close()


            #spvcnn_config_td_11_tbeta_5_ttbar.yaml
