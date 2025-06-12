param (
  [string]$file = $(throw "Podaj plik z kodem")
)

Write-Host "=== Uruchamianie interpretera ==="
python interpreter.py $file
