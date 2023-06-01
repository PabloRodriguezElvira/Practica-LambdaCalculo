grammar lc;

root : expr                          
    // | comb                           
    ;

expr : '('expr')'                    # expresion
    | expr expr                      # aplicacion 
    | ('λ'|'\\') Var+ ('.') expr     # abstraccion 
    | Var                            # variable 
    // | Nombre                         # nombremacro
    ;

Var : [a-z];                               

// comb: Nombre ('≡'|'=') expr          # macro
//     ;

// Nombre : [A-Z] [a-zA-Z0-9]*;

WS : [ \t\n\r]+ -> skip;
