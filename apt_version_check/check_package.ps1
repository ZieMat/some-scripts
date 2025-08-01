param (
    [Parameter(Mandatory = $true)]
    [string]$package
)

# Set the Docker image name as a variable
$image = "check_apt_version:1.0"

# Run the Docker container with the user input
docker run --rm -it $image $package