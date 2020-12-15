#!/usr/bin/python3
# Kubernetes Manifest Sorter - https://github.com/alpozcan/k8s-manifest-sorter
import argparse, shutil, sys
from yaml import load_all, Loader, dump_all, Dumper

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--backup', default=False, help='Create a backup copy of the original file with .bak suffix. Default: disabled', action='store_true')
parser.add_argument('-f', '--filter', default=False, help='Filter out all resource kinds other than those specified in the order. Default: disabled', action='store_true')
parser.add_argument('-l', '--last', default=False, help='Instead of placing the specified resources at the top, place them at the bottom. Default: disabled', action='store_true')
parser.add_argument("order", nargs=1, help='The order of resource Kinds as a comma-separated list. The resources will be moved to the top of the manifest in the order given.')
parser.add_argument("input_files", nargs="+", default=[], help='One or more input files to process.')

args = parser.parse_args()

for f in args.input_files:
  if args.backup:
    shutil.copyfile(f, f'{f}.bak')

  with open(f, 'r') as file:
    manifest = [ d for d in load_all(file, Loader=Loader) ]

  sorted_resources = []

  kinds = args.order[0].split(',')
  for kind in kinds:
    for resource in manifest:
      if resource['kind'] == kind:
        sorted_resources.append(resource)

  unmatched_resources = [ r for r in manifest if r['kind'] not in kinds ] if not args.filter else []
  final_manifest = [ *sorted_resources, *unmatched_resources ] if not args.last else [ *unmatched_resources, *sorted_resources ]

  with open(f, 'w') as file:
    dump_all(final_manifest, file, Dumper=Dumper, default_flow_style=False)
