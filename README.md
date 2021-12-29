# WIP

vetores originais
v_x = [1,0]
v_y = [0,1]

vetores rodados
r_x = [r_x0, r_x1]
r_y = [r_y0, r_y1]


matrix de mudança de base - transforma vetores em [r_x, r_y] nas coordenadas originais
v_r = vetor na base rodada
v_r.M = v

M = [[m00,m01],
     [m10,m11]]
     
[r_x, . M = [v_x,
 r_y]        v_y]
 
 M = [v_x, v_y] . [r_x, r_y]^-1


matrix de rotacao transforma [1,0] em [1,0] rodado
eu quero agora uma matriz que transforme [1,0] nas coordenadas
