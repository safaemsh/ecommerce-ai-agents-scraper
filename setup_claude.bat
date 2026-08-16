@echo off
title Configuration Claude Desktop MCP
echo.
echo === CONFIGURATION CLAUDE DESKTOP MCP ===
echo.
python -c "$PROJECT_DIR = (Get-Location).Path; $MCP_SCRIPT = \"$PROJECT_DIR\mcp_scripts\mcp_server.py\"; $CONFIG_FILE = \"$env:APPDATA\Claude\claude_desktop_config.json\"; if (Test-Path $CONFIG_FILE) { $json = Get-Content $CONFIG_FILE -Raw | ConvertFrom-Json; if (-not $json.mcpServers.'scraping-system') { if (-not $json.mcpServers) { $json | Add-Member -MemberType NoteProperty -Name 'mcpServers' -Value @{} }; $json.mcpServers.'scraping-system' = @{ command = 'python'; args = @($MCP_SCRIPT); env = @{} }; $json | ConvertTo-Json -Depth 10 | Set-Content $CONFIG_FILE; Write-Host 'Configuration MCP ajoutee!' -ForegroundColor Green } else { Write-Host 'Configuration MCP deja presente!' -ForegroundColor Green } } else { New-Item -ItemType Directory -Force -Path \"$env:APPDATA\Claude\" | Out-Null; $config = @{ mcpServers = @{ 'scraping-system' = @{ command = 'python'; args = @($MCP_SCRIPT); env = @{} } } }; $config | ConvertTo-Json -Depth 10 | Set-Content $CONFIG_FILE; Write-Host 'Fichier de configuration cree!' -ForegroundColor Green }; Write-Host \"`nFichier: $CONFIG_FILE\" -ForegroundColor Cyan; Write-Host \"`nRedemarrez Claude Desktop pour activer MCP!\" -ForegroundColor Yellow"
echo.
pause

