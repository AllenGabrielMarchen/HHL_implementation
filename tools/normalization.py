import numpy as np

#양자 회로를 통해서 얻어진 결과(dictionary)를 통해서 normalize된 결과 벡터 x를 구하는 함수
def normalize_vector(answer, nb):
    #nb register에서 얻어질 수 있는 상태들을 dictionary의 key의 형태로 만들어 저장한다.
    possible_states = []
    for s in range(2**(nb)):
        possible_states.append(format(s, "b").zfill(nb))
    #print(answer)
    #flag register를 측정한 결과가 1이 나온 경우에 대해서 nb register의 결과를 순서대로 추가한다.
    available_result = []
    for i in possible_states:
        for key in answer.keys():
        
            if key[0:2] == i:
                if int(key[-1]) == 1:
                    available_result.append(answer[key])
                else:
                    pass
            else:
                pass
    #확률 분포를 상태 벡터의 형식으로 바꾸기 위해서 제곱근을 취한다.
    available_result = np.sqrt(np.array(available_result))
    #벡터의 크기가 1이 되도록 normalize해준다.
    normalized_result = available_result/np.linalg.norm(available_result)
    return normalized_result