Param(
  [Parameter(Mandatory=$true)]
  [ValidateSet("deepseek","openai","gemini","azure","openai_compat")]
  [string]$Provider,
  [Parameter(Mandatory=$true)]
  [string]$Key,
  [string]$Base = "",
  [switch]$Insecure
)

function Get-UrlAndHeaders {
  param($Provider,$Key,$Base)
  switch ($Provider) {
    "deepseek" { @{ Url = "https://api.deepseek.com/models"; Headers = @{ Authorization = "Bearer $Key" } } }
    "openai"   { @{ Url = "https://api.openai.com/v1/models"; Headers = @{ Authorization = "Bearer $Key" } } }
    "gemini"   { @{ Url = "https://generativelanguage.googleapis.com/v1beta/models?key=$Key"; Headers = @{} } }
    "azure"    {
      if (-not $Base) { throw "Azure requires -Base like https://<resource>.openai.azure.com" }
      @{ Url = "$($Base.TrimEnd('/'))/openai/models?api-version=2024-10-21"; Headers = @{ "api-key" = $Key } }
    }
    "openai_compat" {
      if (-not $Base) { throw "openai_compat requires -Base like http://localhost:8000/v1" }
      @{ Url = "$($Base.TrimEnd('/'))/models"; Headers = @{ Authorization = "Bearer $Key" } }
    }
  }
}

$cfg = Get-UrlAndHeaders -Provider $Provider -Key $Key -Base $Base
$invokeParams = @{
  Uri = $cfg.Url
  Headers = $cfg.Headers
  Method = "GET"
  ErrorAction = "SilentlyContinue"
  TimeoutSec = 15
}
if ($Insecure) { $invokeParams.SkipCertificateCheck = $true }

try {
  $resp = Invoke-WebRequest @invokeParams
  $code = [int]$resp.StatusCode
} catch {
  $code = if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { 0 }
}

Write-Host "PROVIDER=$Provider URL=$($cfg.Url) STATUS=$code"

if ($code -ge 200 -and $code -lt 300) { exit 0 }
elseif ($code -eq 401 -or $code -eq 403) { exit 1 }
elseif ($code -eq 429) { exit 3 }
elseif ($code -ge 500 -and $code -lt 600) { exit 4 }
else { exit 5 }
