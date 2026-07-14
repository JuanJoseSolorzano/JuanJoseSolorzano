param(
    [string]$InputFile = "reposInfo.txt"
)

$data = Get-Content $InputFile -Raw

$langs = @{}
$total = 0

foreach ($line in ($data -split "`n")) {
    if ($line -match '^\t([^:]+):\s*([\d,]+)\s+bytes') {
        $lang = $matches[1].Trim()
        $bytes = [int]($matches[2] -replace ',', '')
        $langs[$lang] += $bytes
        $total += $bytes
    }
}

Write-Output "=== TOTAL BYTES: $total ==="
Write-Output ""

foreach ($l in ($langs.GetEnumerator() | Sort-Object Value -Descending)) {
    $pct = [math]::Round(($l.Value / $total) * 100, 1)
    Write-Output "$($l.Key): $($l.Value) bytes ($pct%)"
}
