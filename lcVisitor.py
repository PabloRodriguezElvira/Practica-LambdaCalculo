# Generated from lc.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .lcParser import lcParser
else:
    from lcParser import lcParser

# This class defines a complete generic visitor for a parse tree produced by lcParser.

class lcVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by lcParser#root.
    def visitRoot(self, ctx:lcParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lcParser#expresion.
    def visitExpresion(self, ctx:lcParser.ExpresionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lcParser#nombremacro.
    def visitNombremacro(self, ctx:lcParser.NombremacroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lcParser#variable.
    def visitVariable(self, ctx:lcParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lcParser#aplicacion.
    def visitAplicacion(self, ctx:lcParser.AplicacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lcParser#abstraccion.
    def visitAbstraccion(self, ctx:lcParser.AbstraccionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lcParser#vars.
    def visitVars(self, ctx:lcParser.VarsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lcParser#defmacro.
    def visitDefmacro(self, ctx:lcParser.DefmacroContext):
        return self.visitChildren(ctx)



del lcParser