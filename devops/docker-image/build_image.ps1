# PowerShell version of build_image.cmd
# Usage:
#   cd <project home directory>
#   powershell -ExecutionPolicy Bypass -File devops/docker-image/build_image.ps1 .

$projectname = "dashboard-server"  # lower case, only
$repositoryname = "tylerm007"
$version = "1.0.0"

function debug($msg) {
    $debug = $false
    # Write-Host $msg
}

debug "\n"
debug "build_image here 1.0"

if ($args.Count -eq 0) {
    Write-Host "\nBuilds docker image for API Logic Project\n"
    Write-Host "  cd <project home directory>"
    Write-Host "  powershell -ExecutionPolicy Bypass -File devops/docker-image/build_image.ps1 [ . | <docker-id> ]"
    Write-Host "    . means use defaults:"
    Write-Host "        ${repositoryname}/${projectname}:$version"
    Write-Host "    <docker-id> means use explicit args: <repository-name> <project-name> <version> eg,"
    Write-Host "        powershell -ExecutionPolicy Bypass -File build_image.ps1 myrepository myproject 1.0.1"
    Write-Host " "
    exit 0
}

Write-Host " "
if ($args[0] -eq ".") {
    debug "..using defaults"
} else {
    debug "using arg overrides"
    $repositoryname = $args[0]
    $projectname = $args[1]
    $version = $args[2]
}

Write-Host "Building ${repositoryname}/${projectname}\n"

# Build the docker image
$buildCmd = "docker build -f devops/docker-image/build_image.dockerfile -t $repositoryname/$projectname --rm ."
Invoke-Expression $buildCmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "\nImage built successfully.. test:\n"
    Write-Host "  powershell -ExecutionPolicy Bypass -File devops/docker-image/run_image.ps1"
    Write-Host " "
    Write-Host "\nNext steps:"
    Write-Host "  docker tag ${repositoryname}/${projectname} ${repositoryname}/${projectname}:$version"
    Write-Host "  docker push ${repositoryname}/${projectname}:$version  # requires docker login"
    Write-Host " "
    Write-Host "  docker tag ${repositoryname}/${projectname} ${repositoryname}/${projectname}:latest"
    Write-Host "  docker push ${repositoryname}/${projectname}:latest"
    Write-Host " "
    Write-Host "Image ready to deploy; e.g. on Azure: https://apilogicserver.github.io/Docs/DevOps-Containers-Deploy"
} else {
    Write-Host "docker build unsuccessful\n"
    exit 1
}
Write-Host " "
exit 0
