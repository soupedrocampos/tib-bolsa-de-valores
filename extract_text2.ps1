$content = Get-Content 'c:\Users\pacc1\Downloads\PATRICK\tib site\site\9a992352-1a20-4ee4-bfd2-01c940b8e11f.htm' -Raw -Encoding UTF8

# Remove style/script/base64 blobs
$text = $content -replace '(?s)<style[^>]*>.*?</style>', ''
$text = $text -replace '(?s)<script[^>]*>.*?</script>', ''
$text = $text -replace 'data:[^"]+base64,[^"]+', ''

# Remove all HTML tags
$text = $text -replace '<[^>]+>', ' '

# Fix entities
$text = $text -replace '&nbsp;', ' '
$text = $text -replace '&amp;', '&'
$text = $text -replace '&lt;', '<'
$text = $text -replace '&gt;', '>'
$text = $text -replace '&#160;', ' '
$text = $text -replace '&quot;', '"'

# Collapse whitespace and filter meaningful lines
$lines = $text -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_.Length -gt 10 }

$output = $lines -join "`n"

# Take first 60000 chars
$trimmed = $output.Substring(0, [Math]::Min($output.Length, 60000))
$trimmed | Out-File 'c:\Users\pacc1\Downloads\PATRICK\tib site\site\extracted_text2.txt' -Encoding UTF8
Write-Host "Done: $($trimmed.Length) chars"
