#!/bin/zsh
# Uso: run.sh <nombre> <mcp.json|-> <allowedTools> <prompt> [plugins_on]
# Lanza claude -p aislado (sin MCP del usuario, plugins apagados salvo que se pidan) y guarda el JSON.
D=${0:a:h}; N=$1; M=$2; T=$3; PR=$4; PL=${5:-off}
W=$D/work/$N; mkdir -p $W; cd $W
if [[ $PL == off ]]; then S='{"enabledPlugins":{"superpowers@claude-plugins-official":false,"context7@claude-plugins-official":false,"frontend-design@claude-plugins-official":false,"ralph-loop@claude-plugins-official":false,"ccos-asset-creator@local-desktop-app-uploads":false}}'; else S='{"enabledPlugins":{"superpowers@claude-plugins-official":true,"context7@claude-plugins-official":false,"frontend-design@claude-plugins-official":false,"ralph-loop@claude-plugins-official":false,"ccos-asset-creator@local-desktop-app-uploads":false}}'; fi
MC=(--strict-mcp-config); [[ $M != - ]] && MC+=(--mcp-config $D/$M)
t0=$(date +%s)
claude -p "$PR" --model claude-sonnet-5-5 --output-format json --no-session-persistence --settings "$S" $MC --allowedTools "$T" > $D/runs/$N.json 2> $D/runs/$N.err
echo "{\"wall_s\": $(( $(date +%s) - t0 ))}" > $D/runs/$N.wall.json
uv run python -I -c "import json,sys;d=json.load(open('$D/runs/$N.json'));print('$N',d.get('num_turns'),round(d.get('total_cost_usd',0),3),d.get('usage',{}).get('input_tokens'),d.get('usage',{}).get('cache_read_input_tokens'),d.get('usage',{}).get('output_tokens'),open('$D/runs/$N.wall.json').read().strip())"
