from __future__ import annotations
from dataclasses import dataclass
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor


# Árbol semántico que representa las expresiones en cálculo lambda.
@dataclass
class Variable:
    val: str


@dataclass
class Abstraccion:
    var: str
    term: ArbolLC


@dataclass
class Aplicacion:
    l: ArbolLC
    r: ArbolLC


@dataclass
class Vacio:
    pass


ArbolLC = Variable | Abstraccion | Aplicacion | Vacio

# Diccionario para guardar macros (Tasca 4)
# {string, ArbolLC}
Macros = dict()

# Visitor que construye el tipo algebraico Arbol


class LCTreeVisitor(lcVisitor):
    def visitExpresion(self, ctx):
        [_, term, _] = list(ctx.getChildren())
        return self.visit(term)

    def visitAplicacion(self, ctx):
        [termino1, termino2] = list(ctx.getChildren())
        l = self.visit(termino1)
        r = self.visit(termino2)
        return Aplicacion(l, r)

    def visitAbstraccion(self, ctx):
        [_, params, _, term] = list(ctx.getChildren())
        paramsText = params.getText()
        termino = self.visit(term)

        # Si la abstracción tiene más de un parámetro, tenemos que encadenar abstracciones.
        for param in reversed(paramsText):
            termino = Abstraccion(param, termino)

        return termino

    def visitVariable(self, ctx):
        [letra] = list(ctx.getChildren())
        return Variable(letra.getText())

    def visitDefmacro(self, ctx):
        [nombre, _, term] = list(ctx.getChildren())
        t = self.visit(term)
        Macros[nombre.getText()] = t
        return "defmacro"

    def visitNombremacro(self, ctx):
        [nameMacro] = list(ctx.getChildren())
        t = Macros[nameMacro.getText()]
        return t

    def visitMacroinfija(self, ctx):
        [term1, operator, term2] = list(ctx.getChildren())
        t1 = self.visit(term1)
        t2 = self.visit(term2)
        op = Macros[operator.getText()]
        return Aplicacion(Aplicacion(op, t1), t2)



def printMacros():
    for nombre, arbol in Macros.items():
        print(nombre, "≡", tree2str(arbol))


# Función que imprime el árbol por pantalla:
def tree2str(t: ArbolLC) -> str:
    arbol = ""
    match t:
        case Variable(val):
            arbol += val
        case Abstraccion(var, term):
            arbol += "(" + "λ" + var + "." + tree2str(term) + ")"
        case Aplicacion(termL, termR):
            arbol += "(" + tree2str(termL) + tree2str(termR) + ")"
    return arbol


def getVariablesLigadas(tree):
    s = set()
    match tree:
        case Abstraccion(param, term):
            s.add(param)
            s.update(getVariablesLigadas(term))
        case Aplicacion(t1, t2):
            s.update(getVariablesLigadas(t1))
            s.update(getVariablesLigadas(t2))
    return s


def getVariablesLibres(tree):
    s = set()
    varsLigadas = getVariablesLigadas(tree)
    varsLibres = getVarsLibresPosiblesRec(tree)
    # Si nos encontramos alguna variable libre que también es ligada, entonces deja de ser libre. (Ejemplo 5 Tarea 3)
    return varsLibres - varsLigadas


def getVarsLibresPosiblesRec(tree):
    s = set()
    match tree:
        case Variable(var):
            s.add(var)
        case Abstraccion(_, term):
            s.update(getVariablesLibres(term))
        case Aplicacion(t1, t2):
            s.update(getVariablesLibres(t1))
            s.update(getVariablesLibres(t2))
    return s


def getFreshVariable(ligadas):
    abc = "abcdefghijklmnopqrstuvwxyz"
    abcSet = set(abc)
    diff = abcSet - ligadas
    return list(diff)[0]


def substitute(tree, v, nv):
    match tree:
        case Variable(_):
            return tree
        case Abstraccion(param, t):
            if param == v:
                return Abstraccion(nv, substitute(t, v, nv))
            return Abstraccion(param, substitute(t, v, nv))
        case Aplicacion(t1, t2):
            return Aplicacion(substitute(t1, v, nv), substitute(t2, v, nv))


def alphaConversion(tl, tr):
    ligadasLeft = getVariablesLigadas(tl)
    ligadasRight = getVariablesLigadas(tr)
    libres = getVariablesLibres(tr)
    intersec = ligadasLeft.intersection(libres)
    if len(intersec) != 0:
        var = list(intersec)[0]
        # Para obtener una variable nueva, tenemos que tener en cuenta TODAS las variables ligadas.
        newVar = getFreshVariable(ligadasLeft.union(ligadasRight))
        print("α-conversió: ", var, "->", newVar)
        tNew = substitute(tl, var, newVar)
        print(tree2str(tl), "->", tree2str(tNew))
        return tNew
    return Vacio()


def beta_reduction(arbol):
    maxDepth = 50
    counter = 1
    while True:
        # try-catch
        try:
            res = evaluar(arbol, counter, maxDepth)
        except RecursionError:
            print("Resultat:\nNothing")
            return
        # Se puede cambiar la condicion y comprobar si los arboles son iguales modulo alpha conversion.
        if len(tree2str(res)) == len(tree2str(arbol)):
            break
        arbol = res
    print("Resultat:")
    print(tree2str(res))


def evaluar(tree: ArbolLC, c, md) -> ArbolLC:
    match tree:
        case Variable(_):
            return tree
        case Abstraccion(param, term):
            return Abstraccion(param, evaluar(term, c, md))
        case Aplicacion(termLeft, termRight):
            match termLeft:
                case Abstraccion(param, term):
                    newAbstr = alphaConversion(termLeft, termRight)
                    p = param
                    t = term
                    tOld = tree
                    if newAbstr != Vacio():
                        p = newAbstr.var
                        t = newAbstr.term
                        tOld = Aplicacion(newAbstr, termRight)
                    tSub = applyBetaRed(p, t, termRight)
                    c = c+1
                    # Si llegamos al máximo número de beta-reducciones tiramos la excepcion.
                    if c == md:
                        raise RecursionError
                    print("β-reducció:")
                    print(tree2str(tOld), "->", tree2str(tSub))
                    return evaluar(tSub, c, md)
                case _:
                    l = evaluar(termLeft, c, md)
                    r = evaluar(termRight, c, md)
                    return Aplicacion(l, r)


def applyBetaRed(param, tree: ArbolLC, sub: ArbolLC) -> ArbolLC:
    match tree:
        case Variable(val):
            if (val == param):
                return sub
            else:
                return tree
        case Aplicacion(left, right):
            newl = applyBetaRed(param, left, sub)
            newr = applyBetaRed(param, right, sub)
            return Aplicacion(newl, newr)
        case Abstraccion(var, term):
            newt = applyBetaRed(param, term, sub)
            return Abstraccion(var, newt)


while True:
    input_stream = InputStream(input('? '))
    lexer = lcLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = lcParser(token_stream)
    tree = parser.root()

    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = LCTreeVisitor()
        arbol = visitor.visit(tree)
        if (arbol == "defmacro"):
            printMacros()
        else:
            print("Arbre:")
            print(tree2str(arbol))
            beta_reduction(arbol)
    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))


# print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
# print(tree.toStringTree(recog=parser))
