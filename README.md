# k8s-manifest-sorter
Sorts Kubernetes manifest files in-place by resource Kind.

It can also be used to filter resources based on their kind, with the `-f` switch.

## Usage:

```
kms.py [-h] [-b] [-f] [-l] order input_files [input_files ...]

positional arguments:
  order         The order of resource Kinds as a comma-separated list. The
                resources will be moved to the top of the manifest in the
                order given.
  input_files   One or more input files to process.

optional arguments:
  -h, --help    show this help message and exit
  -b, --backup  Create a backup copy of the original file with .bak suffix.
                Default: disabled
  -f, --filter  Filter out all resource kinds other than those specified in
                the order. Default: disabled
  -l, --last    Instead of placing the specified resources at the top, place
                them at the bottom. Default: disabled
```

## Example:

Reorder the manifest so that CustomResourceDefinitions are at the top of the manifest, therefore ensuring they get applied first:
```
./kms.py CustomResourceDefinition manifest.yaml
```

Reorder the manifest so that Projects get created before the Applications to avoid error in Argo CD. Also, take a backup of the original manifest:
```
./kms.py -b AppProject,Application manifest.yaml
```

Reorder the manifest so that Deployments are at the bottom of the manifest, therefore ensuring they get applied last:
```
./kms.py -l Deployment manifest.yaml
```
