def data_types():
    a = 2                  
    b = "liechka"             
    c = 2.28               
    d = True                
    e = [1, 2, 3]           
    f = {'hunnimod': 'liechka'}    
    g = (1, 2, 3)          
    h = {1, 2, 3}           
    
    types = [type(a).__name__, type(b).__name__, type(c).__name__, type(d).__name__,
             type(e).__name__, type(f).__name__, type(g).__name__, type(h).__name__]
    print(f"[{', '.join(types)}]")

if __name__ == '__main__':
    data_types()