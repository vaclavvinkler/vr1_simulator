import numpy as np

def max_rod_flux_equation(grid, target_coords, external_source_flux, abs_c, B_T, alpha=2, mu=0.3):

    #grid: 2D list (seznam seznamů), kde každá hodnota je S_k nebo 0
    #target_coords: (i, j) souřadnice cílové tyče T
    #abs_c: koeficient absorbce
    #eta_c: koeficient absorpce kontrolní tyče
    #B_T: vlastní příspěvek dané tyče
    #phi_0: tok od zdroje
    #alpha: koeficient (vliv vzdálenosti a geometrie zóny)
    #mu: koeficient Exponenciální útlum vlivu (vliv stínění)



    phi_sum = 0
    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows):
        for j in range(cols):
            if (i, j) == target_coords:
                continue
            S_k = grid[i][j]
            if S_k == 0:
                continue
            # Vzdálenost mezi T a k
            r = np.sqrt((target_coords[0] - i)**2 + (target_coords[1] - j)**2)
            # Počet překážek: zjednodušeně počet tyčí mezi nimi v přímce
            n = abs(target_coords[0] - i) + abs(target_coords[1] - j)
            # Příspěvek od tyče k
            contribution = S_k * (abs_c) * (r ** -alpha) * np.exp(-mu * n)
            phi_sum += contribution


    return (B_T*abs_c + phi_sum + external_source_flux*abs_c)





