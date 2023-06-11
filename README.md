# Práctica LP - Intérprete y evaluador de expresiones en λ-cálculo

En esta práctica de LP se ha realizado un evaluador de expresiones en λ-cálculo. También se ha hecho un bot en Telegram que lo incorpora.

# Instalación

Se necesita python-telegram-bot versión 20.3. El bot de Telegram se ha hecho con esta versión.
```bash 
pip install python-telegram-bot --upgrade
```
Librerías para visualizar los grafos de las expresiones: 
```bash
pip install pydot
sudo apt install graphviz 
```
ANTLR para la gramática:
```bash
pip install antlr4-tools
antlr4
pip install antlr4-python3-runtime
```

# Uso

Simplemente ejecutar el script achurch.py, en la terminal saldrá un mensaje preguntando si se quiere usar el bot o la terminal para evaluar expresiones. El bot de telegram tiene dirección t.me/LambdaUltraBot.
