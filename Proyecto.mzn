%=============================================================================%
% Proyecto: Minimizar la Polarización en una Población
% Análisis de Algoritmos II - Universidad del Valle
% Autores: Andrey Quiceño, Iván, Francesco, Jonathan
% Fecha: Diciembre 2025
%=============================================================================%

%-----------------------------------------------------------------------------
% PARÁMETROS
%-----------------------------------------------------------------------------

% Número total de personas en la población
int: n;

% Número de opiniones posibles
int: m;

% Distribución inicial de personas por opinión
% p[i] = número de personas con opinión i
array[1..m] of int: p;

% Valores de las opiniones (en [0,1])
% v[i] = valor real de la opinión i
array[1..m] of float: v;

% Distribución de personas por opinión y nivel de resistencia
% s[i,k] = número de personas con opinión i y resistencia k
% k=1: baja, k=2: media, k=3: alta
array[1..m, 1..3] of int: s;

% Costo total máximo permitido
float: ct;

% Cantidad máxima de movimientos permitidos
float: maxMovs;

% Factores de resistencia según nivel
% 1=baja(1.0), 2=media(1.5), 3=alta(2.0)
array[1..3] of float: resistance_factors = [1.0, 1.5, 2.0];

%-----------------------------------------------------------------------------
% VARIABLES DE DECISIÓN
%-----------------------------------------------------------------------------

% x[k,i,j] = número de personas con resistencia k que se mueven de opinión i a opinión j
array[1..3, 1..m, 1..m] of var 0..n: x;

% Distribución final de personas por opinión después de los movimientos
array[1..m] of var 0..n: final_distribution;

% Valor de la mediana de la distribución final
var float: median_value;

% Polarización final
var float: polarization;

%-----------------------------------------------------------------------------
% RESTRICCIONES
%-----------------------------------------------------------------------------

% 1. No se pueden mover más personas de las que hay inicialmente con cada nivel de resistencia
constraint forall(k in 1..3, i in 1..m)(
    sum(j in 1..m)(x[k,i,j]) <= s[i,k]
);

% 2. No se mueven personas de una opinión a sí misma
constraint forall(k in 1..3, i in 1..m)(
    x[k,i,i] = 0
);

% 3. Calcular la distribución final de personas por opinión
constraint forall(i in 1..m)(
    final_distribution[i] = p[i] + 
        sum(k in 1..3, j in 1..m)(x[k,j,i]) - 
        sum(k in 1..3, j in 1..m)(x[k,i,j])
);

% 4. El número total de personas debe mantenerse constante
constraint sum(i in 1..m)(final_distribution[i]) = n;

% 5. Restricción de costo total
% Costo de mover x personas de opinión i a j con resistencia k:
% x[k,i,j] * |i-j| * resistance_factors[k]
constraint 
    sum(k in 1..3, i in 1..m, j in 1..m)(
        x[k,i,j] * abs(i-j) * resistance_factors[k]
    ) <= ct;

% 6. Restricción de cantidad máxima de movimientos
% Movimientos = suma de distancias entre opiniones
constraint 
    sum(k in 1..3, i in 1..m, j in 1..m)(
        x[k,i,j] * abs(i-j)
    ) <= maxMovs;

%-----------------------------------------------------------------------------
% CÁLCULO DE LA MEDIANA
%-----------------------------------------------------------------------------

% Para calcular la mediana, necesitamos expandir la distribución final
% y encontrar el valor en la posición central

% Posiciones para la mediana (considerando n total de personas)
int: median_pos_low = (n div 2);
int: median_pos_high = ((n div 2) + 1);

% Variable auxiliar: acumulado de personas hasta cada opinión
array[1..m] of var 0..n: cumulative;

constraint cumulative[1] = final_distribution[1];
constraint forall(i in 2..m)(
    cumulative[i] = cumulative[i-1] + final_distribution[i]
);

% Determinar en qué opinión cae la mediana
% Si n es par, promediamos las dos posiciones centrales
% Si n es impar, tomamos el valor central

var 1..m: median_opinion_low;
var 1..m: median_opinion_high;

% Para median_opinion_low: encontrar i tal que cumulative[i-1] < median_pos_low <= cumulative[i]
constraint forall(i in 1..m)(
    (i = 1 /\ median_pos_low <= cumulative[1]) \/
    (i > 1 /\ cumulative[i-1] < median_pos_low /\ median_pos_low <= cumulative[i])
    -> median_opinion_low = i
);

% Para median_opinion_high
constraint forall(i in 1..m)(
    (i = 1 /\ median_pos_high <= cumulative[1]) \/
    (i > 1 /\ cumulative[i-1] < median_pos_high /\ median_pos_high <= cumulative[i])
    -> median_opinion_high = i
);

% Calcular el valor de la mediana
constraint if n mod 2 = 1 then
    % n impar: la mediana es el valor en la posición central
    median_value = v[median_opinion_high]
else
    % n par: la mediana es el promedio de los dos valores centrales
    median_value = (v[median_opinion_low] + v[median_opinion_high]) / 2.0
endif;

%-----------------------------------------------------------------------------
% FUNCIÓN OBJETIVO: MINIMIZAR POLARIZACIÓN
%-----------------------------------------------------------------------------

% Pol(p,v) = Σ p[i] * |v[i] - median(p,v)|
constraint polarization = sum(i in 1..m)(
    final_distribution[i] * abs(v[i] - median_value)
);

% Minimizar la polarización
solve minimize polarization;

%-----------------------------------------------------------------------------
% SALIDA
%-----------------------------------------------------------------------------

output [
    "polarization=", show(polarization), "\n",
    "final_distribution=", show(final_distribution), "\n",
    "median_value=", show(median_value), "\n",
    "movements_k1=[\n"
] ++
[
    show(x[1,i,j]) ++ if j = m then "\n" else "," endif
    | i in 1..m, j in 1..m
] ++
[
    "]\n",
    "movements_k2=[\n"
] ++
[
    show(x[2,i,j]) ++ if j = m then "\n" else "," endif
    | i in 1..m, j in 1..m
] ++
[
    "]\n",
    "movements_k3=[\n"
] ++
[
    show(x[3,i,j]) ++ if j = m then "\n" else "," endif
    | i in 1..m, j in 1..m
] ++
[
    "]\n"
];
