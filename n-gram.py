import pandas as pd
from androguard.misc import AnalyzeAPK
from collections import defaultdict
from tqdm import tqdm
import os

def list_opcode(dx,n_gram):
    list_opcode_set=defaultdict(int)
    for method in dx.get_methods():
        if method.is_external():
            continue
        m = method.get_method()
        tmp_str = ""
        for idx, ins in m.get_instructions_idx():
            tmp_str+=format(ins.get_op_value(),"02x")
        
        if (len(tmp_str)> 2*n_gram):
            continue
        list_opcode_set[tmp_str]+=1
        
    if '' in list_opcode_set:
        del list_opcode_set['']
    
    return list_opcode_set

if __name__=="__main__":
    #SETTING
    APK_DIRECTORY = "./TESTS/"
    LABEL = 0
    n_gram = 5
    
    
    #초기 값
    df = pd.DataFrame()
    list_apk = os.listdir(APK_DIRECTORY)

    #opcode 데이터 수집    
    for apk in tqdm(list_apk):
        try:
            apk = APK_DIRECTORY+apk
            a,d,dx = AnalyzeAPK(apk)
            list = list_opcode(dx,n_gram)
            list = {**{"label":LABEL},**list}
            tmp_df = pd.DataFrame.from_dict([list])
            df = pd.concat([df,tmp_df],axis=0).fillna(0)
            
        except:
            print("\nfail")
            
    print("done")
    df.astype(int).to_csv("./n-gram_result.csv",index=False)
    
