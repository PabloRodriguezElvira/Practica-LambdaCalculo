# Generated from lc.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,10,43,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,3,0,11,8,0,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,25,8,1,1,1,1,1,5,
        1,29,8,1,10,1,12,1,32,9,1,1,2,4,2,35,8,2,11,2,12,2,36,1,3,1,3,1,
        3,1,3,1,3,0,1,2,4,0,2,4,6,0,2,1,0,3,4,1,0,6,7,44,0,10,1,0,0,0,2,
        24,1,0,0,0,4,34,1,0,0,0,6,38,1,0,0,0,8,11,3,2,1,0,9,11,3,6,3,0,10,
        8,1,0,0,0,10,9,1,0,0,0,11,1,1,0,0,0,12,13,6,1,-1,0,13,14,5,1,0,0,
        14,15,3,2,1,0,15,16,5,2,0,0,16,25,1,0,0,0,17,18,7,0,0,0,18,19,3,
        4,2,0,19,20,5,5,0,0,20,21,3,2,1,3,21,25,1,0,0,0,22,25,5,8,0,0,23,
        25,5,9,0,0,24,12,1,0,0,0,24,17,1,0,0,0,24,22,1,0,0,0,24,23,1,0,0,
        0,25,30,1,0,0,0,26,27,10,4,0,0,27,29,3,2,1,5,28,26,1,0,0,0,29,32,
        1,0,0,0,30,28,1,0,0,0,30,31,1,0,0,0,31,3,1,0,0,0,32,30,1,0,0,0,33,
        35,5,8,0,0,34,33,1,0,0,0,35,36,1,0,0,0,36,34,1,0,0,0,36,37,1,0,0,
        0,37,5,1,0,0,0,38,39,5,9,0,0,39,40,7,1,0,0,40,41,3,2,1,0,41,7,1,
        0,0,0,4,10,24,30,36
    ]

class lcParser ( Parser ):

    grammarFileName = "lc.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'\\u03BB'", "'\\'", "'.'", 
                     "'\\u2261'", "'='" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "Var", "Nombre", "WS" ]

    RULE_root = 0
    RULE_expr = 1
    RULE_vars = 2
    RULE_comb = 3

    ruleNames =  [ "root", "expr", "vars", "comb" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    Var=8
    Nombre=9
    WS=10

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(lcParser.ExprContext,0)


        def comb(self):
            return self.getTypedRuleContext(lcParser.CombContext,0)


        def getRuleIndex(self):
            return lcParser.RULE_root

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = lcParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        try:
            self.state = 10
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 8
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 9
                self.comb()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return lcParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ExpresionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(lcParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpresion" ):
                return visitor.visitExpresion(self)
            else:
                return visitor.visitChildren(self)


    class NombremacroContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Nombre(self):
            return self.getToken(lcParser.Nombre, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNombremacro" ):
                return visitor.visitNombremacro(self)
            else:
                return visitor.visitChildren(self)


    class VariableContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Var(self):
            return self.getToken(lcParser.Var, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariable" ):
                return visitor.visitVariable(self)
            else:
                return visitor.visitChildren(self)


    class AplicacionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(lcParser.ExprContext)
            else:
                return self.getTypedRuleContext(lcParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAplicacion" ):
                return visitor.visitAplicacion(self)
            else:
                return visitor.visitChildren(self)


    class AbstraccionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def vars_(self):
            return self.getTypedRuleContext(lcParser.VarsContext,0)

        def expr(self):
            return self.getTypedRuleContext(lcParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbstraccion" ):
                return visitor.visitAbstraccion(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = lcParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                localctx = lcParser.ExpresionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 13
                self.match(lcParser.T__0)
                self.state = 14
                self.expr(0)
                self.state = 15
                self.match(lcParser.T__1)
                pass
            elif token in [3, 4]:
                localctx = lcParser.AbstraccionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 17
                _la = self._input.LA(1)
                if not(_la==3 or _la==4):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 18
                self.vars_()

                self.state = 19
                self.match(lcParser.T__4)
                self.state = 20
                self.expr(3)
                pass
            elif token in [8]:
                localctx = lcParser.VariableContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 22
                self.match(lcParser.Var)
                pass
            elif token in [9]:
                localctx = lcParser.NombremacroContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 23
                self.match(lcParser.Nombre)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 30
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = lcParser.AplicacionContext(self, lcParser.ExprContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                    self.state = 26
                    if not self.precpred(self._ctx, 4):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                    self.state = 27
                    self.expr(5) 
                self.state = 32
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class VarsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Var(self, i:int=None):
            if i is None:
                return self.getTokens(lcParser.Var)
            else:
                return self.getToken(lcParser.Var, i)

        def getRuleIndex(self):
            return lcParser.RULE_vars

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVars" ):
                return visitor.visitVars(self)
            else:
                return visitor.visitChildren(self)




    def vars_(self):

        localctx = lcParser.VarsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_vars)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 33
                self.match(lcParser.Var)
                self.state = 36 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==8):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CombContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return lcParser.RULE_comb

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class MacroContext(CombContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a lcParser.CombContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Nombre(self):
            return self.getToken(lcParser.Nombre, 0)
        def expr(self):
            return self.getTypedRuleContext(lcParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacro" ):
                return visitor.visitMacro(self)
            else:
                return visitor.visitChildren(self)



    def comb(self):

        localctx = lcParser.CombContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_comb)
        self._la = 0 # Token type
        try:
            localctx = lcParser.MacroContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.match(lcParser.Nombre)
            self.state = 39
            _la = self._input.LA(1)
            if not(_la==6 or _la==7):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 40
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         




