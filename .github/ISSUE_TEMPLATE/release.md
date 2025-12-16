---
name: Release
about: Tag a new release
title: 'Tag v<version>'
labels: ''
assignees: ''

---

<!-- Replace <version> with the new version to be released, e.g. 0.3.0 -->

1. [ ] Set the version to tag as a variable:
   ```bash
   VERSION=<version>
   ```
1. [ ] Checkout the latest `main` branch:
   ```bash
   git fetch && git checkout origin/main
   ```
1. [ ] Create and checkout a new branch for tagging the release:
   ```bash
   git branch tag-${VERSION} && git checkout tag-${VERSION}
   ```
1. [ ] Generate release notes for the new version:
   ```bash
   uv run towncrier build --version ${VERSION}
   ```
1. [ ] Commit changes:
   ```bash
   git add -A . && git commit -m "Tag v${VERSION}"
   ```
1. [ ] Push changes:
   ```bash
   git push -u origin tag-${VERSION}
   ```
1. [ ] Make a new release tag PR on GitHub and link it here: (PR URL)
1. [ ] Merge the release tag PR.
1. [ ] Checkout the latest `main` branch:
   ```bash
   git fetch && git checkout origin/main
   ```
1. [ ] Tag and push the latest release:
   ```bash
   git tag ${VERSION} && git push origin ${VERSION}
   ```
1. [ ] Confirm that the new version was released to PyPI: https://pypi.org/project/python-openstack-odooclient
1. [ ] Confirm that a new release was created on GitHub, and that the release notes are correct: https://github.com/catalyst-cloud/python-openstack-odooclient/releases
1. [ ] Confirm that the docs website has been updated, and the Changelog page has the latest changes: https://catalyst-cloud.github.io/python-openstack-odooclient
