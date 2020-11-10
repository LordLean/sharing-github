nextTo(C1,C2,C) :-
    append(_,[C1,C2|_],C);
    append(_,[C2,C1|_],C).

leftTo(C1,C2,C) :-
    append(_,[C1,C2|_],C).

houses(H) :-
    length(H,5),
    % Nationality, Pet, Car, Colour, Drink
    member(house(brit,_,_,red,_),H),
    member(house(greek,dogs,_,_,_),H),
    member(house(chinese,_,_,_,tea),H),
    %Green house Next to and left of white house
    %nextTo(house(_,_,_,green,_),house(_,_,_,white,_),H),
    leftTo(house(_,_,_,green,_),house(_,_,_,white,_),H),
    member(house(_,_,_,green,coffee),H),
    member(house(_,canary,ford,_,_),H),
    member(house(_,_,landrover,yellow,_),H),
    H = [_,_,house(_,_,_,_,milk),_,_],
    H = [house(czech,_,_,_,_)|_],
    nextTo(house(_,_,toyota,_,_),house(_,sheep,_,_,_),H),
    nextTo(house(_,horses,_,_,_),house(_,_,landrover,yellow,_),H),
    member(house(_,_,vauxhall,_,beer),H),
    H = [_,house(_,_,_,blue,_),_,_,_],
    nextTo(house(_,_,toyota,_,_),house(_,_,_,_,water),H),
    member(house(german,_,volvo,_,_),H),
    member(house(_,cat,_,_,_),H).

