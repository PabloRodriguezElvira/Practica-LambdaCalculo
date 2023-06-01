// Generated from /home/paloli/Documentos/q6/lp/practica/Practica-LambdaCalculo/lc.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class lcParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, Var=8, Nombre=9, 
		WS=10;
	public static final int
		RULE_root = 0, RULE_expr = 1, RULE_vars = 2, RULE_comb = 3;
	private static String[] makeRuleNames() {
		return new String[] {
			"root", "expr", "vars", "comb"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'('", "')'", "'\u03BB'", "'\\'", "'.'", "'\u2261'", "'='"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, "Var", "Nombre", "WS"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "lc.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public lcParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class RootContext extends ParserRuleContext {
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public CombContext comb() {
			return getRuleContext(CombContext.class,0);
		}
		public RootContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_root; }
	}

	public final RootContext root() throws RecognitionException {
		RootContext _localctx = new RootContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_root);
		try {
			setState(10);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(8);
				expr(0);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(9);
				comb();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ExprContext extends ParserRuleContext {
		public ExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expr; }
	 
		public ExprContext() { }
		public void copyFrom(ExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class ExpresionContext extends ExprContext {
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public ExpresionContext(ExprContext ctx) { copyFrom(ctx); }
	}
	public static class NombremacroContext extends ExprContext {
		public TerminalNode Nombre() { return getToken(lcParser.Nombre, 0); }
		public NombremacroContext(ExprContext ctx) { copyFrom(ctx); }
	}
	public static class VariableContext extends ExprContext {
		public TerminalNode Var() { return getToken(lcParser.Var, 0); }
		public VariableContext(ExprContext ctx) { copyFrom(ctx); }
	}
	public static class AplicacionContext extends ExprContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public AplicacionContext(ExprContext ctx) { copyFrom(ctx); }
	}
	public static class AbstraccionContext extends ExprContext {
		public VarsContext vars() {
			return getRuleContext(VarsContext.class,0);
		}
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public AbstraccionContext(ExprContext ctx) { copyFrom(ctx); }
	}

	public final ExprContext expr() throws RecognitionException {
		return expr(0);
	}

	private ExprContext expr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExprContext _localctx = new ExprContext(_ctx, _parentState);
		ExprContext _prevctx = _localctx;
		int _startState = 2;
		enterRecursionRule(_localctx, 2, RULE_expr, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(24);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__0:
				{
				_localctx = new ExpresionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(13);
				match(T__0);
				setState(14);
				expr(0);
				setState(15);
				match(T__1);
				}
				break;
			case T__2:
			case T__3:
				{
				_localctx = new AbstraccionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(17);
				_la = _input.LA(1);
				if ( !(_la==T__2 || _la==T__3) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(18);
				vars();
				{
				setState(19);
				match(T__4);
				}
				setState(20);
				expr(3);
				}
				break;
			case Var:
				{
				_localctx = new VariableContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(22);
				match(Var);
				}
				break;
			case Nombre:
				{
				_localctx = new NombremacroContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(23);
				match(Nombre);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(30);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new AplicacionContext(new ExprContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_expr);
					setState(26);
					if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
					setState(27);
					expr(5);
					}
					} 
				}
				setState(32);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public static class VarsContext extends ParserRuleContext {
		public List<TerminalNode> Var() { return getTokens(lcParser.Var); }
		public TerminalNode Var(int i) {
			return getToken(lcParser.Var, i);
		}
		public VarsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_vars; }
	}

	public final VarsContext vars() throws RecognitionException {
		VarsContext _localctx = new VarsContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_vars);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(34); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(33);
				match(Var);
				}
				}
				setState(36); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==Var );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class CombContext extends ParserRuleContext {
		public CombContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comb; }
	 
		public CombContext() { }
		public void copyFrom(CombContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class MacroContext extends CombContext {
		public TerminalNode Nombre() { return getToken(lcParser.Nombre, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public MacroContext(CombContext ctx) { copyFrom(ctx); }
	}

	public final CombContext comb() throws RecognitionException {
		CombContext _localctx = new CombContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_comb);
		int _la;
		try {
			_localctx = new MacroContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(38);
			match(Nombre);
			setState(39);
			_la = _input.LA(1);
			if ( !(_la==T__5 || _la==T__6) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			setState(40);
			expr(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 1:
			return expr_sempred((ExprContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean expr_sempred(ExprContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 4);
		}
		return true;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\f-\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\4\5\t\5\3\2\3\2\5\2\r\n\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3"+
		"\3\3\3\3\3\3\3\5\3\33\n\3\3\3\3\3\7\3\37\n\3\f\3\16\3\"\13\3\3\4\6\4%"+
		"\n\4\r\4\16\4&\3\5\3\5\3\5\3\5\3\5\2\3\4\6\2\4\6\b\2\4\3\2\5\6\3\2\b\t"+
		"\2.\2\f\3\2\2\2\4\32\3\2\2\2\6$\3\2\2\2\b(\3\2\2\2\n\r\5\4\3\2\13\r\5"+
		"\b\5\2\f\n\3\2\2\2\f\13\3\2\2\2\r\3\3\2\2\2\16\17\b\3\1\2\17\20\7\3\2"+
		"\2\20\21\5\4\3\2\21\22\7\4\2\2\22\33\3\2\2\2\23\24\t\2\2\2\24\25\5\6\4"+
		"\2\25\26\7\7\2\2\26\27\5\4\3\5\27\33\3\2\2\2\30\33\7\n\2\2\31\33\7\13"+
		"\2\2\32\16\3\2\2\2\32\23\3\2\2\2\32\30\3\2\2\2\32\31\3\2\2\2\33 \3\2\2"+
		"\2\34\35\f\6\2\2\35\37\5\4\3\7\36\34\3\2\2\2\37\"\3\2\2\2 \36\3\2\2\2"+
		" !\3\2\2\2!\5\3\2\2\2\" \3\2\2\2#%\7\n\2\2$#\3\2\2\2%&\3\2\2\2&$\3\2\2"+
		"\2&\'\3\2\2\2\'\7\3\2\2\2()\7\13\2\2)*\t\3\2\2*+\5\4\3\2+\t\3\2\2\2\6"+
		"\f\32 &";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}