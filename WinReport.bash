# Coleta informações de eventos de inicialização do sistema
$events = Get-WinEvent -LogName System | Where-Object { $_.Id -eq 6005 -or $_.Id -eq 6006 }

# Caminho para o arquivo de relatório
$reportFile = "C:\Relatorio_Eventos_Inicializacao.txt"

# Gera um relatório e o salva em um arquivo
$events | ForEach-Object {
    $eventTime = $_.TimeCreated
    $eventMessage = $_.Message
    $report = "Data e Hora: $eventTime`nMensagem: $eventMessage`n`n"
    $report | Out-File -Append -FilePath $reportFile
}

Write-Host "Relatório de eventos de inicialização do sistema salvo em $reportFile"
