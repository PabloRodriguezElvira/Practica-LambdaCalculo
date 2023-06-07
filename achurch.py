from __future__ import annotations
from dataclasses import dataclass
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

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


# Custom exception (para el ejemplo 5 tarea 3 - betareducciones infinitas)
class MaxBetasReached(Exception):
    "Se lanza cuando se alcanza el número máximo de betareducciones."
    pass

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
        case Variable(var):
            if var == v:
                return Variable(nv)
            else:
                return tree
        case Abstraccion(param, t):
            if param == v:
                return Abstraccion(nv, substitute(t, v, nv))
            return Abstraccion(param, substitute(t, v, nv))
        case Aplicacion(t1, t2):
            return Aplicacion(substitute(t1, v, nv), substitute(t2, v, nv))


def alphaConversion(tl, tr, lista):
    ligadasLeft = getVariablesLigadas(tl)
    ligadasRight = getVariablesLigadas(tr)
    libresRight = getVariablesLibres(tr)
    intersec = ligadasLeft.intersection(libresRight)
    if len(intersec) != 0:
        var = list(intersec)[0]
        # Para obtener una variable nueva, tenemos que tener en cuenta TODAS las variables ligadas.
        newVar = getFreshVariable(ligadasLeft.union(ligadasRight))
        print("α-conversió: ", var, "→", newVar)
        tNew = substitute(tl, var, newVar)
        lista.append(tree2str(tl) + "→ α →" + tree2str(tNew))
        print(tree2str(tl), "→", tree2str(tNew))
        return tNew
    return Vacio()


def beta_reduction(arbol):
    # En l almacenaremos las beta-reducciones y alfa-conversiones para después mostrarlas en el bot.
    l = list()
    maxDepth = 50
    counter = 1
    while True:
        # try-catch
        try:
            res = evaluar(arbol, counter, maxDepth, l)
        except MaxBetasReached:
            print("Resultat:\nNothing")
            l.append("Nothing")
            return l
        # Se puede cambiar la condicion y comprobar si los arboles son iguales modulo alpha conversion.
        if len(tree2str(res)) == len(tree2str(arbol)):
            break
        arbol = res
    print("Resultat:")
    print(tree2str(res))
    l.append(tree2str(res))
    return l


def evaluar(tree: ArbolLC, c, md, lista) -> ArbolLC:
    match tree:
        case Variable(_):
            return tree
        case Abstraccion(param, term):
            return Abstraccion(param, evaluar(term, c, md, lista))
        case Aplicacion(termLeft, termRight):
            match termLeft:
                case Abstraccion(param, term):
                    newAbstr = alphaConversion(termLeft, termRight, lista)
                    p = param
                    t = term
                    tOld = tree
                    # Si newAbstr no es vacío, significa que hemos hecho una alfa conversión.
                    if newAbstr != Vacio():
                        p = newAbstr.var
                        t = newAbstr.term
                        tOld = Aplicacion(newAbstr, termRight)
                    tSub = applyBetaRed(p, t, termRight)
                    c = c+1
                    # Si llegamos al máximo número de beta-reducciones tiramos la excepcion custom.
                    if c == md:
                        raise MaxBetasReached 
                    print("β-reducció:")
                    lista.append(tree2str(tOld) + "→ β →" + tree2str(tSub)) 
                    print(tree2str(tOld), "→", tree2str(tSub))
                    return evaluar(tSub, c, md, lista)
                case _:
                    l = evaluar(termLeft, c, md, lista)
                    r = evaluar(termRight, c, md, lista)
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


# TELEGRAM BOT (usa la versión de python-telegram-bot 20.3) --------------------------------

# Función para /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    "Manda un mensaje cuando se escribe el comando /start y se instancia el visitor."
    user = update.effective_user
    message = "Muy buenas %s!\nSoy LambdaUltraBot!" % (user.mention_html())
    await update.message.reply_html(message)
        

# Función para /author
async def author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    "Muestra el autor del bot."
    s = "@ Pablo Rodríguez Elvira - 2023"
    await update.message.reply_text(s)

# Función para /help
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    "Muestra los comandos disponibles y su función."
    s1 = "/start -> Manda un mensaje de saludo.\n"
    s2 = "/author -> Muestra el autor del bot.\n"
    s3 = "/help -> Muestra los comandos disponibles.\n"
    s4 = "/macros -> Muestra el listado de macros que se han definido."
    await update.message.reply_text(s1+s2+s3+s4)


async def visitExpresion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    "Si el usuario nos manda una expresión, la evaluamos."
    input_stream = InputStream(update.message.text)
    lexer = lcLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = lcParser(token_stream)
    tree = parser.root()
    # Para saber si tenemos que mostrar las reducciones o no.
    macros = False
    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = LCTreeVisitor()
        arbol = visitor.visit(tree)
        listaBetasAlfas = list()
        if (arbol == "defmacro"):
            macros = True
        else:
            print("Arbre:")
            listaBetasAlfas.append(tree2str(arbol))
            listaBetasAlfas = listaBetasAlfas + beta_reduction(arbol)
    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))

    if (not macros):
        for elem in listaBetasAlfas:
            await update.message.reply_text(elem) 


async def macros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    "Se encarga de mostrar el diccionario de macros." 
    str = ""
    if (len(Macros) != 0):
        for nombre, arbol in Macros.items():
            # await update.message.reply_text(nombre + " ≡ " + tree2str(arbol))
            str += (nombre + " ≡ " + tree2str(arbol) + "\n")
    else:
        str = "No hay macros definidas en el sistema."
    await update.message.reply_text(str)


def ejecutarTerminal():
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


def ejecutarBot():
    # Creamos el bot con nuestro token:
    application = Application.builder().token("6097810236:AAEMnMIKrJLxYWdHMBU1GNW1bEdyQRukZ7U").build()

    # Añadimos los handlers para comandos:
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("author", author))
    application.add_handler(CommandHandler("help", ayuda))
    application.add_handler(CommandHandler("macros", macros))

    # Añadimos el handler para no comandos (visitar expresiones)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, visitExpresion))

    # Correr el bot:
    application.run_polling()


def main(): 
    b = True
    while b:
        print("Escribe 0 para usar la terminal, 1 para usar el Bot de Telegram.")
        option = input()
        if option == "0":
            ejecutarTerminal()
            b = False 
        elif option == "1":
            ejecutarBot()
            b = False


if __name__  == "__main__":
    main()

