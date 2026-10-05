#!/usr/bin/env python3
"""Genera programa1.script (URScript) para dibujar iniciales.
Uso: python3 gen_initials.py "JP" "MG" "AR"   (una cadena por integrante: Nombre+Apellido)"""
import sys

# Letras en una cuadricula de 2 (ancho) x 4 (alto). Cada letra = lista de trazos.
L = {
 'A': [[(0,0),(1,4),(2,0)], [(.5,1.6),(1.5,1.6)]],
 'B': [[(0,0),(0,4),(1.4,4),(1.8,3.6),(1.8,2.4),(1.4,2),(0,2)],
       [(1.4,2),(2,1.6),(2,.4),(1.6,0),(0,0)]],
 'C': [[(2,3.4),(1.6,4),(.4,4),(0,3.4),(0,.6),(.4,0),(1.6,0),(2,.6)]],
 'D': [[(0,0),(0,4),(1.3,4),(2,3.2),(2,.8),(1.3,0),(0,0)]],
 'E': [[(2,4),(0,4),(0,0),(2,0)], [(0,2),(1.5,2)]],
 'F': [[(2,4),(0,4),(0,0)], [(0,2),(1.5,2)]],
 'G': [[(2,3.4),(1.6,4),(.4,4),(0,3.4),(0,.6),(.4,0),(1.6,0),(2,.6),(2,2),(1,2)]],
 'H': [[(0,0),(0,4)], [(2,0),(2,4)], [(0,2),(2,2)]],
 'I': [[(.3,4),(1.7,4)], [(1,4),(1,0)], [(.3,0),(1.7,0)]],
 'J': [[(.3,4),(2,4)], [(1.5,4),(1.5,.6),(1.1,0),(.4,0),(0,.6)]],
 'K': [[(0,0),(0,4)], [(2,4),(0,1.8)], [(.6,2.5),(2,0)]],
 'L': [[(0,4),(0,0),(2,0)]],
 'M': [[(0,0),(0,4),(1,2),(2,4),(2,0)]],
 'N': [[(0,0),(0,4),(2,0),(2,4)]],
 'O': [[(.4,0),(0,.6),(0,3.4),(.4,4),(1.6,4),(2,3.4),(2,.6),(1.6,0),(.4,0)]],
 'P': [[(0,0),(0,4),(1.5,4),(2,3.5),(2,2.5),(1.5,2),(0,2)]],
 'Q': [[(.4,0),(0,.6),(0,3.4),(.4,4),(1.6,4),(2,3.4),(2,.6),(1.6,0),(.4,0)], [(1.2,1),(2,0)]],
 'R': [[(0,0),(0,4),(1.5,4),(2,3.5),(2,2.5),(1.5,2),(0,2)], [(1,2),(2,0)]],
 'S': [[(2,3.4),(1.6,4),(.4,4),(0,3.4),(0,2.6),(.4,2),(1.6,2),(2,1.4),(2,.6),(1.6,0),(.4,0),(0,.6)]],
 'T': [[(0,4),(2,4)], [(1,4),(1,0)]],
 'U': [[(0,4),(0,.6),(.4,0),(1.6,0),(2,.6),(2,4)]],
 'V': [[(0,4),(1,0),(2,4)]],
 'W': [[(0,4),(.5,0),(1,2.5),(1.5,0),(2,4)]],
 'X': [[(0,0),(2,4)], [(0,4),(2,0)]],
 'Y': [[(0,4),(1,2),(2,4)], [(1,2),(1,0)]],
 'Z': [[(0,4),(2,4),(0,0),(2,0)]],
}

# --- Parametros de area de trabajo (metros, en el marco base del robot) ---
S      = 0.025   # metros por unidad de cuadricula (letra = 0.05 x 0.10 m)
PITCH  = 0.09    # separacion entre letras
Y0     = 0.35    # distancia de la fila de letras
Z_DRAW = 0.20    # altura de la "mesa" donde se dibuja
Z_LIFT = 0.05    # cuanto sube el lapiz entre trazos
ROT    = "0.0,3.1416,0.0"   # herramienta apuntando hacia abajo

def P(x, y, z):
    return f"p[{x:.4f},{y:.4f},{z:.4f},{ROT}]"

def main(members):
    letters = [(i+1, c.upper()) for i, m in enumerate(members) for c in m if c.upper() in L]
    x0 = -(len(letters)-1) * PITCH / 2
    o = ["def programa1():",
         "  set_tcp(p[0,0,0,0,0,0])",
         "  movej([0.0,-1.5708,1.5708,-1.5708,-1.5708,0.0], a=1.0, v=0.5)"]
    first = True
    for n, (member, ch) in enumerate(letters):
        ox = x0 + n * PITCH
        o.append(f'  popup("Integrante {member}: se va a simular la letra {ch}", "Programa 1", False, False, True)')
        for stroke in L[ch]:
            pts = [(ox + x*S, Y0 + y*S) for x, y in stroke]
            ax, ay = pts[0]
            o.append(("  movej(" if first else "  movel(") + P(ax, ay, Z_DRAW+Z_LIFT) + ", a=1.0, v=0.4)")
            first = False
            for x, y in pts:
                o.append("  movel(" + P(x, y, Z_DRAW) + ", a=0.5, v=0.1)")
            ex, ey = pts[-1]
            o.append("  movel(" + P(ex, ey, Z_DRAW+Z_LIFT) + ", a=1.0, v=0.4)")
    o += ['  movej([0.0,-1.5708,1.5708,-1.5708,-1.5708,0.0], a=1.0, v=0.5)',
          '  popup("Trayectoria de iniciales finalizada", "Programa 1", False, False, True)',
          "end"]
    open("programa1.script", "w").write("\n".join(o) + "\n")
    print(f"Generado programa1.script con {len(letters)} letras")

if __name__ == "__main__":
    main(sys.argv[1:] or ["AB"])

