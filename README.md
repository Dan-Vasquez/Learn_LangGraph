# Introduccion

Este es un proyecto de prueba para explirar el funcionamiento y manejo de LangChanin y LangGraph, en la reacion de agentes y flujos, utlizando inteligencia artificial

# Requisitos

- Python 3.10+
- Tener uv installado local o globalmente (ej pip install uv )

# Installacion

Si no funciona o esta en local con pip anteponer `python -m` antes de los comandos

Verificacion
```
uv --version
```
Iniciar repositorio y entorno
```
uv init
uv venv
```
Iniciar repositorio y entorno
```
.venv\Scripts\activate
```
añadir dependencias 
```
uv add langgraph langchain langchain-openai
```
añadir dependencias de desarrollo
```
uv add langgraph-cli[inmem] ipykernel --dev
```
Sincronizar entorno de uv
```
uv sync
```
Instalar paquete
```
uv pip install -e .
```


# Comandos de ejecusion entorno desarrollo

LangGraph - UI 
```
uv run langgraph dev
```


Desarrollador - **DanDok**
