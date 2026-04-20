$content = Get-Content 'c:\Users\pacc1\Downloads\PATRICK\tib site\site\9a992352-1a20-4ee4-bfd2-01c940b8e11f.htm' -Raw -Encoding UTF8
$text = $content -replace '<[^>]+>', ' '
$text = $text -replace '&nbsp;', ' '
$text = $text -replace '&amp;', '&'
$text = $text -replace '&lt;', '<'
$text = $text -replace '&gt;', '>'
$text = $text -replace '\s+', ' '
$trimmed = $text.Substring(0, [Math]::Min($text.Length, 80000))
$trimmed | Out-File 'c:\Users\pacc1\Downloads\PATRICK\tib site\site\extracted_text.txt' -Encoding UTF8
Write-Host 'Done'
