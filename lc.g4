grammar lc;

root : expr                          
    | comb                           
    ;

expr : '('expr')'                    # expresion
    | expr Op expr                   # macroinfija
    | expr expr                      # aplicacion 
    | ('λ'|'\\') vars ('.') expr     # abstraccion 
    | Var                            # variable 
    | (Nombre|Op)                    # nombremacro
    ;

vars : Var+;

Var : [a-z];

comb: (Nombre|Op) ('≡'|'=') expr          # defmacro
    ;

Op: ('+'|'-');

Nombre : [A-Z] [a-zA-Z0-9]*;

WS : [ \t\n\r]+ -> skip;
