# Banco de pruebas de extensiones de Claude

Material del vídeo «Medí 7 extensiones de Claude: solo 2 cambian el juego» (Frogames Formación).
Mide, con el mismo encargo y **con y sin** cada extensión, el tiempo, los tokens y si la tarea sale bien.

Pruebas hechas el 24 de noviembre de 2026 con Claude Code 2.1.330 y `claude-sonnet-5-5`.
Los dólares que da `claude -p` son el equivalente en API, no un cobro real.

## Las 7 extensiones y qué se midió

| Extensión | Encargo | Sin ella | Con ella | Veredicto |
|---|---|---|---|---|
| **Firecrawl** (MCP, sin clave) | Kit de marca de una web | 31 s, 5 turnos: «no he podido» | 16 s, 2 turnos: 5 de 6 datos bien | Sí |
| **Playwright** (MCP) | Hacer las 5 primeras preguntas de un test web y leer la 6.ª | 20 s: «no tengo navegador» | 63 s, 22 turnos: lo consigue | Sí, pero caro |
| **Context7** (MCP) | Script con un SDK actual y comandos de `playwright-cli` | Respuesta correcta a la primera | La misma respuesta | No cambió nada |
| **Superpowers** (plugin) | `validar_iban_es()` «lista para producción» + 10 tests ocultos | 9/10 | 9/10 (repetido: 9/10); cargó 15 skills y no usó ninguna | No cambió nada en tarea pequeña |
| **Perplexity** | Sin medir: necesita clave de API con saldo | | | Depende |
| **PostHog** | Sin medir: necesita una web que ya mande datos a PostHog | | | Depende |
| **Composio** | Sin medir: necesita cuenta y acceso OAuth a tus apps | | | Depende |

Playwright leyó 1,17 M tokens de contexto (caché) frente a 0,32 M sin él: 3,6x contexto y 3x tiempo.

### Coste de tenerlas instaladas (tokens de entrada en un «Responde solo: hola»)

| Configuración | Tokens | Diferencia |
|---|---|---|
| Ninguna | 50.984 (repetido: 50.992) | |
| + Firecrawl | 57.263 (repetido: 57.266) | +6.279 en cada mensaje |
| + Playwright | 51.371 | +387 |
| + Context7 | 51.310 | +326 |
| Las tres | 57.902 | +6.918 |

## Cómo instalarlas

| Extensión | Instalación |
|---|---|
| Firecrawl | MCP remoto `https://mcp.firecrawl.dev/v2/mcp` (ver `mcp/firecrawl.json`) |
| Playwright | `claude mcp add playwright npx @playwright/mcp@latest` |
| Context7 | `npx @upstash/context7-mcp` o remoto `mcp.context7.com/mcp` |
| Superpowers | `/plugin install superpowers@claude-plugins-official` |
| Perplexity | `claude mcp add perplexity` con `PERPLEXITY_API_KEY` y `@perplexity-ai/mcp-server` |
| PostHog | Directorio de conectores de Claude o `npx @posthog/wizard mcp add` |
| Composio | Conector personalizado con `connect.composio.dev/mcp` |

## Contenido

- `run.sh`: lanza `claude -p` aislado (`--strict-mcp-config`, plugins apagados salvo el que se prueba) y guarda el JSON en `runs/`.
- `mcp/*.json`: configuración MCP de cada prueba (`firecrawl`, `playwright`, `context7`, `todos`).
- `tests_ocultos_iban.py`: los 10 tests ocultos del IBAN español.
- `work/sp-base`, `work/sp-plugin`, `work/sp-plugin2`: el `iban.py` que escribió Claude sin Superpowers y con él.
- `datos.json`: resumen de los resultados medidos.

## Reproducir el test del IBAN

```bash
uv run python tests_ocultos_iban.py work/sp-base
uv run python tests_ocultos_iban.py work/sp-plugin
```

Las tres variantes sacan 9/10. Todas fallan el mismo caso: un IBAN que cuadra el control ISO pero con los
dígitos de control de la cuenta (CCC) mal. Ninguna valida el CCC.

## Lanzar una prueba

Hace falta Claude Code instalado. Uso: `./run.sh <nombre> <mcp.json|-> <allowedTools> <prompt> [plugins_on]`

```bash
./run.sh fc-mcp mcp/firecrawl.json "mcp__firecrawl" "Dame el kit de marca de https://ejemplo.com"
```
