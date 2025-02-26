# Release checklist

01. Ensure local `main` is up to date with respect to `origin/main`.
02. Run pre-commit checks:
    ```console
    $ pre-commit run --all-files
    ```
03. Update `VERSION`; this should simply be removing the `"-dev"` part.
04. Build the entire benchmark with `make -C targets`. It should succeed. If you run it again, it
    should tell you that nothing needs to be rebuilt; otherwise, some binaries failed to build
    (otherwise they would exist and thus the Makefile would not retrigger). Note that this requires
    installing the dependencies of the targets.
05. Update `CHANGELOG.md`.
06. Build the Docker image with the `build.sh` script and make sure it succeeds (check that an image
    with the right version has been created with `docker images`).
07. Run the Docker image with the `run.sh` script and inspect the contents of the container.
08. Commit the changes and tag the commit with the version. For example, for version `X.Y.Z`, tag
    the commit with `git tag -a X.Y.Z`.
09. Push the commit **without pushing the tag** via `git push --no-follow-tags`. Wait for the CI to
    finish, and continue to the next steps only if the CI succeeds.
10. Push the tag with `git push --tags`.
11. Tag and push the Docker image: `docker tag rosarum:X.Y.Z plumtrie/rosarum:X.Y.Z`,
    `docker push plumtrie/rosarum:X.Y.Z`.
12. Tag and push the new image as "latest":
    `docker tag plumtrie/rosarum:X.Y.Z plumtrie/rosarum:latest`,
    `docker push plumtrie/rosarum:latest`.
13. Prepare for the next version by bumping the PATCH number in the version and appending `"-dev"`.
    This means that `"1.2.3"` should become `"1.2.4-dev"`.
