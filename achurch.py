from __future__ import annotations
from dataclasses import dataclass
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import pydot

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

# Clase visitor que construye el tipo algebraico ArbolLC
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


# Imprime el diccionario de macros.
def printMacros():
    for nombre, arbol in Macros.items():
        print(nombre, "≡", tree2str(arbol))


# Pasa el árbol de tipo ArbolLC a string.
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

# Obtiene el conjunto de variables ligadas del árbol tree. 
def getVariablesLigadas(tree: ArbolLC) -> set:
    s = set()
    match tree:
        case Abstraccion(param, term):
            s.add(param)
            s.update(getVariablesLigadas(term))
        case Aplicacion(t1, t2):
            s.update(getVariablesLigadas(t1))
            s.update(getVariablesLigadas(t2))
    return s

# Obtiene el conjunto de variables libres del árbol tree.
def getVariablesLibres(tree) -> set:
    varsLigadas = getVariablesLigadas(tree)
    varsLibres = getVarsLibresPosiblesRec(tree)
    # Si nos encontramos alguna variable libre que también es ligada, entonces deja de ser libre. (Ejemplo 5 Tarea 3)
    return varsLibres - varsLigadas

# Obtiene las variables (en general) del árbol tree.
def getVarsLibresPosiblesRec(tree: ArbolLC) -> set:
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

# Devuelve una variable no usada en el árbol.
def getFreshVariable(ligadas: set) -> str:
    abc = "abcdefghijklmnopqrstuvwxyz"
    abcSet = set(abc)
    diff = abcSet - ligadas
    return list(diff)[0]

# Sustituye en el ArbolLC tree las apariciones de la variable v por nv.
def substitute(tree: ArbolLC, v: str, nv: str) -> ArbolLC:
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

# Realiza una alfa-conversión en el árbol formado por tl y tr. Si no quedan
# posibles alfa-conversiones, se retorna el arbol vacío.
def alphaConversion(tl: ArbolLC, tr: ArbolLC, lista: list) -> ArbolLC:
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

# Realiza beta-reducciones hasta que el árbol obtenido no cambie (o hasta que se llegue al límite
# de beta-reducciones.) Retorna la lista que usaremos para mostrar en el bot y el último árbol evaluado.
def beta_reduction(arbol: ArbolLC) -> tuple:
    # En l almacenaremos las beta-reducciones y alfa-conversiones para después mostrarlas en el bot.
    l = list()
    maxDepth = 50
    counter = 1
    while True:
        try:
            res = evaluar(arbol, counter, maxDepth, l)
        except MaxBetasReached:
            print("Resultat:\nNothing")
            l.append("Nothing")
            return l, Vacio()
        if len(tree2str(res)) == len(tree2str(arbol)):
            break
        arbol = res
    print("Resultat:")
    print(tree2str(res))
    l.append(tree2str(res))
    return l, res

# Función recursiva encargada de encontrar una beta-reducción y aplicarla.
# Justo antes de aplicarla hemos de comprobar si se puede aplicar una alfa-conversión.
def evaluar(tree: ArbolLC, c: int, md: int, lista: list) -> ArbolLC:
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

# Función encargada de aplicar una beta-reducción, es decir, sustituir las aparciciones de
# param en tree por sub.
def applyBetaRed(param: str, tree: ArbolLC, sub: ArbolLC) -> ArbolLC:
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


# TELEGRAM BOT t.me/LambdaUltraBot (usa la versión de python-telegram-bot 20.3) --------------------------------

# Función recursiva encargada de generar el grafo. La idea detrás de esta función es que cada nodo
# ha de tener un identificador único, por eso tenemos un parámetro path que vamos actualizando
# en cada case. Con este identificador vamos creando los nodos y añadiendo las aristas que tocan al grafo
# (parámetro graph)
def crearGrafoRec(tree: ArbolLC, path: str, graph) -> str:
    match tree:
        case Abstraccion(var, term):
            path_child = path + var
            nodo = pydot.Node(path_child, label="λ"+var, penwidth=0)
            graph.add_node(nodo)
            graph.add_edge(pydot.Edge(
                path_child, crearGrafoRec(term, path_child, graph)))
            return path_child

        case Aplicacion(t1, t2):
            path_child = path + "@"
            nodo = pydot.Node(path_child, label="@", penwidth=0)
            graph.add_node(nodo)
            # Añadimos 1 o 2 a los hijos izquierdo y derecho para diferenciarlos. (cada árbol ha de tener un id diferente)
            graph.add_edge(pydot.Edge(
                path_child, crearGrafoRec(t1, path_child+"1", graph)))
            graph.add_edge(pydot.Edge(
                path_child, crearGrafoRec(t2, path_child+"2", graph)))
            return path_child

        case Variable(var):
            # Añadimos "|" para indicar final de path.
            path_child = path + "|"
            nodo = pydot.Node(path_child, label=var, penwidth=0)
            graph.add_node(nodo)
            # Comprobamos si la variable aparece en el path. Si aparece, significa que hay una abstracción que
            # tiene parámetro igual a dicha variable. Tenemos que encontrar la posición de la última aparición de esta variable,
            # ya que el camino desde el principio hasta esa posición es el id de la abstracción con la que la queremos ligar.
            # rfind se encarga de encontrar la última aparición de la variable en el path.
            lastPos = path_child.rfind(var)
            if lastPos != -1:
                id_abstr = path_child[:lastPos+1]
                graph.add_edge(pydot.Edge(path_child, id_abstr,
                               style="dashed", color="magenta"))
            return path_child


# Se encarga de llamar a la función recursiva de creación del grafo y guardarlo en un archivo.
def crearGrafo(tree: ArbolLC, option: int):
    graph = pydot.Dot(graph_type='digraph')
    path = ""
    crearGrafoRec(tree, path, graph)

    # Guardar el gráfico en un archivo
    if option == 0:
        graph.write_png('grafoInicial.png')
    else:
        graph.write_png('grafoFinal.png')


# FUNCIONES PARA LOS COMANDOS DEL BOT ------------------------

# Función para /start. Da un mensaje de bienvenida.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = "Muy buenas %s!\nSoy LambdaUltraBot!" % (user.mention_html())
    await update.message.reply_html(message)


# Función para /author. Muestra el autor del bot.
async def author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    s = "@ Pablo Rodríguez Elvira - 2023"
    await update.message.reply_text(s)

# Función para /help. Muestra los comandos y una breve explicación de cada uno.
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    s1 = "/start -> Manda un mensaje de saludo.\n"
    s2 = "/author -> Muestra el autor del bot.\n"
    s3 = "/help -> Muestra los comandos disponibles.\n"
    s4 = "/macros -> Muestra el listado de macros que se han definido.\n"
    s5 = "El bot evaluará expresiones en λ-cálculo con sintaxis correcta."
    await update.message.reply_text(s1+s2+s3+s4+s5)


# Función para visitar expresiones o definir macros.
async def visitExpresion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        if (arbol == "defmacro"):
            macros = True
        else:
            listaBetasAlfas, ultimoArbol = beta_reduction(arbol)
            # Grafo del árbol inicial:
            crearGrafo(arbol, 0)
            # Grafo del árbol resultado:
            crearGrafo(ultimoArbol, 1)
    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))

    if (not macros):
        # Mostrar el árbol inicial:
        await update.message.reply_text(tree2str(arbol))
        # Mostrar grafo del árbol inicial:
        await update.message.reply_photo("grafoInicial.png")
        # Mostrar lista de beta-reducciones/alfa-conversiones:
        for elem in listaBetasAlfas:
            await update.message.reply_text(elem)
        # Mostrar grafo del árbol final (si no es Vacio)
        if ultimoArbol != Vacio():
            await update.message.reply_photo("grafoFinal.png")

# Función para /macros. Se encarga de mostrar el diccionario de macros.
async def macros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    str = ""
    if (len(Macros) != 0):
        for nombre, arbol in Macros.items():
            str += (nombre + " ≡ " + tree2str(arbol) + "\n")
    else:
        str = "No hay macros definidas en el sistema."
    await update.message.reply_text(str)


# PROGRAMA PRINCIPAL ----------------------------------------------

# Se usa la terminal para evaluar expresiones.
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

# Se usa el bot en vez de la terminal.
def ejecutarBot():
    # Creamos el bot con nuestro token:
    application = Application.builder().token(
        "6097810236:AAEMnMIKrJLxYWdHMBU1GNW1bEdyQRukZ7U").build()

    # Añadimos los handlers para comandos:
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("author", author))
    application.add_handler(CommandHandler("help", ayuda))
    application.add_handler(CommandHandler("macros", macros))

    # Añadimos el handler para no comandos (visitar expresiones)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, visitExpresion))

    # Correr el bot:
    application.run_polling()

# Programa principal. Pregunta al usuario si quiere usar la terminal o el bot de Telegram.
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


if __name__ == "__main__":
    main()
