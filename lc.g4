grammar lc;

root : expr                          
    // | comb                           
    ;

expr : '('expr')'                    # expresion
    | expr expr                      # aplicacion 
    | ('λ'|'\\') vars ('.') expr     # abstraccion 
    | Var                            # variable 
    // | Nombre                         # nombremacro
    ;

vars : Var+;
Var : [a-z];

// comb: Nombre ('≡'|'=') expr          # macro
//     ;

// ombre : [A-Z] [a-zA-Z0-9]*;

WS : [ \t\n\r]+ -> skip;
