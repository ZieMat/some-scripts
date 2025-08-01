# Get paths from environment variables
$baseFolder = $env:PROJECTS_BASE_FOLDER
$zipBasePath = $env:BACKUP_ZIP_PATH

# Verify environment variables are set
if (-not $baseFolder -or -not $zipBasePath) {
    Write-Host "Environment variables not set! Please set:" -ForegroundColor Red
    Write-Host "PROJECTS_BASE_FOLDER: Path to your projects folder" -ForegroundColor Yellow
    Write-Host "BACKUP_ZIP_PATH: Path for zip file storage" -ForegroundColor Yellow
    exit 1
}

# Load ZIP functionality
Add-Type -AssemblyName System.IO.Compression.FileSystem

# Get all subfolders in the base folder
$subFolders = Get-ChildItem -Path $baseFolder -Directory | Select-Object -ExpandProperty Name

# Process each subfolder
foreach ($folder in $subFolders) {
    $sourcePath = Join-Path $baseFolder $folder
    $zipFile = Join-Path $zipBasePath "$folder.zip"
    
    # Check if zip file already exists and delete it
    if (Test-Path $zipFile) {
        try {
            Write-Host "Removing existing zip file: $zipFile" -ForegroundColor Yellow
            Remove-Item -Path $zipFile -Force
            Write-Host "Successfully removed existing zip file" -ForegroundColor Green
        }
        catch {
            Write-Host "Error removing existing zip file: $_" -ForegroundColor Red
            continue
        }
    }
    
    try {
        Write-Host "Zipping folder: $folder" -ForegroundColor Yellow
        [System.IO.Compression.ZipFile]::CreateFromDirectory($sourcePath, $zipFile)
        Write-Host "Successfully created: $zipFile" -ForegroundColor Green
    }
    catch {
        Write-Host "Error creating zip for $folder : $_" -ForegroundColor Red
    }
}

Write-Host "Backup process completed" -ForegroundColor Green