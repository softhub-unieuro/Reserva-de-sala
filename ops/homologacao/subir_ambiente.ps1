$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$envFile = Join-Path $projectRoot ".env"

Push-Location $projectRoot
try {

if (-not (Test-Path $envFile)) {
    New-Item -Path $envFile -ItemType File | Out-Null
}

function Get-EnvValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Key
    )

    $line = Get-Content $envFile | Where-Object { $_ -match "^\s*$([regex]::Escape($Key))\s*=" } | Select-Object -Last 1
    if (-not $line) {
        return ""
    }

    $value = ($line -replace "^\s*$([regex]::Escape($Key))\s*=\s*", "").Trim()
    $value = $value -replace "\s+#.*$", ""

    if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
        $value = $value.Substring(1, $value.Length - 2)
    }

    return $value.Trim()
}

function Set-EnvValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Key,
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    $lines = @()
    if (Test-Path $envFile) {
        $lines = Get-Content $envFile
    }

    $updated = $false
    $result = [System.Collections.Generic.List[string]]::new()

    foreach ($line in $lines) {
        if ($line -match "^\s*$([regex]::Escape($Key))\s*=") {
            if (-not $updated) {
                $result.Add("$Key=$Value")
                $updated = $true
            }
            continue
        }
        $result.Add($line)
    }

    if (-not $updated) {
        $result.Add("$Key=$Value")
    }

    Set-Content -Path $envFile -Value $result -Encoding utf8
}

function Require-EnvVar {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Key
    )

    $value = Get-EnvValue -Key $Key
    if ([string]::IsNullOrWhiteSpace($value)) {
        throw "Erro: variavel $Key nao encontrada ou vazia em .env."
    }
}

function Resolve-PythonCommand {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        return @("python", "-c")
    }

    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        return @("py", "-3", "-c")
    }

    throw "Erro: Python nao encontrado para gerar SECRET_KEY."
}

function Resolve-ComposeCommand {
    $legacy = Get-Command docker-compose -ErrorAction SilentlyContinue
    if ($legacy) {
        return @("docker-compose")
    }

    $docker = Get-Command docker -ErrorAction SilentlyContinue
    if ($docker) {
        try {
            & docker compose version | Out-Null
            return @("docker", "compose")
        }
        catch {
            throw "Erro: Docker Compose nao encontrado."
        }
    }

    throw "Erro: Docker nao encontrado."
}

function Invoke-Compose {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$ComposeBase,
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    if ($ComposeBase.Length -eq 1) {
        & $ComposeBase[0] @Args
        return
    }

    & $ComposeBase[0] $ComposeBase[1] @Args
}

$existingSecret = Get-EnvValue -Key "SECRET_KEY"

if ([string]::IsNullOrWhiteSpace($existingSecret)) {
    $pythonCmd = Resolve-PythonCommand
    $code = "import secrets; print(secrets.token_urlsafe(64))"
    $generatedSecret = (& $pythonCmd[0] $pythonCmd[1] $pythonCmd[2] $code).Trim()

    if ([string]::IsNullOrWhiteSpace($generatedSecret)) {
        throw "Erro: nao foi possivel gerar SECRET_KEY."
    }

    Set-EnvValue -Key "SECRET_KEY" -Value $generatedSecret
    Write-Host "SECRET_KEY gerada e salva no .env"
}

Require-EnvVar -Key "DB_USERNAME"
Require-EnvVar -Key "DB_PASSWORD"
Require-EnvVar -Key "DB_DATABASE"

$composeCmd = Resolve-ComposeCommand

Invoke-Compose -ComposeBase $composeCmd -Args @("up", "--build", "-d")
Invoke-Compose -ComposeBase $composeCmd -Args @("exec", "-T", "web", "python", "manage.py", "migrate")
Invoke-Compose -ComposeBase $composeCmd -Args @("exec", "-T", "web", "python", "manage.py", "collectstatic", "--noinput")
Invoke-Compose -ComposeBase $composeCmd -Args @("exec", "-T", "web", "python", "manage.py", "setup_usuarios")

Write-Host "Ambiente de homologacao pronto."
}
finally {
    Pop-Location
}
